## Docker

### Steps for Building Docker Images

Directly below are instructions for building an image using the provided Dockerfile:

```
# See listing of images on computer
docker image ls

# Build from Dockerfile
docker build --no-cache -f Dockerfile --tag=centrifuger_sylph:0.0.1 .

# Testing, take a peek inside
docker run -ti centrifuger_sylph:0.0.1 /bin/bash

# Updating Tag  before pushing to DockerHub
docker tag centrifuger_sylph:0.0.1 rroutsong/centrifuger_sylph:0.0.1
docker tag centrifuger_sylph:0.0.1 rroutsong/centrifuger_sylph         # latest

# Check out new tag(s)
docker image ls

# Push new tagged image to DockerHub
docker push rroutsong/centrifuger_sylph:0.0.1
docker push rroutsong/centrifuger_sylph:latest
```

> **Please Note**: Any references to `rroutsong` should be replaced your username if you would also like to push the image to a non-org account.

### Other Recommended Steps

Scan your image for known vulnerabilities:

```bash
docker scan centrifuger_sylph:0.0.1
```


## Downloading References

### sylph 

Sylph<sub>1</sub> is a tool for rapid species-level metagenome profiling and containment estimation. It is designed to be fast and accurate, and can be used to profile metagenomic samples in a matter of seconds. sylph is based on a novel algorithm that uses a combination of k-mer counting and machine learning to classify reads at the species level.

Sylph has pre-built databases for a number of species, including bacteria, viruses, and fungi. More information about each of the available pre-built databases can be found on their [wiki](https://github.com/bluenote-1577/sylph/wiki/Pre%E2%80%90built-databases).

Here for more information, please also visit:
- Github: https://github.com/bluenote-1577/sylph 
- Download Databases: http://faust.compbio.cs.cmu.edu/sylph-stuff/ 

### centrifuger

Centrifuger<sub>2</sub> is a fast and accurate metagenomic sequence classification tool. It implemented a novel lossless compression method, run-block comprssed BWT, and other strategies to efficiently reduce the size of the microbial genome database like RefSeq.

For more information about centrifuger, please visit:
- Github: https://github.com/mourisl/centrifuger

#### Download Databases

```bash
# Human: T2T-CHM13
./centrifuger-download -o library -d "vertebrate_mammalian" -t 9606 refseq >> seqid.map

# human: hg38 reference genome
./centrifuger-download -o library -d "vertebrate_mammalian" -a "Chromosome" -t 9606 -c 'reference genome' refseq

# Mouse
./centrifuger-download -o library -d "vertebrate_mammalian" -a "Chromosome" -t 10090 -c 'reference genome' refseq >> seqid.map
```

### References

1. Jim Shaw and Yun William Yu. Rapid species-level metagenome profiling and containment estimation with sylph (2024). Nature Biotechnology.
2. Song, L., Langmead B.. Centrifuger: lossless compression of microbial genomes for efficient and accurate metagenomic sequence classification. Genome Biol. 2024 Apr 25;25(1):106. doi: 10.1186/s13059-024-03244-4.
