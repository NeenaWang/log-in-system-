from bottle import (
    post,
    request,
    response,
    jinja2_template as template,
)

from app.models.user import (
    get_user,
)

from app.models.session import (
    logged_in,
)


@post('/pay')
@logged_in
def do_payment(db, session):
    sender = get_user(db, session.get_username())
    recipient = get_user(db, request.forms.get('recipient'))
    payment_amount = int(request.forms.get('amount'))
    error = None
    if (sender.get_coins() < payment_amount):
        response.status = 400
        error = "Not enough funds."
    elif (recipient is None):
        response.status = 400
        error = "Recipient does not exist."
    else:
        sender.debit_coins(payment_amount)
        recipient.credit_coins(payment_amount)
    return template(
        "profile",
        user=sender,
        session_user=sender,
        error=error,
    )

