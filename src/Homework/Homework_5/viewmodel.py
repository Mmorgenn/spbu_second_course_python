from functools import partial
from threading import Thread
from time import sleep
from tkinter import Tk
from typing import Callable

from src.Homework.Homework_5.model import *
from src.Homework.Homework_5.view import *


class ViewModel:
    def __init__(self, root: Tk, model: TicTacToeModel) -> None:
        self._root = root
        self._model = model
        self._viewmodels = {
            "menu": MenuViewModel(self._model),
            "multiplayer": MultiplayerViewModel(self._model),
            "choose": ChooseSideViewModel(self._model),
            "field": FieldViewModel(self._model),
            "winner": WinnerViewModel(self._model),
        }

        self._session_callback = self._model.session.add_callback(self._session_observer)
        self._winner_callback = self._model.winner.add_callback(self._winner_observer)
        self._current_view: ttk.Frame | None = None

    # To WinnerView
    def _winner_observer(self, winner: str) -> None:
        self.switch("winner", {"winner": winner})

    # To FieldView/Menu
    def _session_observer(self, data: dict[str, Any]) -> None:
        if "view_name" in data and type(data["view_name"]) is str:
            self.switch(data["view_name"], data)

    def switch(self, name: str, data: dict) -> None:
        if name not in self._viewmodels:
            raise RuntimeError(f"Unknown view to switch: {name}")
        if self._current_view is not None:
            self._current_view.destroy()
        self._current_view = self._viewmodels[name].start(self._root, data)
        self._current_view.grid(row=0, column=0, sticky="NSEW")

    def start(self) -> None:
        self.switch("menu", {})


class IViewModel(metaclass=ABCMeta):
    def __init__(self, model: TicTacToeModel):
        self._model = model

    @abstractmethod
    def start(self, root: Tk, data: dict[str, Any]) -> ttk.Frame:
        raise NotImplementedError


class MenuViewModel(IViewModel):

    def _bind(self, view: MenuView) -> None:
        def chose_single_player() -> None:
            self._model.session.value = {
                "view_name": "field",
                "user_1": SinglePlayer("X"),
                "user_2": SinglePlayer("O"),
            }

        def chose_bot_easy() -> None:
            self._model.session.value = {
                "view_name": "choose",
                "user_1": SinglePlayer,
                "user_2": BotEasy,
            }

        def chose_bot_hard() -> None:
            self._model.session.value = {
                "view_name": "choose",
                "user_1": SinglePlayer,
                "user_2": BotHard,
            }

        def choos_multiplayer() -> None:
            self._model.session.value = {"view_name": "multiplayer"}

        view.button_single_player.config(command=lambda: chose_single_player())
        view.button_bot_easy.config(command=lambda: chose_bot_easy())
        view.button_bot_hard.config(command=lambda: chose_bot_hard())
        view.button_multiplayer.config(command=lambda: choos_multiplayer())

    def start(self, root: Tk, data: dict[str, Any]) -> ttk.Frame:
        frame = MenuView(root)
        self._bind(frame)
        return frame


class MultiplayerViewModel(IViewModel):

    def _bind(self, view: MultiplayerView) -> None:

        def take_ip() -> None:
            ip = view._get_ip()
            self._model.session.value = {"view_name": "field", "ip": str(ip)}

        view.ip_button.config(command=lambda: take_ip())

    def start(self, root: Tk, data: dict[str, Any]) -> ttk.Frame:
        frame = MultiplayerView(root)
        self._bind(frame)
        return frame


class ChooseSideViewModel(IViewModel):

    def _bind(self, view: ChooseSideView, data: dict[str, Any]) -> None:

        def choose(user_1: User, user_2: User) -> None:
            self._model.session.value = {"view_name": "field", "user_1": user_1, "user_2": user_2}

        if "user_1" in data or "user_2" in data:
            if issubclass(data["user_1"], User) and issubclass(data["user_2"], User):

                view.sideX_button.config(command=lambda: choose(data["user_1"]("X"), data["user_2"]("O")))
                view.sideO_button.config(command=lambda: choose(data["user_2"]("X"), data["user_1"]("O")))

    def start(self, root: Tk, data: dict[str, Any]) -> ttk.Frame:
        frame = ChooseSideView(root)
        self._bind(frame, data)
        return frame


