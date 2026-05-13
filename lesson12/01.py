from dataclasses import dataclass


@dataclass
class Movie:
    title: str
    director: str
    yearOfRelease: int


movie1 = Movie("The Shawshank Redemption", "Frank Darabont", 1994)
movie2 = Movie("The Godfather", "Francis Ford Coppola", 1972)
print(movie1)
print(movie2)
