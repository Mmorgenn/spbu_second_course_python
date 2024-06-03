import socket
from itertools import cycle
from threading import Thread

from loguru import logger

IP: str = "127.0.0.1"
PORT: int = 55555


class Server:

    def __init__(self, players: dict[str, tuple[socket.socket, str]], host_port: str, guest_port: str):
        self.players = players
        self.host_port = host_port
        self.guest_port = guest_port
        self.cycle_ports = cycle([host_port, guest_port])
        self.current_port = host_port

    def update_port(self) -> None:
        self.current_port = next(self.cycle_ports)

    def give_response(self, data: str) -> None:
        data = data.split()
        if data[0] == "menu":
            for conn, addr in self.players.values():
                conn.sendall(bytes("menu", encoding="UTF-8"))
        else:
            if data[1] == self.current_port:
                next_port = next(self.cycle_ports)
                player = self.players[next_port]
                conn, addr = player[0], player[1]
                conn.sendall(bytes(data[0], encoding="UTF-8"))
                self.current_port = next_port

    def get_response(self, conn: socket.socket, addr: str) -> None:
        while True:
            data = conn.recv(1024)
            if data:
                data_str = data.decode("utf-8")
                self.give_response(data_str)
            else:
                logger.info(f"{addr} is disconected")
                conn.close()


def start() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, PORT))
    logger.info(f"Server is active! IP: {IP} PORT: {PORT}")
    sock.listen()
    server = Server({}, "", "")
    while True:
        conn_first, addr_first = sock.accept()
        logger.info(f"{addr_first} is connected")
        conn_first.sendall(bytes("host", encoding="UTF-8"))
        conn_second, addr_second = sock.accept()
        logger.info(f"{addr_second} is connected")
        conn_second.sendall(bytes("guest", encoding="UTF-8"))
        server.host_port = str(addr_first[1])
        server.guest_port = str(addr_second[1])
        server.cycle_ports = cycle([server.host_port, server.guest_port])
        server.players = {str(addr_first[1]): (conn_first, addr_first), str(addr_second[1]): (conn_second, addr_second)}
        server.update_port()
        thread_first = Thread(target=server.get_response, args=(conn_first, addr_first))
        thread_second = Thread(target=server.get_response, args=(conn_second, addr_second))
        thread_first.start()
        thread_second.start()


if __name__ == "__main__":
    start()
