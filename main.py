import requests
from bs4 import BeautifulSoup
from tkinter import *

# -------------------------------- CONSTANTS -----------------------------------------
BACKGROUND_COLOR = "#F48660"
FONT_STYLE = ("Arial", 26, "bold")
TEXT_COLOR = "#ECE2D0"


# -------------------------------- FUNCTIONS -----------------------------------------
def pick_movie():
    pass


# -------------------------------- WEB SCRAPING --------------------------------------
def empire_scraping():
    response = requests.get(
        url="https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features"
            "/best-movies-2/")
    response.raise_for_status()
    empire_website = response.text

    soup = BeautifulSoup(empire_website, "html.parser")
    movie_tags = soup.find_all(name="h3", class_="title")
    movie_titles = [tag.get_text().strip("1234567890) ") for tag in movie_tags]

    with open(file="movies.txt", mode="w", encoding="utf-8") as movie_file:
        for movie_title in movie_titles:
            movie_file.write(f"{movie_title}\n")


# --------------------------------- GUI SET ------------------------------------------
movies = []

try:
    with open(file="movies.txt", mode="r") as file:
        content = file.readlines()
except FileNotFoundError:
    empire_scraping()
else:
    for title in content:
        movies.append(title.strip())

window = Tk()
window.title("100 Movies You Must Watch")
window.config(padx=70, pady=50, width="600px", height="300px", bg=BACKGROUND_COLOR)

popcorn_image = PhotoImage(file="popcorn.png")
popcorn_image = popcorn_image.subsample(2, 2)
canvas = Canvas(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.create_image(100, 150, image=popcorn_image)
canvas.grid(column=0, row=0, rowspan=3)

header_label = Label(text="In need of a movie?", bg=TEXT_COLOR, font=FONT_STYLE, fg="black", padx=15, pady=15)
header_label.grid(column=1, row=0)

button_pick_movie = Button(text="Give me something good!", command=pick_movie)

window.mainloop()
