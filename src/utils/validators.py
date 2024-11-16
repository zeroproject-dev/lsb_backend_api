from jsonschema import validate


login_schema = {
    "type": "object",
    "properties": {"email": {"type": "string"}, "password": {"type": "string"}},
    "required": ["email", "password"],
}


def is_valid_json_login(json):
    try:
        validate(instance=json, schema=login_schema)
        return True
    except Exception:
        return False


role_schema = {
    "type": "object",
    "properties": {"name": {"type": "string"}, "description": {"type": "string"}},
    "required": ["name"],
}


def is_valid_json_role(json):
    try:
        validate(instance=json, schema=role_schema)
        return True
    except Exception:
        return False


word_schema = {
    "type": "object",
    "properties": {
        "word": {"type": "string"},
    },
    "required": ["word"],
}


def is_valid_json_word(json):
    try:
        validate(instance=json, schema=word_schema)
        return True
    except Exception:
        return False
