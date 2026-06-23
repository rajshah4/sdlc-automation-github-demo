FROM python:3.12-slim

WORKDIR /app
COPY petstore_app ./petstore_app
COPY web ./web

ENV PYTHONPATH=/app
ENV PORT=8080

CMD ["python", "-m", "petstore_app.cloud_run_app"]
