FROM rocker/r-base

RUN apt-get update && apt-get install -y \
    r-cran-biocmanager \
    wkhtmltopdf cargo make pandoc gsfonts \
    libnlopt-dev libcurl4-openssl-dev libssl-dev libicu-dev \
    libnode-dev libmagick++-dev libxml2-dev \
    libpng-dev libfontconfig1-dev libfreetype6-dev \
    imagemagick libmagick++-dev libharfbuzz-dev \
    libfribidi-dev libgmp3-dev

WORKDIR /root/

COPY ./histomx/r-prebuilt-packages.txt ./
RUN xargs -a ./r-prebuilt-packages.txt apt-get install -y

# Install all required packages through BiocManager.
COPY ./histomx/r-packages-install.R ./
RUN Rscript r-packages-install.R

# Install python & pip, this is used for exposing an http endpoint.
RUN apt-get update && apt-get install -y python3 python3-pip

COPY ./requirements/histomx.txt ./requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# Copy the python code for the server.
COPY ./histomx ./histomx

# Copy necessary all other necessary files.
COPY . .

ENV HISTOMX_TEMPLATES='{"DEFAULT": "./histomx/example.Rmd"}'

CMD ["uvicorn", "histomx:app", "--host", "0.0.0.0", "--port", "80"]
