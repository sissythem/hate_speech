FROM python:3.7

USER root
ARG RELEASE=master
RUN apt update && apt install -y apt-utils git vim
