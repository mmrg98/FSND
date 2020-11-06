import json
from flask import request, _request_ctx_stack
from flask import Flask, request, jsonify, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


'''https://coffee-shop1.us.auth0.com/authorize?audience=coffee&response_type=token&client_id=6Jb422PzvZeQ2My3Guj2z6jFYPsZyOq4&redirect_uri=http://localhost:8100/tabs/user-page'''

'''logout: https://coffee-shop1.us.auth0.com/v2/logout?federated'''

'''Barista: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxqdjBqYUsyTFE1NXRlaVdWZzFmUyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS1zaG9wMS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhNGI4NjlhYzVkOTUwMDcxOTU2OGMyIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNjA0NjMxOTU3LCJleHAiOjE2MDQ3MTgzNTcsImF6cCI6IjZKYjQyMlB6dlplUTJNeTNHdWoyejZqRllQc1p5T3E0Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6ZHJpbmtzLWRldGFpbCJdfQ.bHRSu9oyyTZ_rbUyLtcGHYfJGU3LhezbMmRRd6gzjjDeGkrAEk5-WBKXi9jpvJF1pAPnmkfOv6QuqTLhz6-_acKeHkEWcO-31idPm4eYQWjXZtNHGlpIw7cjWzA6Trwx2EhXlazn1TW1BKrJ5THVB3UckTPlPdoLArykpt2eis6bIzSaE_U4K-997mkKlgVfccpJnw-B5j3rAAm23i8Y5xeeo56u43Dgj1f_6dkIz2X4IDAjsTdbPb3UAdacqGih1tjtEzjyXrbQR2stZtQsBPPhZRvOaYBaKE2Ly6Acf2ZzTahZ51BjwVfTGHtLs8inZafWlcEVO6Dg3O2eKSnWWA'''

'''Manager:eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxqdjBqYUsyTFE1NXRlaVdWZzFmUyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS1zaG9wMS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY5ODZkOTU3MDkyMDgwMDZlYTg5ZDIyIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNjA0NjMzODMxLCJleHAiOjE2MDQ3MjAyMzEsImF6cCI6IjZKYjQyMlB6dlplUTJNeTNHdWoyejZqRllQc1p5T3E0Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmNvZmZlZSIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpjb2ZmZWUiLCJwb3N0OmRyaW5rcyJdfQ.lyuJ1mSbY36OzZkrA8Fclly9ZLSYj_lSWLl6IOUH3WeErTMelZ8RxjlVo1qAfeIHhUYldlUCL8-3QfMEbOp9rQYaplhq2PYFkwjBHaAa_vFkltzXdXudXgOoCSWoDKEGWo1_-zy7b3H4uQT6ZUkbhwhzgJp_s66aoajlXPQFjIPx-FwwIUI7x0SoWqqRqOjfe0tXdISvpLOXKUJvcyG9Eox79tpFd8_wgbCfrIylCSzTpnXmbsbN1x-zvLtPvdJLcoYxO8A2fADl4BcAZFlQZJopzO8OIyfnrC96IhmWi6eoi5vTScx4OjSDFQTRS-Ckj6YmZYc3-TyFNB9Vxj-XaQ'''

AUTH0_DOMAIN = 'coffee-shop1.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)

    token= request.headers['Authorization'].split(" ")

    if len(token) != 2:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)
    elif token[0].lower() != 'bearer':
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)

    return token[1]


'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
        'code': 'invalid_claims',
        'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True
    raise Exception('Not Implemented')

'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            try:
                payload = verify_decode_jwt(jwt)
            except:
                abort(401)


            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
