from csv import reader

from app.models.breaches import (
    create_plaintext_breach_entry,
    create_hashed_breach_entry,
    create_salted_breach_entry,
)

PLAINTEXT_BREACH_PATH = "app/scripts/breaches/plaintext_breach.csv"
HASHED_BREACH_PATH = "app/scripts/breaches/hashed_breach.csv"
SALTED_BREACH_PATH = "app/scripts/breaches/salted_breach.csv"

def load_breaches(db):
    with open(PLAINTEXT_BREACH_PATH) as f:
        r = reader(f, delimiter=' ')
        header = next(r)
        assert(header[0] == 'username')
        for creds in r:
            create_plaintext_breach_entry(db, creds[0], creds[1])

    # TODO: Add logic for other types of breaches
    with open(HASHED_BREACH_PATH) as f:
        r = reader(f, delimiter=' ')
        header = next(r)
        assert(header[0] == 'username')
        for username, hashed_password in r:
            create_hashed_breach_entry(db, username, hashed_password)

    with open(SALTED_BREACH_PATH) as f:
        r = reader(f, delimiter=' ')
        header = next(r)
        assert(header[0] == 'username')
        for username, salted_password, salt in r:
            create_salted_breach_entry(db, username, salted_password, salt)



