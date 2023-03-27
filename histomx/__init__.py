import functools
import json
import subprocess
import tempfile
import typing
from enum import Enum
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel, BaseSettings

# TODO: import base64  # for rcc_file encoding.


app = FastAPI()


class Settings(BaseSettings):
    class Config:
        env_prefix = "HISTOMX_"

    templates: dict[str, str]


settings = Settings()

Templates = Enum("Templates", {k: k for k in settings.templates})


class HashableBaseModel(BaseModel):
    def __hash__(self):
        return hash((type(self), self.json()))


class ReportParameters(HashableBaseModel):
    rccdata: bytes
    template: Templates
    rna_metadata: dict[str, typing.Any]
    patient_metadata: dict[str, typing.Any]


@functools.lru_cache(maxsize=32)
def get_histomx_html(params: ReportParameters):
    rmdfilepath = settings.templates[params.template.value]

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdirpath = Path(tmpdir)

        htmloutpath = tmpdirpath / "output_file.html"
        rccfilepath = tmpdirpath / "input_file.rcc"
        rnajsonpath = tmpdirpath / "rna_file.json"
        patientjsonpath = tmpdirpath / "patient_file.json"

        with rccfilepath.open(mode="wb") as rccfile:
            rccfile.write(params.rccdata)

        for jsonpath, jsondata in [
            (rnajsonpath, params.rna_metadata),
            (patientjsonpath, params.patient_metadata),
        ]:
            with jsonpath.open(mode="w") as jsonfile:
                json.dump(jsondata, jsonfile)

        p = subprocess.run(
            [
                "R",
                "-e",
                f"""
        rmarkdown::render("{rmdfilepath}",
            output_file="{htmloutpath}",
            params=list(
                rcc_file="{rccfilepath}",
                rna_file="{rnajsonpath}",
                patient_file="{patientjsonpath}"
            )
        )
        """,
            ]
        )

        if p.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail="We had a problem generating the HTML report.",
            )

        with htmloutpath.open(mode="rb") as htmlfile:
            return htmlfile.read()


@app.post("/histomx_report/html")
@functools.lru_cache(maxsize=32)
def generate_histomx_html_report(params: ReportParameters):
    html = get_histomx_html(params)
    return HTMLResponse(content=html)


@app.post("/histomx_report/pdf")
@functools.lru_cache(maxsize=32)
def generate_histomx_pdf_report(params: ReportParameters):
    html = get_histomx_html(params)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdirpath = Path(tmpdir)

        htmloutpath = tmpdirpath / "output_file.html"
        pdfoutpath = tmpdirpath / "output_file.pdf"

        with htmloutpath.open(mode="wb") as htmlfile:
            htmlfile.write(html)

        p = subprocess.run(["wkhtmltopdf", htmloutpath, pdfoutpath])
        if p.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail="We had a problem converting the HTML report to pdf.",
            )

        try:
            with pdfoutpath.open(mode="rb") as pdffile:
                pdf = pdffile.read()
        except FileNotFoundError:
            raise HTTPException(
                status_code=500,
                detail="We had a problem generating the report :-(",
            )

    return Response(content=pdf, media_type="application/pdf")
