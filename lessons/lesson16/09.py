class FakeServer:
    def __init__(self):

        self.db = {
            "users": [
                {
                    "1": {
                        "name": "Katarzyna",
                        "email": "k.nowak@example.com",
                        "city": "Warszawa",
                    }
                }
            ]
        }

    def handle_request(self, request_: dict, id):

        if request_["method"] == "PUT" and request_["target"] == "/users":
            user_key = str(id)
            for entry in self.db["users"]:
                if user_key in entry:
                    entry[user_key] = request_["body"]
                    break
            else:
                self.db["users"].append({user_key: request_["body"]})
            return {
                "code": 200,
                "body": "Replaced",
                "comment": self.db["users"],
            }

        elif request_["method"] == "PATCH" and request_["target"] == "/users":
            user_key = str(id)
            for entry in self.db["users"]:
                if user_key in entry:
                    entry[user_key].update(request_["body"])
                    break
            else:
                self.db["users"].append({user_key: request_["body"]})
            return {"code": 200, "body": "Updated", "comment": self.db["users"]}

        else:
            return {"code": 404, "body": "Not Found"}


class FakeClient:
    def __init__(self):
        pass

    def send(self, server_, request_, id):
        response = server_.handle_request(request_, id)
        print(response)


server = FakeServer()
client = FakeClient()

request_put = {
    "method": "PUT",
    "target": "/users",
    "body": {
        "name": "Kasia",
        "email": "k.nowak@example.com",
        "city": "Warszawa",
    },
}
request_patch = {
    "method": "PATCH",
    "target": "/users",
    "body": {
        "name": "Kasia",
    },
}
client.send(server, request_put, 1)
client.send(server, request_patch, 1)
