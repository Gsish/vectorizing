import os

REQUIRED_ENVIRONMENT_VARIABLES = {
    'PORT': int,
    'DATABASE_URL': str,
    'R2_ACCOUNT_ID': str,
    'R2_ACCESS_KEY_ID': str,
    'R2_SECRET_ACCESS_KEY': str,
    'R2_BUCKET_NAME': str,
    'R2_PUBLIC_DOMAIN': str,
}

OPTIONAL_ENVIRONMENT_VARIABLES = {
    'SENTRY_DSN': str,
}

class VariableNotDefinedException(Exception):
    pass

def get_required():
    missing_required = any([
        not key in os.environ
        for key in REQUIRED_ENVIRONMENT_VARIABLES
    ])

    if missing_required:
        raise VariableNotDefinedException()

    return [
        cast(os.environ[key])
        for key, cast in REQUIRED_ENVIRONMENT_VARIABLES.items()
    ]

def get_optional():
    return [
        cast(os.environ[key]) if key in os.environ else None
        for key, cast in OPTIONAL_ENVIRONMENT_VARIABLES.items()
    ]
