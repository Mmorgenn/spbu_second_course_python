import abc
import asyncio
from tkinter import Tk, ttk

from src.Exam.Exam_2.model import BashQuotes
from src.Exam.Exam_2.view import MainView


class IViewModel(metaclass=abc.ABCMeta):

    def __init__(self, model: BashQuotes, loop: asyncio.AbstractEventLoop) -> None:
        self._model = model
        self._loop = loop

    @abc.abstractmethod
    def start(self, root: Tk) -> ttk.Frame:
        raise NotImplementedError


class MainViewModel(IViewModel):

    def _bind(self, view: MainView) -> None:
        view.button_new.config(command=lambda: self._loop.create_task(self.update_quote(view, "new")))
        view.button_best.config(command=lambda: self._loop.create_task(self.update_quote(view, "best")))
        view.button_random.config(command=lambda: self._loop.create_task(self.update_quote(view, "random")))

    async def update_quote(self, view: MainView, type_quote: str) -> None:
        result = await self._model.get_quote(type_quote)
        view.update_text(result)

    def start(self, root: Tk) -> MainView:
        frame = MainView(root)
        self._bind(frame)
        frame.pack()
        return frame
