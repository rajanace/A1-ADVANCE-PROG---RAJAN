import tkinter as tk
import random
import os


def load_jokes():
    jokes = []
    path = os.path.join("resources", "randomJokes.txt")
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "?" not in line:
                    continue
                left, right = line.split("?", 1)
                setup = left.strip() + "?"
                punch = right.strip()
                jokes.append((setup, punch))
    except FileNotFoundError:
        jokes = [
            ("Why did the chicken cross the road?", "To get to the other side."),
            ("What happens if you boil a clown?", "You get a laughing stock."),
            ("Why don’t scientists trust atoms?", "Because they make up everything."),
        ]
    return jokes


def main():
    jokes = load_jokes()
    current_setup = {"text": ""}
    current_punch = {"text": ""}

    root = tk.Tk()
    root.title("Exercise 2 - Alexa tell me a Joke")

    info = tk.Label(root, text="Type: Alexa tell me a Joke")
    info.pack(pady=8)

    entry = tk.Entry(root, width=35)
    entry.pack()

    setup_label = tk.Label(root, text="", wraplength=380, justify="left")
    setup_label.pack(pady=10)

    punch_label = tk.Label(root, text="", wraplength=380, justify="left", fg="blue")
    punch_label.pack()

    def ask(event=None):
        text = entry.get().strip().lower()
        if text == "alexa tell me a joke":
            setup, punch = random.choice(jokes)
            current_setup["text"] = setup
            current_punch["text"] = punch
            setup_label.config(text=setup)
            punch_label.config(text="")
            show_btn.config(state="normal")
        else:
            setup_label.config(text="Please type exactly: Alexa tell me a Joke")
            punch_label.config(text="")
            show_btn.config(state="disabled")

    def show_punch():
        if current_punch["text"]:
            punch_label.config(text=current_punch["text"])

    ask_btn = tk.Button(root, text="Ask", command=ask)
    ask_btn.pack(pady=4)

    show_btn = tk.Button(root, text="Show Punchline", command=show_punch, state="disabled")
    show_btn.pack(pady=4)

    entry.bind("<Return>", ask)
    entry.focus_set()

    root.mainloop()


if __name__ == "__main__":
    main()
