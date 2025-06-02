from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.dosen_service import update_dosen_status
from app.services.notification_service import clear_old_notifications
from app.services.notification_service import send_upcoming_bimbingan_notifications
from app.core.config import settings
from app.core.logging import logger
from app.database.session import SessionLocal

def send_upcoming_bimbingan_notification_job():
    logger.info("Running job: send_upcoming_bimbingan_notifications")
    db = SessionLocal()
    try:
        send_upcoming_bimbingan_notifications(db)
        logger.info("Finished job: send_upcoming_bimbingan_notifications")
    except Exception as e:
        logger.exception("Error in job: send_upcoming_bimbingan_notifications")
    finally:
        db.close()

async def update_dosen_status_job():
    logger.info("Running job: update_dosen_status")
    db = SessionLocal()
    try:
        await update_dosen_status(db)
        logger.info("Finished job: update_dosen_status")
    except Exception as e:
        logger.exception("Error in job: update_dosen_status")
    finally:
        db.close()

def clear_old_notifications_job():
    logger.info("Running job: clear_old_notifications")
    try:
        clear_old_notifications()
        logger.info("Finished job: clear_old_notifications")
    except Exception as e:
        logger.exception("Error in job: clear_old_notifications")

def create_scheduler():
    logger.info("Initializing APScheduler...")

    scheduler = AsyncIOScheduler(
        job_defaults={"coalesce": True, "max_instances": 1},
        timezone=settings.timezone,
    )

    scheduler.add_job(
        func=clear_old_notifications_job,
        trigger="cron",
        hour=0,
        minute=0,
        id="clear_old_notifications",
        replace_existing=True
    )

    scheduler.add_job(
        func=send_upcoming_bimbingan_notification_job,
        trigger="interval",
        minutes=1,
        id="send_upcoming_bimbingan_notifications",
        replace_existing=True
    )

    scheduler.add_job(
        func=update_dosen_status_job,
        trigger="cron",
        hour=17,
        minute=5,
        id="update_dosen_status",
        replace_existing=True
    )

    scheduler.start()
    logger.info("Scheduler started with 3 jobs.")
    return scheduler
