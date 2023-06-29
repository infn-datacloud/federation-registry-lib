# Run the Change Management Database

We suggest to run the python program in containers. To do so, you need [docker](https://www.docker.com/) installed on your system.

At first you need to create an empty `.env` file in the top folder. You can fill this file later.

To launch the FastAPI application use the docker cli command (to run it in background, add `-d` arguments):

```
docker compose up -d
```

By default, the app will accept REST requests to the standard url `http://localhost:8000`.
