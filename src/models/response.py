from flask import jsonify


class Response():
    succ: bool
    message: str

    @staticmethod
    def new(message: str, success=True, data=None):
        return jsonify(Response(success, message, data).to_json())

    @staticmethod
    def success(message: str, data):
        return jsonify(Response(True, message, data).to_json())

    @staticmethod
    def fail(message: str):
        return jsonify(Response(False, message, None).to_json())

    def __init__(self, success, message, data) -> None:
        self.succ = success
        self.message = message
        self.data = data

    def to_json(self):
        json = {}
        json['success'] = self.succ
        json['message'] = self.message
        json['data'] = self.data
        return json
