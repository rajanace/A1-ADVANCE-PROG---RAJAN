import tkinter as tk
from tkinter import messagebox
import os


# Beginner-friendly extended version: simple data structures and small functions
students = []  # list of dicts: {code, name, c1, c2, c3, exam}


def file_path():
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, "resources", "studentMarks.txt")


def load_students():
    global students
    students = []
    path = file_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        if not lines:
            messagebox.showerror("Error", "studentMarks.txt is empty")
            return
        try:
            expected = int(lines[0])
        except ValueError:
            messagebox.showerror("Error", "First line must be number of students")
            return
        for line in lines[1:]:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 6:
                continue
            try:
                code = int(parts[0])
                name = parts[1]
                c1 = int(parts[2])
                c2 = int(parts[3])
                c3 = int(parts[4])
                exam = int(parts[5])
            except ValueError:
                continue
            students.append({"code": code, "name": name, "c1": c1, "c2": c2, "c3": c3, "exam": exam})
        if expected != len(students):
            messagebox.showinfo("Note", f"Expected {expected} students, loaded {len(students)}.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Could not find resources/studentMarks.txt")


def save_students():
    path = file_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(len(students)) + "\n")
            for s in students:
                line = f"{s['code']},{s['name']},{s['c1']},{s['c2']},{s['c3']},{s['exam']}\n"
                f.write(line)
        messagebox.showinfo("Saved", "Changes saved to studentMarks.txt")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file: {e}")


def coursework_total(s):
    return s["c1"] + s["c2"] + s["c3"]


def overall_total(s):
    return coursework_total(s) + s["exam"]


def percentage(s):
    return round((overall_total(s) / 160) * 100, 2)


def grade_for(pct):
    if pct >= 70:
        return "A"
    elif pct >= 60:
        return "B"
    elif pct >= 50:
        return "C"
    elif pct >= 40:
        return "D"
    else:
        return "F"


def format_student(s):
    cwt = coursework_total(s)
    pct = percentage(s)
    grd = grade_for(pct)
    return (
        f"Name: {s['name']}\n"
        f"Number: {s['code']}\n"
        f"Coursework Total: {cwt} / 60\n"
        f"Exam Mark: {s['exam']} / 100\n"
        f"Overall %: {pct}%\n"
        f"Grade: {grd}\n"
    )


def show_all():
    output.delete("1.0", tk.END)
    if not students:
        output.insert(tk.END, "No student data loaded.\n")
        return
    total_pct = 0.0
    for s in students:
        output.insert(tk.END, format_student(s))
        output.insert(tk.END, "------------------------------\n")
        total_pct += percentage(s)
    avg = round(total_pct / len(students), 2)
    output.insert(tk.END, f"Students: {len(students)}\nAverage %: {avg}%\n")


def show_selected_student(sel_index):
    if sel_index is None:
        messagebox.showerror("Error", "Please select a student")
        return
    s = students[sel_index]
    output.delete("1.0", tk.END)
    output.insert(tk.END, format_student(s))


def open_select_window(action_name, on_pick):
    if not students:
        messagebox.showerror("Error", "No student data loaded")
        return
    win = tk.Toplevel(root)
    win.title(action_name)
    win.geometry("380x340")

    tk.Label(win, text="Pick a student then click Continue").pack(pady=6)
    lb = tk.Listbox(win, width=44, height=12)
    lb.pack(pady=6)
    for idx, s in enumerate(students):
        lb.insert(tk.END, f"{idx+1}. {s['name']} ({s['code']})")

    def go():
        sel = lb.curselection()
        if not sel:
            messagebox.showerror("Error", "Please select a student")
            return
        i = sel[0]
        win.destroy()
        on_pick(i)

    tk.Button(win, text="Continue", command=go).pack(pady=6)


def show_one():
    def picked(i):
        show_selected_student(i)
    open_select_window("View One", picked)


def show_highest():
    output.delete("1.0", tk.END)
    if not students:
        output.insert(tk.END, "No student data loaded.\n")
        return
    best = students[0]
    for s in students[1:]:
        if overall_total(s) > overall_total(best):
            best = s
    output.insert(tk.END, format_student(best))


def show_lowest():
    output.delete("1.0", tk.END)
    if not students:
        output.insert(tk.END, "No student data loaded.\n")
        return
    worst = students[0]
    for s in students[1:]:
        if overall_total(s) < overall_total(worst):
            worst = s
    output.insert(tk.END, format_student(worst))


def sort_records(ascending=True):
    if not students:
        messagebox.showerror("Error", "No student data loaded")
        return
    # simple bubble sort (beginner-friendly)
    n = len(students)
    for i in range(n):
        for j in range(0, n - i - 1):
            left = overall_total(students[j])
            right = overall_total(students[j + 1])
            need_swap = left > right if ascending else left < right
            if need_swap:
                students[j], students[j + 1] = students[j + 1], students[j]
    show_all()


