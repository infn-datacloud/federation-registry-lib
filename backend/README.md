This is a [FastAPI](https://fastapi.tiangolo.com/) project.

## Getting Started

Start the virtual environment:

```bash
poetry install
poetry shell
```

Start your neo4j database. If you want, from the top folder, you can run a dockerized version with the following command:

```bash
docker compose -f docker-compose.neo4j.dev.yml up -d
```

Finally run the development server (use the --reload flag to allow server reload on changes):

```bash
uvicorn app.main --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) with your browser to see the automatic documentation. From this page you can test the API.
