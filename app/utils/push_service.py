from pywebpush import webpush
from pywebpush import WebPushException
from dotenv import load_dotenv

import json
import os

load_dotenv()

VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")

VAPID_CLAIMS = {
    "sub": "mailto:simantap.ifitera@gmail.com"
}

def send_web_push(subscription_info, data):
    try:
        webpush(
            subscription_info=subscription_info,
            data=json.dumps(data),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS
        )
    except WebPushException as e:
        print(f"Web Push Failed: {e}")