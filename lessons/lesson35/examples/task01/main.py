import time

import requests


def check_service_health(urls):
    results = []
    for url in urls:
        started = time.perf_counter()
        try:
            response = requests.get(url, timeout=5)
            status = response.status_code
            error = None
        except requests.RequestException as exc:
            status, error = None, type(exc).__name__
        results.append(
            dict(
                url=url,
                status=status,
                ok=status == 200,
                seconds=round(time.perf_counter() - started, 4),
                error=error,
            )
        )
    return results


def demo(work, cloud):
    from demo_support import health_server

    with health_server() as base:
        return check_service_health(
            [base + "/ok", base + "/ready", base + "/unavailable"]
        )
