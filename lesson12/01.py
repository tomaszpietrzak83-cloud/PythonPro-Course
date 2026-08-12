from dataclasses import dataclass


@dataclass
class Movie:
    title: str
    director: str
    yearOfRelease: int
    additionalInfo: str = "No additional information"

    def __str__(self):
        return f"""
            {self.title} ({self.yearOfRelease}), directed by {self.director}.
            {self.additionalInfo}
            """


movie1 = Movie(
    "The Shawshank Redemption",
    "Frank Darabont",
    1994,
    "Great movie about hope and friendship.",
)
movie2 = Movie(
    "The Godfather", "Francis Ford Coppola", 1972, "Classic crime drama."
)
print(movie1)
print(movie2)
