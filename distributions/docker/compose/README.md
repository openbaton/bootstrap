# Open Baton via Docker Compose
## System Requirements
You will need:

- [Docker](https://www.docker.com/community-edition#/download) (>=17.06)
- [Docker Compose](https://docs.docker.com/compose/install/) (>=1.14)
- A checkout of this repository

## Simple deploy

Change into the directory containing the composition YAML files and issue [up](https://docs.docker.com/compose/reference/up/) command. You can choose to issue a simple curl loop to check if the orchestrator is up and check on the logged output of e.g. the orchestrator.

```bash
$ cd bootstrap/distribution/docker/compose
$ docker-compose -f min-compose.yml up -d
$ # until curl -sSf --stderr /dev/null http://localhost:8080; do printf '.' && sleep 5;done
$ # docker logs -f compose_nfvo_1
```

