from abc import ABCMeta, abstractmethod
from itertools import cycle
from random import choice
from typing import Iterable

from src.Homework.Homework_5.observer import Observable

WIN_POS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


class User(metaclass=ABCMeta):
    def __init__(self, name: str, side: str) -> None:
        self.name = name
        self.side = side

    @abstractmethod
    def make_move(self, field: list[Observable[str]], possible_pos: list[int], pos: int | None) -> None:
        raise NotImplementedError


class SinglePlayer(User):
    def __init__(self, name: str, side: str) -> None:
        super().__init__(name, side)

    def make_move(self, field: list[Observable[str]], possible_pos: list[int], pos: int | None) -> None:
        if pos is None:
            return
        field[pos].value = self.side
        possible_pos.remove(pos)


class Bot_Easy(User):
    def __init__(self, side: str) -> None:
        super().__init__("bot", side)

    def make_move(self, field: list[Observable[str]], possible_pos: list[int], pos: int | None) -> None:
        move_pos = choice(possible_pos)
        field[move_pos].value = self.side
        possible_pos.remove(move_pos)


class Bot_Hard(User):
    def __init__(self, side: str) -> None:
        super().__init__("bot", side)

    def make_move(self, field: list[Observable[str]], possible_pos: list[int], pos: int | None) -> None:
        move_pos = self.choose_move(field, possible_pos)
        field[move_pos].value = self.side
        possible_pos.remove(move_pos)

    def choose_move(self, field: list[Observable[str]], possible_pos: list[int]) -> int:
        if len(possible_pos) == 9:
            return 4
        win_pos = self.get_win_pos(field, possible_pos, self.side)
        if len(win_pos) > 0:
            return win_pos[0]
        enemys_side = "X" if self.side == "O" else "O"
        importan_pos = self.get_win_pos(field, possible_pos, enemys_side)
        if len(importan_pos) > 0:
            return importan_pos[0]
        return choice(possible_pos)

    def get_win_pos(self, field: list[Observable[str]], possible_pos: list[int], side: str) -> list[int]:
        win_pos = []
        for pos in possible_pos:
            field_pos = [pos.value for pos in field]
            field_pos[pos] = side
            if self.check_winner(field_pos, side):
                win_pos.append(pos)
        return win_pos

    def check_winner(self, field: list[str | None], side: str) -> bool:
        for pos in WIN_POS:
            if field[pos[0]] == field[pos[1]] == field[pos[2]] == side:
                return True
        return False


class TicTacToeModel:
    def __init__(self) -> None:
        self.field: list[Observable[str]] = [Observable() for _ in range(9)]
        self.possible_pos: list[int] = []
        self.user_1: User | None = None
        self.user_2: User | None = None
        self.cycle_players: cycle[User | None] = cycle([])
        self.current_player: Observable[User | None] = Observable()
        self.winner: Observable[str] = Observable()
        self.session: Observable[dict[str, User]] = Observable()
        self.exit: Observable[int] = Observable()

    def update_current_player(self) -> None:
        self.current_player.value = next(self.cycle_players)

    def set_users(self, user_1: User, user_2: User) -> None:
        for i in self.field:
            i.value = ""
        self.possible_pos = [i for i in range(9)]
        self.user_1 = user_1
        self.user_2 = user_2
        self.cycle_players = cycle([user_1, user_2])

    def check_winner(self) -> str:
        if not isinstance(self.user_1, User) or not isinstance(self.user_2, User):
            raise KeyError("Users are not found")
        for pos in WIN_POS:
            if self.field[pos[0]].value == self.field[pos[1]].value == self.field[pos[2]].value != "":
                if self.user_1.side == self.field[pos[0]].value:
                    self.winner.value = self.user_1.side
                    return self.user_1.side
                self.winner.value = self.user_2.side
                return self.user_2.side
        if len(self.possible_pos) == 0:
            return "Draw"
        return ""

    def make_move(self, pos: int | None = None) -> None:
        if not isinstance(self.current_player.value, User):
            raise KeyError("Current user is not found")
        if pos is None or pos in self.possible_pos:
            self.current_player.value.make_move(self.field, self.possible_pos, pos)
        else:
            return

        current_result = self.check_winner()
        if current_result != "":
            self.winner.value = current_result
        else:
            self.update_current_player()

    def restart(self) -> None:
        if not isinstance(self.user_1, User) or not isinstance(self.user_2, User):
            raise KeyError("Users are not found")
        if self.user_2.side == self.winner.value:
            self.set_users(self.user_2, self.user_1)
        else:
            self.set_users(self.user_1, self.user_2)
