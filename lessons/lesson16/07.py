def parser(url: str):
    protocol = url[: url.find("://")]

    cut_url = url.split("://")[1]

    if ":" in cut_url:
        domain = (cut_url)[: cut_url.find(":")]
        cut_url = cut_url.split(":")[1]
        port = (cut_url)[: cut_url.find("/")]
        cut_url = cut_url.split("/", maxsplit=1)[1]
        path = "/" + cut_url
    else:
        domain = (cut_url)[: cut_url.find("/")]
        path = "/" + cut_url.split("/", maxsplit=1)[1]
        if protocol == "http":
            port = "80"
        elif protocol == "https":
            port = "443"

    url_dictionary = {
        "protocol": protocol,
        "domain": domain,
        "port": port,
        "path": path,
    }
    return url_dictionary


link = "https://api.example.com:8080/users/search?active=true"
link2 = "https://api.example.com/users/search?active=true"
link3 = "http://api.example.com/users/search?active=true"

print(parser(link))
print(parser(link2))
print(parser(link3))
