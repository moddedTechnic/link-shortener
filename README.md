# Link Shortener

A simple link shortener.

Set the `AUTH_TOKEN` environment variable to a secure random string.


Either run with Docker (below) or bung into a docker-compose.

```sh
docker build -t link-shortener .
docker run -p 8000:8000 -e AUTH_TOKEN=<AUTH TOKEN HERE> -v ./routes.json:/app/routes.json link-shortener
```