class FieldViewModel(IViewModel):

    def _bind(self, view: FieldView, data: dict[str, Any]) -> None:

        def make_move_bot(user: User) -> None:
            if user.name == "bot":
                self._model.make_move(None)

        def make_move_waiter(user: User) -> None:
            if user.name == "waiter":
                thread = Thread(target=self._model.make_move, args=(None,))
                thread.start()

        def make_move_single(pos: int) -> None:
            if isinstance(self._model.current_player.value, SinglePlayer):
                self._model.make_move(pos)

        def make_move_active(pos: int) -> None:
            if isinstance(self._model.current_player.value, ActivePlayer):
                self._model.make_move(pos)

        def write_move(pos: int) -> Callable:
            return lambda value: view.field_buttons[pos].config(text=value)

        # 1) Choose Start or Restart
        if "user_1" in data or "user_2" in data:
            if isinstance(data["user_1"], User) and isinstance(data["user_2"], User):
                self._model.set_users(data["user_1"], data["user_2"])
        elif "ip" in data and type(data["ip"]) is str:
            self._model.connect(data["ip"])
        else:
            self._model.restart()

        # 2) Add buttons display
        possitions = []
        for pos in range(9):
            possitions.append(self._model.field[pos].add_callback(write_move(pos)))

        # 3) Add callbacks for current player and choose current player
        if "ip" in data:
            current_player_callback = self._model.current_player.add_callback(lambda user: make_move_waiter(user))
        else:
            current_player_callback = self._model.current_player.add_callback(lambda user: make_move_bot(user))
        self._model.update_current_player()

        # 4) Make buttons work
        for pos in range(9):
            if "ip" in data:
                view.field_buttons[pos].config(command=partial(make_move_active, pos))
            else:
                view.field_buttons[pos].config(command=partial(make_move_single, pos))

        # 5) Add destroyind callbacks
        def _destroy_wrapper(original_destroy: Callable) -> Callable:
            def destroy() -> None:
                original_destroy()
                current_player_callback()
                for pos in possitions:
                    pos()

            return destroy

        view.destroy = _destroy_wrapper(view.destroy)  # type: ignore

    def start(self, root: Tk, data: dict[str, Any]) -> ttk.Frame:
        frame = FieldView(root)
        self._bind(frame, data)
        return frame


class WinnerViewModel(IViewModel):

    def _bind(self, view: WinnerView, winner: str) -> None:
        view.result_label.config(text=f"Result: {winner}")

        if self._model.conn is None:

            def restart() -> None:
                self._model.session.value = {"view_name": "field"}

            def exit_to_menu() -> None:
                self._model.session.value = {"view_name": "menu"}

            view.button_new_game.grid(row=2, column=0, columnspan=3, pady=20)
            view.button_new_game.config(command=lambda: restart())
            view.button_menu.config(command=lambda: exit_to_menu())

        else:

            def wait_choice() -> None:
                if self._model.conn is not None:
                    while True:
                        data = self._model.conn.recv(1024)
                        if data:
                            data_str = data.decode("utf-8")
                            if data_str == "menu":
                                self._model.conn.close()
                                self._model.session.value = {"view_name": "menu"}

            thread = Thread(target=wait_choice)
            thread.start()

            def req_exit_to_menu() -> None:
                if self._model.conn is not None:
                    self._model.conn.sendall(bytes("menu", encoding="UTF-8"))

            view.button_menu.config(command=lambda: req_exit_to_menu())

    def start(self, root: Tk, data: dict[str, User | str]) -> ttk.Frame:
        if "winner" not in data.keys() or not isinstance(data["winner"], str):
            raise KeyError("Winner is lost")
        frame = WinnerView(root)
        self._bind(frame, data["winner"])
        return frame
