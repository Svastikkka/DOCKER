from app.celery_app import celery_app

@celery_app.task
def check_and_rerun_campaigns():
    print("✅ Checking and rerunning campaigns...")
    # your logic here
