import tkinter as tk
from tkinter import messagebox

# Questions for each level
EASY_QUESTIONS = [
    {"q": "Which is the closest star to Earth?", "a": ["Sun", "Moon"], "correct": "Sun"},
    {"q": "What is Earth's natural satellite?", "a": ["Mars", "Moon"], "correct": "Moon"},
    {"q": "What is the largest planet in our solar system?", "a": ["Jupiter", "Earth"], "correct": "Jupiter"},
    {"q": "Which planet in our solar system is called the red planet?", "a": ["Mars", "Venus"], "correct": "Mars"},
    {"q": "What is the fastest thing in the universe?", "a": ["Light", "Sound"], "correct": "Light"},
]
MEDIUM_QUESTIONS = [
    {"q": "What is the closest planet to the Sun?", "a": ["Mercury", "Venus"], "correct": "Mercury"},
    {"q": "Which planet has the most moons in our solar system?", "a": ["Jupiter", "Saturn"], "correct": "Saturn"},
    {"q": "What is the name of the first satellite launched into space?", "a": ["Sputnik 1", "Apollo 11"], "correct": "Sputnik 1"},
    {"q": "What is the largest volcano in our solar system?", "a": ["Olympus Mons", "Mauna Loa"], "correct": "Olympus Mons"},
    {"q": "What is the name of the planet known as the 'Evening Star'?", "a": ["Venus", "Mars"], "correct": "Venus"},
]
HARD_QUESTIONS = [
    {"q": "What is the process by which a star collapses under its own gravity after exhausting its nuclear fuel?", "a": ["Supernova", "Nebula"], "correct": "Supernova"},
    {"q": "What is the name of the force that opposes the gravitational collapse of massive objects, such as stars?", "a": ["Nuclear Fusion", "Gravity"], "correct": "Nuclear Fusion"},
    {"q": "What is the term for the hypothetical boundary around a black hole beyond which nothing can escape its gravitational pull?", "a": ["Event Horizon", "Singularity"], "correct": "Event Horizon"},
    {"q": "What is the name of the process by which a star collapses to a point of infinite density and zero volume?", "a": ["Singularity", "Supernova"], "correct": "Singularity"},
    {"q": "What is the name of the hypothetical substance that is thought to constitute approximately 85% of the matter in the universe, but cannot be directly detected?", "a": ["Dark Matter", "Antimatter"], "correct": "Dark Matter"},
]

class AstroQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Astroventure Quiz Game")
        self.score = 0
        self.level = None
        self.q_index = 0
        self.attempts = 0
        self.questions = []
        self.setup_main_menu()

    def setup_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome to ASTROVENTURE!", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(self.root, text="Select your level:", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Easy", width=15, command=lambda: self.start_level("easy")).pack(pady=5)
        tk.Button(self.root, text="Medium", width=15, command=lambda: self.start_level("medium")).pack(pady=5)
        tk.Button(self.root, text="Hard", width=15, command=lambda: self.start_level("hard")).pack(pady=5)

    def start_level(self, level):
        self.level = level
        self.score = 0
        self.q_index = 0
        self.attempts = 0
        if level == "easy":
            self.questions = EASY_QUESTIONS
        elif level == "medium":
            self.questions = MEDIUM_QUESTIONS
        else:
            self.questions = HARD_QUESTIONS
        self.show_question()

    def show_question(self):
        self.clear_window()
        if self.q_index >= len(self.questions):
            self.show_result()
            return
        q = self.questions[self.q_index]
        tk.Label(self.root, text=f"Level: {self.level.title()} | Score: {self.score}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.root, text=f"Question {self.q_index+1}:", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.root, text=q["q"], font=("Arial", 13)).pack(pady=10)
        for ans in q["a"]:
            tk.Button(self.root, text=ans, width=20, font=("Arial", 12), command=lambda a=ans: self.check_answer(a)).pack(pady=5)
        self.feedback_label = tk.Label(self.root, text="", font=("Arial", 12), fg="red")
        self.feedback_label.pack(pady=10)

    def check_answer(self, answer):
        q = self.questions[self.q_index]
        correct = q["correct"].lower()
        if answer.lower() == correct:
            self.score += 1
            self.feedback_label.config(text="Correct!", fg="green")
            self.root.after(800, self.next_question)
        else:
            self.attempts += 1
            max_attempts = 3 if self.q_index == 4 else 2
            if self.attempts < max_attempts:
                self.feedback_label.config(text=f"Incorrect! Try again. ({self.attempts}/{max_attempts})", fg="red")
            else:
                self.feedback_label.config(text=f"Out of attempts! The correct answer was: {q['correct']}", fg="orange")
                self.root.after(1200, self.next_question)

    def next_question(self):
        self.q_index += 1
        self.attempts = 0
        self.show_question()

    def show_result(self):
        self.clear_window()
        tk.Label(self.root, text=f"Level Complete!", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self.root, text=f"Your Score: {self.score} / {len(self.questions)}", font=("Arial", 15)).pack(pady=10)
        if self.score == len(self.questions):
            msg = "You were incredible! You got every question right! You're a quiz champion!!"
        elif self.score >= len(self.questions) - 1:
            msg = "Great job! You're almost a quiz champion!"
        elif self.score >= 2:
            msg = "Good effort! Keep learning and challenging yourself!"
        else:
            msg = "Don't worry, you can always try again and improve your knowledge!"
        tk.Label(self.root, text=msg, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Play Again", width=15, command=self.setup_main_menu).pack(pady=5)
        tk.Button(self.root, text="Exit", width=15, command=self.root.quit).pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x400")
    app = AstroQuiz(root)
    root.mainloop()
