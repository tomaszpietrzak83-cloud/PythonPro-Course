class FakeServer:
    def __init__(self):

        self.db = {
            "users": [{"id": 1, "name": "Jan"}, {"id": 2, "name": "Anna"}]
        }

    def handle_request(self, request_: dict):
        if request_["method"] == "GET" and request_["target"] == "/users":
            return {"code": 200, "body": self.db["users"]}

        elif request_["method"] == "POST" and request_["target"] == "/users":
            self.db["users"].append(request_["body"])
            return {"code": 201, "body": "Created"}

        else:
            return {"code": 404, "body": "Not Found"}


class FakeClient:
    def __init__(self):
        pass

    def send(self, server_, request_):
        response = server_.handle_request(request_)
        print(response)


server = FakeServer()
client = FakeClient()

request1 = {"method": "GET", "target": "/users"}

client.send(server, request1)

request2 = {
    "method": "POST",
    "target": "/users",
    "body": {"id": 3, "name": "Tom"},
}

client.send(server, request2)
client.send(server, request1)

request3 = {"method": "GET", "target": "/users/id3"}
client.send(server, request3)
