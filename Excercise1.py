import tkinter as tk
from tkinter import messagebox
import random

current_question = 0
score = 0
attempts_left = 2
difficulty = None
num_a = 0
num_b = 0
op = '+'


def displayMenu():
    clear_root()
    title = tk.Label(root, text="DIFFICULTY LEVEL", font=("Arial", 16))
    title.pack(pady=10)

    btn_easy = tk.Button(root, text="1. Easy", width=20, command=lambda: start_quiz("easy"))
    btn_easy.pack(pady=5)

    btn_mod = tk.Button(root, text="2. Moderate", width=20, command=lambda: start_quiz("moderate"))
    btn_mod.pack(pady=5)

    btn_adv = tk.Button(root, text="3. Advanced", width=20, command=lambda: start_quiz("advanced"))
    btn_adv.pack(pady=5)


def randomInt(level):
    if level == "easy":
        return random.randint(1, 9)
    elif level == "moderate":
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)


def decideOperation():
    return random.choice(['+', '-'])


def start_quiz(level):
    global difficulty, current_question, score
    difficulty = level
    current_question = 0
    score = 0
    next_question()


def displayProblem(a, b, operation):
    clear_root()

    info = tk.Label(root, text=f"Question {current_question + 1} of 10", font=("Arial", 12))
    info.pack(pady=5)

    problem_label.config(text=f"{a} {operation} {b} =")
    problem_label.pack(pady=10)

    answer_entry.delete(0, tk.END)
    answer_entry.pack(pady=5)

    feedback_label.config(text="")
    feedback_label.pack(pady=5)

    submit_btn.pack(pady=10)


def isCorrect(a, b, operation, user_answer):
    if operation == '+':
        correct = a + b
    else:
        correct = a - b
    return user_answer == correct, correct


def submit_answer():
    global attempts_left, score, current_question
    try:
        user_input = int(answer_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a whole number")
        return

    ok, correct_value = isCorrect(num_a, num_b, op, user_input)

    if ok:
        if attempts_left == 2:
            score += 10
            feedback_label.config(text="Correct! (+10)")
        else:
            score += 5
            feedback_label.config(text="Correct on second try (+5)")
        root.after(600, advance)
    else:
        attempts_left -= 1
        if attempts_left > 0:
            feedback_label.config(text="Not quite. Try once more!")
        else:
            feedback_label.config(text=f"Wrong. Correct answer was {correct_value}.")
            root.after(800, advance)


def advance():
    global attempts_left, current_question
    attempts_left = 2
    current_question += 1
    if current_question >= 10:
        displayResults()
    else:
        next_question()


def next_question():
    global num_a, num_b, op
    num_a = randomInt(difficulty)
    num_b = randomInt(difficulty)
    op = decideOperation()
    displayProblem(num_a, num_b, op)


def displayResults():
    clear_root()
    total = score
    grade = grade_for_score(total)

    end_title = tk.Label(root, text="Quiz Finished!", font=("Arial", 16))
    end_title.pack(pady=10)

    result = tk.Label(root, text=f"Your score: {total} / 100")
    result.pack(pady=5)

    grade_lbl = tk.Label(root, text=f"Grade: {grade}")
    grade_lbl.pack(pady=5)

    again_lbl = tk.Label(root, text="Play again?")
    again_lbl.pack(pady=10)

    btn_yes = tk.Button(root, text="Yes", width=12, command=displayMenu)
    btn_yes.pack(pady=5)

    btn_no = tk.Button(root, text="No", width=12, command=root.quit)
    btn_no.pack(pady=5)


def grade_for_score(points):
    if points >= 95:
        return "A+"
    elif points >= 90:
        return "A"
    elif points >= 80:
        return "B"
    elif points >= 70:
        return "C"
    elif points >= 60:
        return "D"
    else:
        return "F"


def clear_root():
    for w in root.winfo_children():
        if w not in persistent_widgets:
            w.pack_forget()


# Tkinter setup
root = tk.Tk()
root.title("Maths Quiz")
root.geometry("360x320")

# Re-usable widgets
problem_label = tk.Label(root, text="", font=("Arial", 14))
answer_entry = tk.Entry(root)
feedback_label = tk.Label(root, text="")
submit_btn = tk.Button(root, text="Submit Answer", command=submit_answer)

persistent_widgets = set()

displayMenu()
root.mainloop()


