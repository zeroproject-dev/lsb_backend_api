from jsonschema import validate

user_schema = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "second_name": {"type": "string"},
        "first_surname": {"type": "string"},
        "second_surname": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "role": {"type": "number"},
    },
    "required": ["first_name", "first_surname", "second_surname", "email", "role"],
}


def is_valid_json_user(json: dict | None):
    try:
        validate(instance=json, schema=user_schema)
        return True
    except Exception:
        return False
