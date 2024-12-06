## Steps for Building Docker Images

**Please note:** 

`cellranger mkfastq` needs bcl2fastq2 (>=2.20) to convert BCL files to FastQ files. Before running any of the steps outlined below, the [linux RPM file](https://emea.support.illumina.com/downloads/bcl2fastq-conversion-software-v2-20.html) will need to be downloaded from Illumina's website and copied into the same directory as this README.md and Dockerfile. After logging into Illumina's website and downloading the linux RPM, please unzip the download and copy the RPM file into this folder. That RPM file can be provided to the docker build command below.

The URL to download cellranger needs to be provided with `docker build` command. After logging into 10x's website, the download URL can be found on the [10x Genomics website](https://www.10xgenomics.com/support/software/cell-ranger/downloads#download-links). The URL will be part of the wget/curl command they provide to download cellranger once you have logged in. 
 
The download URL will look something like this:

```txt
https://cf.10xgenomics.com/releases/cell-exp/cellranger-9.0.0.tar.gz?Expires=123&Key-Pair-Id=ABC&Signature=1a2b3c4d"
```

Directly below are instructions for building an image using the provided Dockerfile, the downloaded RPM file, and the cellranager download URL. The following steps will allow you to build the image, test it, and push it to DockerHub:

```bash
# See listing of images on computer
docker image ls

# Build from Dockerfile and RPM file,
# See instructions above for gettting
# the RPM file from Illumina's website
# and getting a cellranger download URL.
# You need to do this first before
# running any of the commands below.
RPM_FILE=$(ls *.rpm)
CELLRANGER_URL="add_your_url_here"
docker build --build-arg BCL2FQ_RPM=${RPM_FILE} --build-arg CELLRANGER_URL="${CELLRANGER_URL}" --no-cache -f Dockerfile --tag=cellranger:9.0.0 .

# Testing, take a peek inside
docker run -ti cellranger:9.0.0 /bin/bash

# Updating Tag  before pushing to DockerHub
docker tag cellranger:9.0.0 skchronicles/cellranger:9.0.0
docker tag cellranger:9.0.0 skchronicles/cellranger         # latest

# Check out new tag(s)
docker image ls

# Push new tagged image to DockerHub
docker push skchronicles/cellranger:9.0.0
docker push skchronicles/cellranger:latest
```

### Other Recommended Steps

Scan your image for known vulnerabilities:

```bash
docker scan cellranger:9.0.0
```

> **Please Note**: Any references to `skchronicles` should be replaced your username if you would also like to push the image to a non-org account.