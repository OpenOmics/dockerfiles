FROM continuumio/miniconda3
RUN conda install -c conda-forge -c bioconda  sylph
RUN apt-get update -y -qq
RUN apt-get install wget git libz-dev build-essential libpthread-stubs0-dev -y -qq
RUN mkdir /work; cd /work; git clone https://github.com/mourisl/centrifuger.git; cd centrifuger; make CXXFLAGS="-Wall -g -O2 -march=x86-64"
ADD centrifudger-link.sh /
RUN ./centrifudger-link.sh
