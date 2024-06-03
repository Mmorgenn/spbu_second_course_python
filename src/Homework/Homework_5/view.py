from tkinter import ttk
from typing import Any


class MenuView(ttk.Frame):

    button_width = 20
    SINGLE_PLAYER = "Single Player"
    BOT_EASY = "Bot: Easy"
    BOT_HARD = "Bot: Hard"
    MULTIPLAYER = "Multiplayer"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.title_label = ttk.Label(self, text="Tic Tac Toe", font=("Arial", 72))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=40)

        self.button_single_player = ttk.Button(self, text=self.SINGLE_PLAYER, width=self.button_width)
        self.button_single_player.grid(row=1, column=0, columnspan=3, pady=20)

        self.button_bot_easy = ttk.Button(self, text=self.BOT_EASY, width=self.button_width)
        self.button_bot_easy.grid(row=2, column=0, columnspan=3, pady=20)

        self.button_bot_hard = ttk.Button(self, text=self.BOT_HARD, width=self.button_width)
        self.button_bot_hard.grid(row=3, column=0, columnspan=3, pady=20)

        self.button_multiplayer = ttk.Button(self, text=self.MULTIPLAYER, width=self.button_width)
        self.button_multiplayer.grid(row=4, column=0, columnspan=3, pady=20)


class FieldView(ttk.Frame):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)
        self.field_buttons = []

        for i in range(9):
            button = ttk.Button(self, text="")
            button.grid(row=i // 3, column=i % 3, sticky="NSEW")
            self.field_buttons.append(button)


class MultiplayerView(ttk.Frame):

    LABEL = ">Input Server-IP"
    BUTTON = "Entry"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.title_label = ttk.Label(self, text=self.LABEL, font=("Arial", 52))
        self.title_label.grid(row=0, column=1, columnspan=3, pady=100)

        self.ip_entry = ttk.Entry(self)
        self.ip_entry.grid(row=1, column=1, columnspan=3, pady=20)

        self.ip_button = ttk.Button(self, text=self.BUTTON)
        self.ip_button.grid(row=2, column=1, columnspan=3, pady=20)

    def _get_ip(self) -> str:
        return self.ip_entry.get()


class ChooseSideView(ttk.Frame):

    LABEL = "<Choose  Side>"
    SIDEX = "Side: X"
    SIDEO = "Side: O"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.title_label = ttk.Label(self, text=self.LABEL, font=("Arial", 52))
        self.title_label.grid(row=0, column=1, columnspan=3, pady=100)

        self.sideX_button = ttk.Button(self, text=self.SIDEX)
        self.sideX_button.grid(row=1, column=0, columnspan=3, pady=20)

        self.sideO_button = ttk.Button(self, text=self.SIDEO)
        self.sideO_button.grid(row=1, column=2, columnspan=3, pady=20)


class WinnerView(ttk.Frame):

    LABEL = "Congratulations!"
    NEW_GAME = "Restart"
    MENU = "Exit"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.title_label = ttk.Label(self, text=self.LABEL, font=("Arial", 52))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=100)

        self.result_label = ttk.Label(self, text="", font=("Arial", 24))
        self.result_label.grid(row=1, column=0, columnspan=3, pady=20)

        self.button_new_game = ttk.Button(self, text=self.NEW_GAME)

        self.button_menu = ttk.Button(self, text=self.MENU)
        self.button_menu.grid(row=3, column=0, columnspan=3, pady=20)
