# Create requirements.txt from poetry dependencies
FROM python:3.8 as requirements

WORKDIR /tmp

RUN pip install poetry

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /tmp/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
ENV INSTALL_CMD="poetry export -f requirements.txt --output requirements.txt --without-hashes"
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then ${INSTALL_CMD} --dev ; else ${INSTALL_CMD} ; fi"


# Stage used for development in containers
FROM python:3.8 as development

WORKDIR /code/

COPY --from=requirements /tmp/requirements.txt /code/requirements.txt

# Upgrade pip and install requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app


# Stage used in production
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8 as prod-backend

WORKDIR /app/

COPY --from=requirements /app/requirements.txt /app/requirements.txt

RUN pip install --user --upgrade pip
RUN pip install --user --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app
ENV PYTHONPATH=/app
