from datetime import datetime
from datetime import timedelta
from sqlalchemy.orm import Session 

from app.database.models.subscription import PushSubscription
from app.database.models.waktu_bimbingan import WaktuBimbingan
from app.schemas.push import PushNotificationPayload
from app.services.push_service import PushService
from app.core.logging import logger

sent_notifications = {}
push = PushService()

def add_notification(notification_id):
    sent_notifications[notification_id] = datetime.now()

def clear_old_notifications():
    now = datetime.now()
    cutoff_time = now - timedelta(days=1)  # Clear notifications older than 1 day
    global sent_notifications
    sent_notifications = {
        nid: timestamp for nid, timestamp in sent_notifications.items()
        if timestamp > cutoff_time
    }
    print("✅ Cleared old notifications from sent_notifications")

async def send_push_notification(
    db: Session,
    target_user_ids: list[str],
    push_payload: PushNotificationPayload
): 
    for user_id in target_user_ids:
        print(f"📪 Preparing WebPush for {user_id}")
        
        subscriptions = db.query(PushSubscription).filter(
            PushSubscription.user_id == user_id
        ).all()

        if subscriptions:
            push.send_bulk_notification(
                subscriptions,
                data={
                    "title": push_payload.title,
                    "body": push_payload.body,
                    "url": push_payload.url
                }
            )
        else:
            print(f"❗ No subscriptions found for {user_id}")


def send_upcoming_bimbingan_notifications(db: Session):
    now = datetime.now()
    thirty_minutes_later = now + timedelta(minutes=30)

    upcoming_sessions = db.query(WaktuBimbingan).filter(
        WaktuBimbingan.tanggal == now.date(),
        WaktuBimbingan.waktu_mulai.between(now.time(), thirty_minutes_later.time())
    ).all()

    for session in upcoming_sessions:
        for antrian in session.antrian_bimbingan:
            notification_id = f"{antrian.id_antrian}-{antrian.mahasiswa_nim}-{str(session.waktu_mulai)}"

            if notification_id in sent_notifications:
                continue

            if antrian.status_antrian in ["Dalam Bimbingan", "Selesai"]:
                continue

            subscription = db.query(PushSubscription).filter(
                PushSubscription.user_id == antrian.mahasiswa_nim
            ).first()

            if subscription:
                try:
                    push.send_notification(
                        subscription={
                            "endpoint": subscription.endpoint,
                            "keys": {
                                "p256dh": subscription.keys_p256dh,
                                "auth": subscription.keys_auth
                            }
                        },
                        data={
                            "title": "Pengingat Bimbingan",
                            "body": f"Bimbingan Anda akan dimulai pada {session.waktu_mulai.strftime('%H:%M')} di {session.lokasi}.",
                            "data": {
                                "bimbingan_id": session.bimbingan_id,
                                "tanggal": session.tanggal.isoformat(),
                                "waktu_mulai": session.waktu_mulai.strftime('%H:%M'),
                                "lokasi": session.lokasi
                            }
                        }
                    )
                    add_notification(notification_id)
                    logger.info(f"✅ Sent notification to {antrian.mahasiswa_nim} for session {session.waktu_mulai.strftime('%H:%M')}")
                except Exception as e:
                    logger.error(f"Failed to send notification to {antrian.mahasiswa_nim}: {e}")