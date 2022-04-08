from flask import jsonify

class InvalidUsage(Exception):

    def __init__(self, message, status_code, payload=None):
        print("Status Code in", status_code)
        Exception.__init__(self)
        self.message = message


        if status_code is not None:
            self.status_code = status_code
        print("Status Code ",self.status_code)
        print("Payload ",payload)
        self.payload = payload
        print("After Payload ", payload)

    def to_dict(self):
        print("self Payload ", self.payload)
        rv = dict(self.payload or ())
        print("Before ",rv)
        rv['message'] = self.message
        print("RV " ,rv)
        return rv