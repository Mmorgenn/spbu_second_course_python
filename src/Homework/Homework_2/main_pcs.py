from src.Homework.Homework_2.command_storage import *

USER_INPUT = "Input command (command list: help) : "
EMPTY_ERROR = ">>> [ERROR] Empty command"
NO_ACTION_ERROR = ">>> [ERROR] No such action"
UNDO_ERROR = ">>> [ERROR] There are no any actions for undo"
COLLECTION_ERROR = ">>> [ERROR] Incorrect collention"
INDEX_ERROR = ">>> [ERROR] Index out of range"
KEY_ERROR = ">>> [ERROR] Incorrect key"
LIST_COLLECTIONS = """Choose collection:
(1) list
(2) dict
(3) deque
>>> """
LIST_COMMANDS = """>>> Commands list:
# first_insert value
# last_insert value
# first_del
# last_del
# add_value key value
# subtract_value key value
# move key_from key_to
# change_value key new_value
# insert key value
# del key
# change_key key_from, key_to
+ All arguments - int +
"""


def choose_collection() -> list | dict | deque:
    while True:
        match input(LIST_COLLECTIONS):
            case "1":
                return list()
            case "2":
                return dict()
            case "3":
                return deque()
            case default:
                print("Error! Choose int 1-3")


def main() -> None:
    collection = choose_collection()
    command_storage = PCS(collection)
    while True:
        user_command = input(USER_INPUT).split()

        if len(user_command) == 0:
            print(EMPTY_ERROR)
            continue

        if len(user_command) == 1:
            if user_command[0] == "help":
                print(LIST_COMMANDS)
                continue
            if user_command[0] == "undo":
                try:
                    command_storage.undo_action()
                    print(f">>> {command_storage.data}")
                except ValueError:
                    print(UNDO_ERROR)
                continue
            if user_command[0] == "exit":
                return

        try:
            action = ACTIONS.dispatch(user_command.pop(0))
            command_storage.apply_action(action(*[int(i) for i in user_command]))
            print(f">>> {command_storage.data}")
        except ValueError:
            print(NO_ACTION_ERROR)
        except TypeError:
            print(NO_ACTION_ERROR)
        except AttributeError:
            print(COLLECTION_ERROR)
        except IndexError:
            print(INDEX_ERROR)
        except KeyError as e:
            print(KEY_ERROR)


if __name__ == "__main__":
    main()
