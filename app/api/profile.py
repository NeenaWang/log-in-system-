from bottle import (
    abort,
    get,
    jinja2_template as template,
)

from app.models.session import logged_in
from app.models.user import get_user

@get("/<username>")
@logged_in
def profile(db, session, username):
    user = get_user(db, username)
    if user is None:
        abort(404)
    return template(
        "profile",
        user=user,
        session_user=get_user(db, session.get_username()),
    )