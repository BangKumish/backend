from pywebpush import webpush
from pywebpush import WebPushException
from dotenv import load_dotenv

from app.models.subscription import PushSubscription

import json
import os

load_dotenv()

class PushService:
    def __init__(self):
        self.vapid_private_key = os.getenv("VAPID_PRIVATE_KEY")
        self.vapid_public_key = os.getenv("VAPID_PUBLIC_KEY")
        self.vapid_claims = {
            "sub": "mailto:simantap.ifitera@gmail.com"
        }

    def get_public_key(self):
        return self.vapid_public_key

    def send_notification(self, subscription: dict, data: dict):
        try:
            webpush(
                subscription_info=subscription,
                data=json.dumps(data),
                vapid_private_key=self.vapid_private_key,
                vapid_claims=self.vapid_claims
            )
        except WebPushException as e:
            print(f"Web Push Failed: {e}")
            raise e

    def send_bulk_notification(self, subcriptions: list[PushSubscription], data: dict):
        sent = 0
        failed = 0
        for sub in subcriptions:
            try:
                self.send_notification({
                    "endpoint": sub.endpoint,
                    "keys": {
                        "p256dh": sub.keys_p256dh,
                        "auth": sub.keys_auth
                    }
                }, data)
                sent += 1
            except Exception as e:
                print(f"Failed to send to {sub['endpoint']}: {repr(e)}")
                failed += 1
        return {"sent": sent, "failed": failed}