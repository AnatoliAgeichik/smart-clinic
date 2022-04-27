from models.notification import Notification
from config import db


def send_notification(recipient_id, message):
    new_notification = Notification(
        recipient_id = recipient_id,
        message = message
    )
    db.session.add(new_notification)
    db.session.commit()
