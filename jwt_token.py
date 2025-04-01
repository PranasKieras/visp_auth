import jwt
import datetime

secret_key = 'your-secret-key'

def issue_token(full_name, personal_code, country):
    payload = {
        'full_name': full_name,
        'personal_code': personal_code,
        'country': country,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)
    }

    return jwt.encode(payload, secret_key, algorithm='HS256')

def extract_token_info(token):
    try:
        decoded_payload = jwt.decode(token, secret_key, algorithms=['HS256'])

        full_name = decoded_payload.get('full_name')
        personal_code = decoded_payload.get('personal_code')
        country = decoded_payload.get('country')
        return full_name, personal_code, country

    except jwt.ExpiredSignatureError:
        print("Token has expired")
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        print("Invalid token")
        raise Exception("Invalid token")

