FROM python:3.10.9-slim-buster

# Environment var
ENV HOME=/home/root \
    DEBIAN_FRONTEND=noninteractive \
    \
    ## PYTHON RELATED THINGS
    PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    #pyenv
    PYENV_ROOT=/home/root/.pyenv \
    \
    # poetry
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    \
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    VIRTUAL_ENV="/opt/pysetup/.venv"

ENV PATH=$POETRY_HOME/bin:$VENV_PATH/bin:${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PYENV_ROOT}/versions/${PYTHON_VERSION}/bin:$PATH

RUN mkdir -p $HOME && apt-get update  
RUN apt-get -y install \
    ca-certificates \ 
    gcc \ 
    libpq-dev \
    python3-dev \
    musl-dev \
    libffi-dev \
    automake \
    make \
    g++ \
    subversion

COPY ./pyproject.toml ${HOME}/app/pyproject.toml
COPY ./poetry.toml ${HOME}/app/poetry.toml
COPY ./poetry.lock ${HOME}/app/poetry.lock

# install poetry and requirements
RUN pip3 install poetry

# Install dependencies globally (for ease of use)
RUN cd ${HOME}/app/ && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . ${HOME}/app/
WORKDIR "${HOME}/app"

ENV PATH=${HOME}/app/scripts:$PATH

RUN chmod +x ${HOME}/app/scripts/*

WORKDIR ${HOME}/app
CMD ["./scripts/start-dev.sh"]
