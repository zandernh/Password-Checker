import requests
import hashlib


def request_api_data(query_hash):
    url = 'https://api.pwnedpasswords.com/range/' + query_hash
    request_response = requests.get(url)
    if request_response.status_code != 200:
        raise RuntimeError(f"Error fetching: {request_response.status_code}, check the API and try again.")
    return request_response


def get_password_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def password_hash_api_check(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_hash, tail_hash = sha1_password[:5], sha1_password[5:]
    response_hash = request_api_data(first5_hash)
    return get_password_count(response_hash, tail_hash)


def execute_password_check(args):
    for password in args:
        count = password_hash_api_check(password)
        if count:
            print(f"\nThe password, {password}, was found {count} times in the repository.\nConsider changing your password.\n")
        else:
            print(f"The password, {password}, was NOT found in the repository.\nConsider yourself good to go!")
    return '\nTask Complete\n'


if __name__ == "__main__":
    with open('passwords.txt', "r") as file:
        for line_in_file in file:
            password_to_check = line_in_file.split()
            execute_password_check(password_to_check)
