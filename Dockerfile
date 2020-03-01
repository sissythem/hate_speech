FROM python:3.7

USER root
ARG RELEASE=master
RUN apt update && apt install -y apt-utils git vim
RUN git clone --branch $RELEASE --single-branch https://gitlab.com/sw-archive/di-msc/thesis/hate_speech.git
RUN cd hate_speech && pip3 install -r requirements.txt
ENV HOME=/hate_speech
WORKDIR ${HOME}

COPY scripts/setup.sh ${HOME}
COPY scripts/entrypoint.sh ${HOME}
COPY scripts/env_prep.py ${HOME}
COPY scripts/data_import.py ${HOME}

RUN rm -rf scripts/ docs/

CMD bash setup.sh && sleep(1) && bash entrypoint.sh
# CMD tail -f /dev/null