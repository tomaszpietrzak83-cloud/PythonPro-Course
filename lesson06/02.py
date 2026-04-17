def bookDescription(title, author, releaseYear):
    description = (
        f"Book '{title}', has been written by {author}, and released in {releaseYear}."
    )
    return description


exampleTitle = "Dune"
exampleAuthor = "Frank Herbert"
exampleReleaseYear = 1965

print(bookDescription(exampleTitle, exampleAuthor, exampleReleaseYear))
