# Celery

Celery setup with flower

```python
# Worker
celery -A app.celery_app worker --loglevel=info

# Beat
celery -A app.celery_app beat --loglevel=info
```

```bash
docker compose up -d --build --scale celery-worker=2
```
### To build image
```bash
docker build -t gcr.io/nonprod1-svc-r4rc/celery-worker:0.0.2  --platform linux/amd64 .
docker push gcr.io/nonprod1-svc-r4rc/celery-worker:0.0.2
```
### To pull and run image
```bash
gcloud auth login
gcloud auth configure-docker
docker pull gcr.io/nonprod1-svc-r4rc/celery-worker:latest
docker run -d gcr.io/nonprod1-svc-r4rc/celery-worker:latest
```