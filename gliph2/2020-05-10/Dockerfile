FROM centos:7
RUN mkdir -p /opt2
# Downloaded from Nature paper code availability:
# https://www.nature.com/articles/s41587-020-0505-4#code-availability
ADD irtools.centos /usr/bin/
RUN chmod a+rx /usr/bin/irtools.centos
ADD Dockerfile /opt2/
RUN chmod -R a+rX /opt2
