import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from lab_support import event, launch, measured, metric, span


def analyze_sentiment(task):
    number, sentence = task
    rng = random.Random(number)
    with span(f"Review {number}", "simulated API"):
        # @step simulate
        time.sleep(rng.uniform(0.5, 2.0))
        result = rng.choice(["Positive", "Negative", "Neutral"])
        return sentence, result


def main(config):
    sentences = [
        "Good product",
        "Delivery was delayed",
        "An ordinary purchase",
        "I recommend it",
        "I do not recommend it",
    ] * 4
    worker_count = config.get("workers", 5)

    def run_analysis():
        results = []
        with ThreadPoolExecutor(max_workers=worker_count) as pool:
            # @step submit
            futures = [
                pool.submit(analyze_sentiment, task)
                for task in enumerate(sentences, 1)
            ]
            # @step complete
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                event("log", "Response", str(result))
        return results

    results = measured(f"Pool size: {worker_count}", run_analysis)
    metric("Analyzed reviews", len(results))


if __name__ == "__main__":
    launch(main)
