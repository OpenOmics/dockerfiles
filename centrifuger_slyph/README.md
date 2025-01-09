# Utility

# build image from dockerfile

docker build -f centrifuger_slyph/Dockerfile .
#prints sha256:<container hash>.

# push image to docker hub

docker tag <container hash> <docker hub repo>:<image tag>
docker push <docker hub repo>:<image tag>

# References

## slyph 

 - github: https://github.com/bluenote-1577/sylph
 - databases: http://faust.compbio.cs.cmu.edu/sylph-stuff/

Jim Shaw and Yun William Yu. Rapid species-level metagenome profiling and containment estimation with sylph (2024). Nature Biotechnology.

## centrifuger

 - github: https://github.com/mourisl/centrifuger
 - databases: 
    ```
    # human: T2T-CHM13
    ./centrifuger-download -o library -d "vertebrate_mammalian" -t 9606 refseq >> seqid.map
    # human: hg38 reference genome
    ./centrifuger-download -o library -d "vertebrate_mammalian" -a "Chromosome" -t 9606 -c 'reference genome' refseq
    # mouse
    ./centrifuger-download -o library -d "vertebrate_mammalian" -a "Chromosome" -t 10090 -c 'reference genome' refseq >> seqid.map
    ```

Song, L., Langmead B.. Centrifuger: lossless compression of microbial genomes for efficient and accurate metagenomic sequence classification. Genome Biol. 2024 Apr 25;25(1):106. doi: 10.1186/s13059-024-03244-4.