def open_add_window():
    win = tk.Toplevel(root)
    win.title("Add Student")
    win.geometry("360x360")

    labels = ["Code (1000-9999)", "Name", "Course 1 (0-20)", "Course 2 (0-20)", "Course 3 (0-20)", "Exam (0-100)"]
    entries = []
    for i, text in enumerate(labels):
        tk.Label(win, text=text).grid(row=i, column=0, padx=6, pady=6, sticky="w")
        e = tk.Entry(win, width=24)
        e.grid(row=i, column=1, padx=6, pady=6)
        entries.append(e)

    def add_now():
        try:
            code = int(entries[0].get())
            name = entries[1].get().strip()
            c1 = int(entries[2].get())
            c2 = int(entries[3].get())
            c3 = int(entries[4].get())
            exam = int(entries[5].get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
            return
        if not (1000 <= code <= 9999):
            messagebox.showerror("Error", "Code must be between 1000 and 9999")
            return
        if name == "":
            messagebox.showerror("Error", "Name cannot be empty")
            return
        for mark in [c1, c2, c3]:
            if not (0 <= mark <= 20):
                messagebox.showerror("Error", "Course marks must be 0-20")
                return
        if not (0 <= exam <= 100):
            messagebox.showerror("Error", "Exam must be 0-100")
            return
        # ensure unique code (simple check)
        for s in students:
            if s["code"] == code:
                messagebox.showerror("Error", "A student with this code already exists")
                return
        students.append({"code": code, "name": name, "c1": c1, "c2": c2, "c3": c3, "exam": exam})
        win.destroy()
        show_all()

    tk.Button(win, text="Add", width=12, command=add_now).grid(row=len(labels), column=0, columnspan=2, pady=10)


def open_delete_window():
    def picked(i):
        s = students[i]
        ok = messagebox.askyesno("Delete", f"Delete {s['name']} ({s['code']})?")
        if ok:
            del students[i]
            show_all()
    open_select_window("Delete Student", picked)


def open_update_window():
    def picked(i):
        s = students[i]
        win = tk.Toplevel(root)
        win.title("Update Student")
        win.geometry("360x360")

        labels = ["Code (1000-9999)", "Name", "Course 1 (0-20)", "Course 2 (0-20)", "Course 3 (0-20)", "Exam (0-100)"]
        values = [str(s["code"]), s["name"], str(s["c1"]), str(s["c2"]), str(s["c3"]), str(s["exam"])]
        entries = []
        for idx, text in enumerate(labels):
            tk.Label(win, text=text).grid(row=idx, column=0, padx=6, pady=6, sticky="w")
            e = tk.Entry(win, width=24)
            e.grid(row=idx, column=1, padx=6, pady=6)
            e.insert(0, values[idx])
            entries.append(e)

        def update_now():
            try:
                code = int(entries[0].get())
                name = entries[1].get().strip()
                c1 = int(entries[2].get())
                c2 = int(entries[3].get())
                c3 = int(entries[4].get())
                exam = int(entries[5].get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
                return
            if not (1000 <= code <= 9999):
                messagebox.showerror("Error", "Code must be between 1000 and 9999")
                return
            if name == "":
                messagebox.showerror("Error", "Name cannot be empty")
                return
            for mark in [c1, c2, c3]:
                if not (0 <= mark <= 20):
                    messagebox.showerror("Error", "Course marks must be 0-20")
                    return
            if not (0 <= exam <= 100):
                messagebox.showerror("Error", "Exam must be 0-100")
                return
            # if code was changed, ensure not colliding with other students
            for idx2, other in enumerate(students):
                if idx2 != i and other["code"] == code:
                    messagebox.showerror("Error", "Another student has this code")
                    return
            students[i] = {"code": code, "name": name, "c1": c1, "c2": c2, "c3": c3, "exam": exam}
            win.destroy()
            show_all()

        tk.Button(win, text="Update", width=12, command=update_now).grid(row=len(labels), column=0, columnspan=2, pady=10)

    open_select_window("Update Student", picked)


def on_load_click():
    load_students()
    if students:
        messagebox.showinfo("Loaded", f"Loaded {len(students)} students")


def on_save_click():
    if not students:
        messagebox.showerror("Error", "No student data to save")
        return
    save_students()


# Tkinter UI
root = tk.Tk()
root.title("Exercise 3 Extended - Student Manager")
root.geometry("720x560")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=8)

tk.Button(btn_frame, text="Load File", width=14, command=on_load_click).grid(row=0, column=0, padx=4, pady=4)
tk.Button(btn_frame, text="Save File", width=14, command=on_save_click).grid(row=0, column=1, padx=4, pady=4)

tk.Button(btn_frame, text="1. View All", width=14, command=show_all).grid(row=0, column=2, padx=4, pady=4)
tk.Button(btn_frame, text="2. View One", width=14, command=show_one).grid(row=0, column=3, padx=4, pady=4)
tk.Button(btn_frame, text="3. Highest", width=14, command=show_highest).grid(row=1, column=0, padx=4, pady=4)
tk.Button(btn_frame, text="4. Lowest", width=14, command=show_lowest).grid(row=1, column=1, padx=4, pady=4)

tk.Button(btn_frame, text="5. Sort Asc", width=14, command=lambda: sort_records(True)).grid(row=1, column=2, padx=4, pady=4)
tk.Button(btn_frame, text="5. Sort Desc", width=14, command=lambda: sort_records(False)).grid(row=1, column=3, padx=4, pady=4)

tk.Button(btn_frame, text="6. Add", width=14, command=open_add_window).grid(row=2, column=0, padx=4, pady=4)
tk.Button(btn_frame, text="7. Delete", width=14, command=open_delete_window).grid(row=2, column=1, padx=4, pady=4)
tk.Button(btn_frame, text="8. Update", width=14, command=open_update_window).grid(row=2, column=2, padx=4, pady=4)
tk.Button(btn_frame, text="Quit", width=14, command=root.quit).grid(row=2, column=3, padx=4, pady=4)

output = tk.Text(root, width=90, height=28)
output.pack(pady=8)

root.mainloop()


