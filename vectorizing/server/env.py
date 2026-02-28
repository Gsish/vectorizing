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
    missing_keys = [
        key for key in REQUIRED_ENVIRONMENT_VARIABLES
        if key not in os.environ
    ]

    invalid_types = []
    for key, cast in REQUIRED_ENVIRONMENT_VARIABLES.items():
        if key in os.environ:
            try:
                cast(os.environ[key])
            except ValueError:
                invalid_types.append(key)

    if missing_keys or invalid_types:
        err_msg = ""
        if missing_keys:
            err_msg += f"Missing variables: {', '.join(missing_keys)}. "
        if invalid_types:
            err_msg += f"Invalid types for: {', '.join(invalid_types)}. "
        raise VariableNotDefinedException(err_msg)

    return [
        cast(os.environ[key])
        for key, cast in REQUIRED_ENVIRONMENT_VARIABLES.items()
    ]

def get_optional():
    return [
        cast(os.environ[key]) if key in os.environ else None
        for key, cast in OPTIONAL_ENVIRONMENT_VARIABLES.items()
    ]
