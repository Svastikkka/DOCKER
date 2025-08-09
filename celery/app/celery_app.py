from celery import Celery
from celery.schedules import crontab
import os

# Create Celery application
celery_app = Celery(
    "app",
    broker=os.environ["CELERY_BROKER_URL"],
    backend=os.environ["CELERY_BROKER_URL"]
)

# Auto-discover tasks in the 'app' package
celery_app.autodiscover_tasks(['app'])

# Periodic tasks
celery_app.conf.beat_schedule = {
    'run-every-minute': {
        'task': 'app.tasks.check_and_rerun_campaigns',
        'schedule': crontab(),
    },
}

celery_app.conf.timezone = 'UTC'
