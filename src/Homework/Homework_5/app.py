from tkinter import Tk

from src.Homework.Homework_5.model import TicTacToeModel
from src.Homework.Homework_5.viewmodel import ViewModel


class App:
    APPLICATION_NAME = "TicTacToe"
    START_SIZE = 512, 512

    def __init__(self) -> None:
        self._root = self._setup_root()
        self._model = TicTacToeModel()
        self._viewmodel = ViewModel(self._root, self._model)

    def _setup_root(self) -> Tk:
        root = Tk()
        root.geometry("x".join(map(str, self.START_SIZE)))
        root.title(self.APPLICATION_NAME)
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        return root

    def start(self) -> None:
        self._viewmodel.start()
        self._root.mainloop()


if __name__ == "__main__":
    App().start()
