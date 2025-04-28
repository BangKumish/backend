from apscheduler.schedulers.background import BackgroundScheduler

from app.services.notification_service import send_upcoming_bimbingan_notifications
from app.core.config import settings
from app.database.session import get_db


def create_scheduler():
    scheduler = BackgroundScheduler(
        job_defaults={
            "coalesce": True,
            "max_instances": 1,
        },
        timezone=settings.timezone,
    )
    scheduler.add_job(
        func=lambda: send_upcoming_bimbingan_notifications(next(get_db())),
        trigger="interval",
        minutes=1,
    )
    scheduler.start()
    return scheduler