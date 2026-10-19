TITLES = [
    ("Pierwsze zadanie", "First task"),
    ("Mnożenie liczb", "Multiply numbers"),
    ("Zapis czasu", "Log timestamp"),
    ("Pierwszy harmonogram", "First schedule"),
    ("Liczenie użytkowników", "Count users"),
    ("Harmonogram crontab", "Crontab schedule"),
    ("Aktualizacja logowania", "Update login"),
    ("Przetwarzanie wideo", "Process video"),
    ("Masowe zadania", "Batch tasks"),
    ("Powiadomienie mailowe", "Email notification"),
    ("Śledzenie postępu", "Track progress"),
    ("Czyszczenie logów", "Clean logs"),
    ("Scraping strony", "Page scraping"),
    ("Raport CSV", "CSV report"),
    ("Ponawianie zadań", "Retry tasks"),
    ("Klasyfikacja obrazu", "Image classification"),
    ("Łańcuch zadań", "Task chain"),
    ("Oddzielne kolejki", "Separate queues"),
    ("Monitorowanie Flower", "Flower monitoring"),
    ("Transakcje bazodanowe", "Database transactions"),
]


def task_catalog():
    return [
        {
            "number": index,
            "label": f"{index:02}",
            "pl": pl,
            "en": en,
            "available": True,
        }
        for index, (pl, en) in enumerate(TITLES, 1)
    ]
