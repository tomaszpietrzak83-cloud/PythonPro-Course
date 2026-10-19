"""Exercise the real HTTP -> worker -> event stream path on either backend."""
import argparse
import http.cookiejar
import json
import time
import urllib.request
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["native", "docker"], default="native")
    parser.add_argument("--tasks", default=",".join(str(n) for n in range(1, 21)))
    args = parser.parse_args()
    jar = http.cookiejar.CookieJar()
    client = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    base = "http://127.0.0.1:8030"
    client.open(base).read()
    token = next(c.value for c in jar if c.name == "csrftoken")

    def request(path, data=None):
        body = None if data is None else json.dumps(data).encode()
        req = urllib.request.Request(base + path, data=body,
              headers={"Content-Type": "application/json", "X-CSRFToken": token})
        return json.load(client.open(req, timeout=30))

    course = request("/api/course")["lessons"]
    results = []
    for number in map(int, args.tasks.split(",")):
        key = request(f"/api/run/{number}", {
            "backend": args.backend, "input": course[number-1]["presets"][0]["value"]})["id"]
        deadline = time.monotonic() + 185
        while time.monotonic() < deadline:
            job = request(f"/api/status/{key}")
            if job["status"] != "running":
                break
            time.sleep(.2)
        assert job["status"] == "done", job
        metrics = {e["label"]: e["value"] for e in job["events"] if e["kind"] == "metric"}
        assert job["events"][0]["kind"] == "boot", job
        assert job["events"][-1]["kind"] == "done", job
        results.append({"task": number, "status": job["status"], "metrics": metrics})
        print(f"{args.backend} {number:02}: OK", flush=True)
    folder = Path(__file__).resolve().parent / ".runtime"
    folder.mkdir(exist_ok=True)
    report_path = folder / f"live-{args.backend}.json"
    prior = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else []
    merged = {r["task"]: r for r in prior}
    merged.update({r["task"]: r for r in results})
    report_path.write_text(json.dumps([merged[n] for n in sorted(merged)],
                                     ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
