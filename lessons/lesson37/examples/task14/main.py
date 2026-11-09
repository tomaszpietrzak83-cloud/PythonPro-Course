def summarize(values):
    return {"count": len(values), "total": sum(values)}


def demo(work):
    import json
    result = summarize([2, 3, 5])
    assert result == {"count": 3, "total": 10}
    (work / "report.json").write_text(json.dumps(result), encoding="utf-8")
    return result
