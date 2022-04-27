from services.auth import get_user_from_request


def get_object_by_id(Model, id):
    return Model.query.filter_by(id=id).first()


def is_equal_user_from_request_with_user_db(request_user, db_user):
    return request_user.id == db_user.id


def is_equal_user_from_request(id_from_request, request):
    user = get_user_from_request(request)
    return id_from_request == user.id
