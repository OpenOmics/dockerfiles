FROM continuumio/miniconda3
RUN conda install -c conda-forge -c bioconda centrifuger sylph
RUN apt-get update -y -qq
RUN apt-get install wget -y -qq
# RUN mkdir /refs; cd /refs; wget http://faust.compbio.cs.cmu.edu/sylph-stuff/gtdb-r220-c200-dbv1.syldb
