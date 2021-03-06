FROM python:3.7-alpine3.7

USER root
ARG RELEASE=master
RUN apk add --no-cache mariadb-client-libs mysql-client && \
    apk add --no-cache --virtual .build-deps build-base git mariadb-dev libffi-dev git && \
    git clone --branch $RELEASE --single-branch https://github.com/sissythem/hate_speech.git && \
    pip install --upgrade pip && \
    pip install -r /hate_speech/requirements.txt && \
    pip install gunicorn && \
    rm -rf /hate_speech/.git && \
    apk del .build-deps

RUN apk add --no-cache bash vim git

ENV HOME=/hate_speech
WORKDIR ${HOME}

COPY scripts/setup.sh ${HOME}
COPY scripts/entrypoint.sh ${HOME}
COPY scripts/env_prep.py ${HOME}
COPY scripts/data_import.py ${HOME}

RUN rm -rf scripts/ docs/

CMD bash setup.sh && sleep(1) && python env_prep.py && sleep(1) && bash entrypoint.sh
# CMD tail -f /dev/null