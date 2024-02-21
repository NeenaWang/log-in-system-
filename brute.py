from csv import reader
import hashlib

COMMON_PASSWORDS_PATH = 'common_passwords.txt'
SALTED_BREACH_PATH = "app/scripts/breaches/salted_breach.csv"

def load_breach(fp):
    with open(fp) as f:
        r = reader(f, delimiter=' ')
        header = next(r)
        assert(header[0] == 'username')
        return list(r)

def load_common_passwords():
    with open(COMMON_PASSWORDS_PATH) as f:
        pws = list(reader(f))
    return pws

def brute_force_attack(target_hash, target_salt):
    # TODO: return cracked password if one is found or None otherwise
    #pass
    common_passwords = load_common_passwords()
    salt_bytes = bytes.fromhex(target_salt)
    report_interval = 100
    print(len(common_passwords))

    for index, password in enumerate(common_passwords, start=1):
        password = password[0]
        hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt_bytes, 100000)
        hash_hex = hash.hex()

        if hash_hex == target_hash:
            return password

        if index % report_interval == 0:
            print(f"Checked {index} passwords...")

    return None

def main():
    salted_creds = load_breach(SALTED_BREACH_PATH)
    print(brute_force_attack(salted_creds[0][1], salted_creds[0][2]))
    print(brute_force_attack(salted_creds[1][1], salted_creds[1][2]))
    print(brute_force_attack(salted_creds[2][1], salted_creds[2][2]))



if __name__ == "__main__":
    main()
