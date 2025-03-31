import requests


def notifier_plateforme_webhook(platform, event, patient_data):
    if platform.webhook_url:
        try:
            requests.post(platform.webhook_url, json={
                "event": event,
                "upi": patient_data.get('upi'),
                "data": patient_data
            }, timeout=5)
        except requests.RequestException:
            pass  # log ou retry si nécessaire
