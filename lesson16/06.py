class HttpRequest:
    def __init__(
        self, method, target, headers: dict | None = None, body: str = "(empty)"
    ):
        self.method = method
        self.target = target
        if headers is None:
            headers = {}
        self.headers = headers
        self.body = body

    def display(self):
        headers_display = "\n"
        for key, value in self.headers.items():
            headers_display += f"\n{key}: {value}"
        print(f"""
--- HTTP Request ---
Method: {self.method}
Target: {self.target}
Headers:{headers_display}
Body:
{self.body}
--------------------
""")


req = HttpRequest(
    "POST",
    "/index.html",
    {"Host": "example.com", "User-Agent": "PythonClient/1.0"},
)
req.display()
