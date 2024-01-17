# Stage used for development in containers
FROM python:3.8

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

# Create a user with the given name, UID and GID 
# Add the user to the sudoers, to allow to execute commands 
# requiring sudoers permissions (such as apt install or access host's docker service).
RUN groupadd --gid ${USER_GID} ${USERNAME} && \
    useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} && \
    apt-get update && \
    apt-get install -y sudo && \
    apt-get clean && \
    echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} && \
    chmod 0440 /etc/sudoers.d/${USERNAME}

# Set current user
USER ${USERNAME}

WORKDIR /code/

# Import requirements from production image
COPY --from=indigopaas/federation-registry:build-docker /app/requirements.txt /code/requirements.txt

# Upgrade pip and install requirements
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ../app /code/app