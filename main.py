import requests
from bs4 import BeautifulSoup
from tkinter import Tk, PhotoImage, Canvas, Label, Button, messagebox
import random

# -------------------------------- CONSTANTS -----------------------------------------
HEADER_FONT_STYLE = ("Roboto", 20, "bold")
LABEL_FONT_STYLE = ("Roboto", 18)
BUTTON_FONT_STYLE = ("Roboto", 13, "bold")

BACKGROUND_COLOR = "#171717"
RED_ISH_COLOR = "#DA0037"
TEXT_COLOR = "white"

chosen_movie = None


# -------------------------------- FUNCTIONS -----------------------------------------
def pick_movie():
    global chosen_movie
    chosen_movie = random.choice(movies)
    button_pick_movie.config(text="Maybe...something else?")
    label_picked_movie.config(text=chosen_movie.encode("utf-8"), fg="#222222", wraplength=300)


def already_seen():
    movies.remove(chosen_movie)
    pick_movie()


def brb():
    movies.remove(chosen_movie)
    messagebox.showinfo(title="Great!", message=f'Enjoy watching "{chosen_movie}"!')
    window.destroy()


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


# --------------------------------- GUI SETUP -----------------------------------------
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
window.config(padx=70, width="600px", height="500px", bg=BACKGROUND_COLOR)
window.minsize(300, 470)

popcorn_image = PhotoImage(file="popcorn.png")
popcorn_image = popcorn_image.subsample(2, 2)
canvas = Canvas(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.create_image(100, 150, image=popcorn_image)
canvas.grid(column=0, row=1, rowspan=3)

header_label = Label(text="In need of a movie?", bg=RED_ISH_COLOR, font=HEADER_FONT_STYLE, fg=TEXT_COLOR,
                     padx=300, pady=10)
header_label.grid(column=0, row=0, columnspan=3, pady=50)

button_pick_movie = Button(text="⭐ Give me something good! ⭐", command=pick_movie, font=BUTTON_FONT_STYLE,
                           bg="#222222", fg="white", pady=10, width=42)
button_pick_movie.grid(column=1, row=1, columnspan=2)

label_picked_movie = Label(text="Movie title will be displayed here", font=LABEL_FONT_STYLE,
                           fg="#AAAAAA", width=30, height=3)
label_picked_movie.grid(column=1, row=2, columnspan=2)

button_brb = Button(text="BRB gonna watch it!", command=brb, bg=RED_ISH_COLOR, fg="white", padx=15, pady=10,
                    font=BUTTON_FONT_STYLE)
button_brb.grid(column=1, row=3)

button_already_seen = Button(text="I've already seen that..", command=already_seen, bg=RED_ISH_COLOR, fg="white",
                             padx=15, pady=10, font=BUTTON_FONT_STYLE)
button_already_seen.grid(column=2, row=3)

window.mainloop()

with open("movies.txt", mode="w") as file:
    for movie_title in movies:
        file.write(f"{movie_title}\n")