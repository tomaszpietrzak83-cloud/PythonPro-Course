def validate_request(request_dict: dict):
    if "Host" not in request_dict["headers"]:
        raise ValueError("Missing required header 'Host'")

    if "User-Agent" not in request_dict["headers"]:
        raise ValueError("Missing required header 'User-Agent'")

    return {"code": 200, "body": "OK"}


request_data1 = {
    "method": "GET",
    "path": "/api/articles",
    "headers": {"Host": "my-blog.com", "User-Agent": "ok"},
}
try:
    validate_request(request_data1)
except ValueError as ve:
    print(ve)
request_data2 = {
    "method": "GET",
    "path": "/api/articles",
    "headers": {"User-Agent": "ok"},
}
try:
    validate_request(request_data2)
except ValueError as ve:
    print(ve)

request_data3 = {
    "method": "GET",
    "path": "/api/articles",
    "headers": {"Host": "my-blog.com"},
}
try:
    validate_request(request_data3)
except ValueError as ve:
    print(ve)
