<div align="center">
  <h1>dockerfiles <sup>:whale:</sup></h1>
  <b><i>A collection of dockerfiles to enable reproducible scientific research and beyond!</i></b>
</div>

## Overview

This repository contains dockerfiles for commonly used bioinformatics tools and applications. Each child directory represents a _dockerized_ tool. If multiple versions of a tool exist, there maybe a sub-directory for each version of the tool.

Within any given tool's directory, you will find a _REAME.md_ and a _Dockerfile_. Each _README.md_ contains instructions for how to `build`, `tag`, and `push` an image to Dockerhub. 

Please note that each Docker image also contains a copy of its _Dockerfile_. It can be found within the following location: `/opt2/Dockerfile`.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install:
- [`docker`](https://docs.docker.com/install/)  
- [`git`](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)  

Accounts you need:
- [`Dockerhub`](https://hub.docker.com/signup)  

### Installation

Once the prerequisites have been met, setting up a development environment is easy!

Let's start off by cloning this repository:
```bash
git clone https://github.com/OpenOmics/dockerfiles.git
cd dockerfiles
```

## Versioning

We use `git`, `GitHub`, and `DockerHub` for versioning. For the versions available on GitHub, please see the [tags on this repository](https://github.com/OpenOmics/dockerfiles/tags).
For more information about available container images, please visit: 
- https://hub.docker.com/u/skchronicles 

<hr>

<p align="center">
  <a href="#dockerfiles-whale">Back to Top</a>
</p>
