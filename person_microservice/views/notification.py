from flask import Blueprint, request, Response

from models.notification import Notification
from config import db
from schemas import notification_schema, notifications_schema
from services.auth import token_required, get_user_from_request
from services.services import is_equal_user_from_request


def create_notification(data):
    import pdb

    pdb.set_trace()
    notification = Notification(**data)
    db.session.add(notification)
    db.session.commit()


notification_view = Blueprint("notification", __name__)


@token_required
@notification_view.route("user/<user_id>/received", methods=["Get"])
def get_all_notification(user_id):
    if not is_equal_user_from_request(user_id, request):
        return Response(status=403)
    notifications = Notification.query.filter_by(recipient_id=user_id)
    return Response(
        notifications_schema.dumps(notifications),
        status=200,
        mimetype="application/json",
    )


@token_required
@notification_view.route("user/<user_id>/received/<notification_id>", methods=["Post"])
def create_notification(user_id, notification_id):
    if not is_equal_user_from_request(user_id, request):
        return Response(status=403)
    notification_data = notification_schema.load(request.json)
    Notification.query.filter_by(id=notification_id).update(**notification_data)
    db.session.commit()
    return Response(status=200)


@token_required
@notification_view.route(
    "user/<user_id>/received/<notification_id>", methods=["Delete"]
)
def delete_notification(user_id, notification_id):
    if not is_equal_user_from_request(user_id, request):
        return Response(status=403)
    db.session.delete(Notification.query.filter_by(id=notification_id))
    db.session.commit()
    return Response(status=204)


@token_required
@notification_view.route(
    "user/<user_id>/received/<notification_id>", methods=["Delete"]
)
def delete_notification(user_id, notification_id):
    if not is_equal_user_from_request(user_id, request):
        return Response(status=403)
    notification_data = notification_schema.load(request.json)
    Notification.query.filter_by(id=notification_id).update(**notification_data)
    db.session.commit()
    return Response(status=200)
