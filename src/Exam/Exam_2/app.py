import asyncio
from tkinter import Tk

from src.Exam.Exam_2.model import BashQuotes
from src.Exam.Exam_2.viewmodel import MainViewModel


class App:
    APPLICATION_NAME = "QUOTES"
    START_SIZE = 700, 500

    def __init__(self) -> None:
        self._root = self._setup_root()
        self._model = BashQuotes()

    def _setup_root(self) -> Tk:
        root = Tk()
        root.geometry("x".join(map(str, self.START_SIZE)))
        root.title(self.APPLICATION_NAME)
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        return root

    async def update_frame(self) -> None:
        while True:
            self._root.update()
            await asyncio.sleep(0.1)

    async def start(self) -> None:
        viewmode = MainViewModel(self._model, asyncio.get_event_loop())
        viewmode.start(self._root)
        await self.update_frame()


if __name__ == "__main__":
    asyncio.run(App().start())
