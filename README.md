# dockerfiles

A collection of dockerfiles to enable reproducible scientific research and beyond! This repository contains dockerfiles for commonly used used bioinformatics tools and applications.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install:
- [`docker`](https://docs.docker.com/install/)  
- [`git`](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)  

Accounts you need:
- [`Dockerhub`](https://hub.docker.com/signup)  

### Installation

A step by step series of examples that tell you how to get a development environment up and running

Let's start off by cloning this repository
```bash
git clone https://github.com/OpenOmics/dockerfiles.git
cd dockerfiles
```

Each of the listed directories represents a _dockerized_ tool. If multiple versions of a tool exist, there maybe a sub-directory for each version of the tool. 

Within any given tool's directory, you will find a _REAME.md_ and a _Dockerfile_. The _README.md_ contains instructions for how to `build`, `tag`, and `push` the docker images to Dockerhub. 

## Versioning

We use `git`, `GitHub`, and `DockerHub` for versioning. For the versions available on GitHub, please see the [tags on this repository](https://github.com/skchronicles/Docker/tags).
For more information about available container images, please visit: 
- https://hub.docker.com/u/skchronicles 


<hr>

<p align="center">
	<a href="#dockerfiles">Back to Top</a>
</p>