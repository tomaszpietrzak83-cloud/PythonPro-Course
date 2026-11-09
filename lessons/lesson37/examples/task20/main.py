import math


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm = math.sqrt(sum(x*x for x in a) * sum(y*y for y in b))
    return dot / norm if norm else 0.0


def recommend(query, titles, embed):
    query_vector, *vectors = embed([query, *titles])
    scores = [(cosine(query_vector, vector), title)
              for title, vector in zip(titles, vectors, strict=True)]
    return [title for score, title in sorted(scores, reverse=True)]


def demo(work):
    ranking = recommend("programming", ["Cooking", "Python"], lambda _: [[1, 0], [0, 1], [1, 0]])
    assert ranking == ["Python", "Cooking"]
    return {"ranking": ranking, "embedding_source": "fixture vectors"}
