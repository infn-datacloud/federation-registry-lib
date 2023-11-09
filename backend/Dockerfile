FROM airdock/python-poetry as requirements

WORKDIR /app/

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
ENV INSTALL_CMD="poetry export -f requirements.txt --output requirements.txt --without-hashes"
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then ${INSTALL_CMD} --dev ; else ${INSTALL_CMD} ; fi"


FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8 as backend

WORKDIR /app/

COPY --from=requirements /app/requirements.txt /app/requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --user --no-cache-dir --upgrade -r /app/requirements.txt

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

COPY ./app /app/app
ENV PYTHONPATH=/app
