import tkinter as tk
import random
import time
import string
import os


class TypingTestApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gyorsíró Teszt")

        self.target_text = ""
        self.start_time = None
        self.best_time = self.load_best_time()

        self.label_target = tk.Label(self.root, text="", font=("Times New Roman", 16))
        self.label_target.pack(pady=10)

        self.entry_text = tk.Entry(self.root, font=("Times New Roman", 16))
        self.entry_text.pack(pady=10)
        self.entry_text.bind("<KeyRelease>", self.check_input)

        self.label_feedback = tk.Label(self.root, text="", font=("Times New Roman", 14))
        self.label_feedback.pack(pady=5)

        self.button_start = tk.Button(self.root, text="Kezdés", font=("Times New Roman", 14), command=self.start_test)
        self.button_start.pack(pady=10)

        self.label_result = tk.Label(self.root, text="", font=("Times New Roman", 14))
        self.label_result.pack(pady=10)

        self.button_retry = tk.Button(self.root, text="Új teszt", font=("Times New Roman", 14), command=self.reset_test, state=tk.DISABLED)
        self.button_retry.pack(pady=10)

        self.label_best_time = tk.Label(self.root, text="Legjobb idő: -", font=("Times New Roman", 14))
        self.label_best_time.pack(pady=10)
        self.update_best_time_label()

    def run(self):
        self.root.mainloop()

    def generate_random_text(self, length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def start_test(self):
        self.target_text = self.generate_random_text()
        self.label_target.config(text="Cél: " + self.target_text)
        self.entry_text.delete(0, tk.END)
        self.entry_text.config(state=tk.NORMAL)
        self.start_time = time.time()
        self.label_feedback.config(text="", fg="black")
        self.label_result.config(text="")
        self.button_retry.config(state=tk.DISABLED)
        self.button_start.config(state=tk.DISABLED)
        self.entry_text.focus()

    def check_input(self, event):
        current_text = self.entry_text.get()

        if current_text == self.target_text:
            elapsed_time = time.time() - self.start_time
            self.entry_text.delete(0, tk.END)
            self.label_feedback.config(text="Helyes!", fg="green")
            self.label_result.config(text=f"Eredmény: {elapsed_time:.2f} másodperc")
            self.entry_text.config(state=tk.DISABLED)
            self.button_start.config(state=tk.NORMAL)
            self.button_retry.config(state=tk.NORMAL)

            if self.best_time is None or elapsed_time < self.best_time:
                self.best_time = elapsed_time
                self.save_best_time(elapsed_time)
                self.update_best_time_label()

        elif self.target_text.startswith(current_text):
            self.label_feedback.config(text="Folytasd...", fg="black")
        else:
            self.label_feedback.config(text="Hibás karakter!", fg="red")

    def reset_test(self):
        self.start_test()

    def update_best_time_label(self):
        if self.best_time is not None:
            self.label_best_time.config(text=f"Legjobb idő: {self.best_time:.2f} másodperc")
        else:
            self.label_best_time.config(text="Legjobb idő: -")

    def load_best_time(self):
        if os.path.exists("best_time.txt"):
            with open("best_time.txt", "r") as file:
                try:
                    return float(file.read().strip())
                except ValueError:
                    return None
        return None

    def save_best_time(self, best_time):
        with open("best_time.txt", "w") as file:
            file.write(f"{best_time:.2f}")
