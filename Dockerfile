# Create requirements.txt from poetry dependencies
FROM python:3.8 AS requirements

WORKDIR /tmp

RUN pip install poetry

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


# Stage used in production
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8 AS production

WORKDIR /app/

COPY --from=requirements /tmp/requirements.txt /app/requirements.txt

RUN pip install --user --upgrade pip && \
    pip install --user --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app
ENV PYTHONPATH=/app
