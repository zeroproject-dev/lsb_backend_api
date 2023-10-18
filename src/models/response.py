from flask import jsonify


class Response():
    success: bool
    message: str

    @staticmethod
    def new(message: str, success=True, data=None):
        return jsonify(Response(success, message, data).to_json())

    def __init__(self, success, message, data) -> None:
        self.success = success
        self.message = message
        self.data = data

    def to_json(self):
        json = {}
        json['success'] = self.success
        json['message'] = self.message
        json['data'] = self.data
        return json
