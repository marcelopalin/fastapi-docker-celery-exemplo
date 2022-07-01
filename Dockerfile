# pull official base image
FROM python:3.10.1-slim-buster as python-base

LABEL maintainer="Marcelo Palin <marcelo.palin@ampereconsultoria.com.br>"
LABEL description="Dockerfile Projeto Exemplo"

# set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/home/ubuntu/proj-celery-exemplo" \
    VENV_PATH="/home/ubuntu/proj-celery-exemplo/.venv" \
    CHROMEDRIVER_DIR="/usr/bin"\
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.13 \
    POETRY_HOME="/home/ubuntu/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1

# create user ubuntu and add to Group Sudo
ARG user=ubuntu
ARG group=ubuntu
ARG uid=1000
ARG gid=1000
RUN groupadd -g ${gid} ${group}
RUN useradd -rm -d /home/${user} -s /bin/bash  -g root -G sudo,${group} -u ${uid} ${user}
RUN mkdir -p /etc/sudoers.d
RUN touch /etc/sudoers.d/dont-prompt-ubuntu-for-sudo-password
RUN echo "${user} ALL=(ALL:ALL) NOPASSWD: ALL" | tee /etc/sudoers.d/dont-prompt-${user}-for-sudo-password

# Chown all the files to the app user.
RUN mkdir -p $PYSETUP_PATH
RUN chown -R ${user}:${group} $PYSETUP_PATH
RUN mkdir -p $PYSETUP_PATH/logs
RUN chown -R ${user}:${group} $PYSETUP_PATH/logs

# prepend poetry, venv and cromedriver to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$CHROMEDRIVER_DIR:$PATH"


# `builder-base` stage is used to build deps + create our virtual environment
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # install sudo
        sudo \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential \
        # chromedriver chrome
        x11vnc \
        xvfb \
        wget \
        unzip \
        joe \
        gnupg \
        curl \
        netcat \
        && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
        && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
        && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
        && apt-get update && apt-get -y install google-chrome-stable

# Add Tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

# Install Chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d $CHROMEDRIVER_DIR

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH

# copie tudo do diretório
# Exceto o que foi definido no .dockerignore
COPY . $PYSETUP_PATH

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev

# `development` image is used during development / testing
FROM python-base as development
ENV FASTAPI_ENV=development
WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

#
RUN mkdir -p $PYSETUP_PATH
RUN chown -R ${user}:${group} $PYSETUP_PATH
RUN mkdir -p $PYSETUP_PATH/logs
RUN chown -R ${user}:${group} $PYSETUP_PATH/logs

# quicker install as runtime deps are already installed
RUN poetry install

# will become mountpoint of our code
# /home/ubuntu/proj-celery-exemplo
WORKDIR $PYSETUP_PATH

EXPOSE 8000
CMD ["uvicorn", "--reload", "app.main:app"]

# Troca do usuário root para o usuario criado
# No .env definimos o UID=1002 igual definimos aqui
USER ${user}


# `production` image used for runtime
FROM python-base as production
ENV FASTAPI_ENV=production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
# CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
WORKDIR $PYSETUP_PATH

RUN mkdir -p $PYSETUP_PATH
RUN chown -R ${user}:${group} $PYSETUP_PATH
RUN mkdir -p $PYSETUP_PATH/logs
RUN chown -R ${user}:${group} $PYSETUP_PATH/logs
# copie tudo do diretório
# Exceto o que foi definido no .gitignore
COPY . $PYSETUP_PATH

EXPOSE 8000
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]

# Troca do usuário root para o usuario criado
USER ${user}
