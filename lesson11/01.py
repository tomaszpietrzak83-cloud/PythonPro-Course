class Movie:
    def __init__(self, title, director, yearOfRelease):
        self.title = title
        self.director = director
        self.yearOfRelease = yearOfRelease

    def information(self):
        return f'"{self.title}" ({self.yearOfRelease}), directed by {self.director}'


video1 = Movie("Inception", "Christopher Nolan", 2010)
video2 = Movie("The Matrix", "The Wachowskis", 1999)
print(video1.information())
print(video2.information())
