from app.util.hash import PERFORMANCE_STATS
from bottle import (
    get,
    post,
    redirect,
    request,
    response,
    jinja2_template as template,
)

from app.models.user import create_user, get_user
from app.models.breaches import get_breaches
from app.models.session import (
    delete_session,
    create_session,
    get_session_by_username,
    logged_in,
)
import hashlib

@get('/login')
def login():
    return template('login')

@post('/login')
def do_login(db):
    username = request.forms.get('username')
    password = request.forms.get('password')
    error = None

    plaintext_breaches, hashed_breaches, salted_breaches = get_breaches(db, username)

    if (request.forms.get("login")):
        user = get_user(db, username)
        print(user.password)
        input_hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), user.salt.encode(), 100000).hex()
        if user is None:
            response.status = 401
            error = "{} is not registered.".format(username)
        elif user.password != input_hashed:
            response.status = 401
            error = "Wrong password for {}.".format(username)
        else:
            #pass  # Successful login
            existing_session = get_session_by_username(db, username)
            if existing_session:
                delete_session(db, existing_session)
            session = create_session(db, username)
            response.set_cookie("session", str(session.get_id()), path='/')
            return redirect(f"/{username}")

    elif (request.forms.get("register")):

        for breach in plaintext_breaches:
            print(plaintext_breaches)
            if breach.password == password:
                response.status = 400
                return template("login", error="This password has been breached and cannot be used.")

        # Check against hashed breaches
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        for breach in hashed_breaches:
            if breach.hashed_password == hashed_password:
                response.status = 400
                return template("login", error="This password has been breached and cannot be used.")

        # Check against salted breaches
        for breach in salted_breaches:
            salted_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(breach.salt), 100000).hex()
            if breach.salted_password == salted_hash:
                response.status = 400
                return template("login", error="This password has been breached and cannot be used.")
       
        user = get_user(db, username)
        if user is not None:
            response.status = 401
            error = f"{username} is already taken."
        else:
            create_user(db, username, password)
            # Perform login after successful registration
            session = create_session(db, username)
            response.set_cookie("session", str(session.get_id()), path='/')
            return redirect(f"/{username}")

    else:
        response.status = 400
        error = "Submission error."
    if error:
        
        return template("login", error=error)

@post('/logout')
@logged_in
def do_logout(db, session):
    delete_session(db, session)
    response.delete_cookie("session")
    return redirect("/login")

@get('/stats')
def stats():
    return PERFORMANCE_STATS
