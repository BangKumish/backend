from apscheduler.schedulers.background import BackgroundScheduler
from app.services.notification_service import clear_old_notifications
from app.services.notification_service import send_upcoming_bimbingan_notifications
from app.core.config import settings
from app.database.session import SessionLocal

def create_scheduler():
    scheduler = BackgroundScheduler(
        job_defaults={
            "coalesce": True,
            "max_instances": 1,
        },
        timezone=settings.timezone,
    )

    def job_function():
        db = SessionLocal()
        try:
            send_upcoming_bimbingan_notifications(db)
        finally:
            db.close()

    scheduler.add_job(
        func=clear_old_notifications,
        trigger="cron",
        hour=0,
        minute=0
    )

    scheduler.add_job(
        func=job_function,
        trigger="interval",
        minutes=1,
    )

    scheduler.start()
    return scheduler