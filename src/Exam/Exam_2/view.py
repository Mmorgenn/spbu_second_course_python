from tkinter import END, Text, Tk, ttk


class MainView(ttk.Frame):
    NEW_QUOTES = "Get new quotes"
    BEST_QUOTES = "Get best quotes"
    RANDOM_QUOTES = "Get random quotes"

    def __init__(self, root: Tk) -> None:
        super().__init__(root)

        self.button_new = ttk.Button(self, text=self.NEW_QUOTES)
        self.button_best = ttk.Button(self, text=self.BEST_QUOTES)
        self.button_random = ttk.Button(self, text=self.RANDOM_QUOTES)

        self.button_new.grid(row=0, column=0)
        self.button_best.grid(row=0, column=1)
        self.button_random.grid(row=0, column=2)

        self.text_label = Text(self, wrap="word", height=25)
        self.text_label.insert(END, "Choose quotes")
        self.text_label.grid(row=1, column=0, columnspan=3)

    def update_text(self, quotes: str) -> None:
        self.text_label.delete(1.0, END)
        self.text_label.insert(END, quotes)
