from pywebpush import webpush
from pywebpush import WebPushException

import json

VAPID_PRIVATE_KEY_PATH = "private_key.pem"
VAPID_PUBLIC_KEY_PATH = "public_key.pem"
VAPID_CLAIMS = {
    "sub": "mailto:simantap.ifitera@gmail.com"
}

def send_web_push(subscription_info, data):
    try:
        webpush(
            subscription_info=subscription_info,
            data=json.dumps(data),
            vapid_private_key=open(VAPID_PRIVATE_KEY_PATH).read(),
            vapid_claims=VAPID_CLAIMS
        )
    except WebPushException as e:
        print(f"Web Push Failed: {e}")