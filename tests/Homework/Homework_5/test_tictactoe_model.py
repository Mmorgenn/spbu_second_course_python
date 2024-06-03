import pytest

from src.Homework.Homework_5.model import BotHard, SinglePlayer, TicTacToeModel


class Tester:
    def __init__(self):
        self.model = TicTacToeModel()

    def set_field(self, field: list[str]):
        for i in range(9):
            self.model.field[i].value = field[i]

    def set_possible_pos(self, possible_pos: list[str]):
        self.model.possible_pos = possible_pos

    def set_single_player(self):
        self.model.set_users(SinglePlayer("X"), SinglePlayer("O"))

    def set_bot_hard(self):
        self.model.set_users(SinglePlayer("X"), BotHard("O"))


@pytest.mark.parametrize(
    "field,possible_pos,expected",
    (
        (["" for _ in range(9)], [i for i in range(9)], ""),
        (["O", "X", "X", "X", "X", "O", "O", "O", "X"], [], "Draw"),
        (["O", "O", "O", "X", "X", "", "X", "", ""], [5, 7, 8], "O"),
        (["X", "O", "", "O", "X", "", "", "", "X"], [2, 5, 6, 7], "X"),
    ),
)
def test_check_winner(field, possible_pos, expected):
    model = Tester()
    model.set_single_player()
    model.set_field(field)
    model.set_possible_pos(possible_pos)
    assert model.model.check_winner() == expected


@pytest.mark.parametrize(
    "field,possible_pos,expected",
    (
        (["" for _ in range(9)], [i for i in range(9)], ["", "", "", "", "O", "", "", "", ""]),
        (["X", "", "O", "", "X", "", "", "", ""], [1, 3, 5, 6, 7, 8], ["X", "", "O", "", "X", "", "", "", "O"]),
        (["", "", "", "O", "", "X", "O", "", "X"], [0, 1, 2, 4, 7], ["O", "", "", "O", "", "X", "O", "", "X"]),
    ),
)
def test_hard_bot(field, possible_pos, expected):
    model = Tester()
    model.set_bot_hard()
    model.set_field(field)
    model.set_possible_pos(possible_pos)
    model.model.update_current_player()
    model.model.update_current_player()
    model.model.make_move(None)
    assert [obs.value for obs in model.model.field] == expected


@pytest.mark.parametrize(
    "field,possible_pos,pos,expected",
    (
        (["" for _ in range(9)], [i for i in range(9)], 1, ["", "X", "", "", "", "", "", "", ""]),
        (["O", "", "X", "X", "X", "O", "O", "O", "X"], [1], 0, ["O", "", "X", "X", "X", "O", "O", "O", "X"]),
        (["O", "", "O", "X", "X", "O", "X", "", ""], [1, 7, 8], 7, ["O", "", "O", "X", "X", "O", "X", "X", ""]),
        (["X", "O", "", "O", "X", "", "", "", ""], [2, 5, 6, 7, 8], 8, ["X", "O", "", "O", "X", "", "", "", "X"]),
    ),
)
def test_single_player(field, possible_pos, pos, expected):
    model = Tester()
    model.set_single_player()
    model.set_field(field)
    model.set_possible_pos(possible_pos)
    model.model.update_current_player()
    model.model.make_move(pos)
    assert [obs.value for obs in model.model.field] == expected
