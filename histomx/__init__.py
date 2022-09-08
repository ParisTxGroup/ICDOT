import functools
import os
import subprocess
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException
from fastapi.responses import HTMLResponse, Response

app = FastAPI()


@functools.lru_cache(maxsize=32)
def get_histomx_html(rccdata: bytes):

    rmdfilepath = os.getenv("HISTOMX_RMD_PATH")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdirpath = Path(tmpdir)

        rccfilepath = tmpdirpath / "input_file.rcc"
        htmloutpath = tmpdirpath / "output_file.html"

        with rccfilepath.open(mode="wb") as rccfile:
            rccfile.write(rccdata)

        p = subprocess.run(
            [
                "R",
                "-e",
                """
        rmarkdown::render("{rmdfilepath}",
            output_file="{outfilepath}",
            params=list(
                rcc_file='{rccfilepath}'
            )
        )
        """.format(
                    rmdfilepath=rmdfilepath,
                    outfilepath=htmloutpath,
                    rccfilepath=rccfilepath,
                ),
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
def generate_histomx_html_report(rccdata: bytes = File(...)):
    html = get_histomx_html(rccdata)
    return HTMLResponse(content=html)


@app.post("/histomx_report/pdf")
@functools.lru_cache(maxsize=32)
def generate_histomx_pdf_report(rccdata: bytes = File(...)):

    html = get_histomx_html(rccdata)

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
