from aiohttp import WSMsgType, web

WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


class Game:
    def __init__(self):
        self.board = [""] * 9
        self.turn = "X"
        self.status = "waiting"
        self.players = {}

    def snapshot(self):
        return {
            "type": "state",
            "board": self.board,
            "turn": self.turn,
            "status": self.status,
        }

    async def publish(self):
        for ws in tuple(self.players):
            if not ws.closed:
                await ws.send_json(self.snapshot())

    def move(self, symbol, cell):
        if self.status != "playing" or symbol != self.turn:
            return "Not your turn or game finished"
        if type(cell) is not int or not 0 <= cell < 9 or self.board[cell]:
            return "Invalid cell"
        self.board[cell] = symbol
        if any(all(self.board[i] == symbol for i in line) for line in WINNING_LINES):
            self.status = f"winner:{symbol}"
        elif all(self.board):
            self.status = "draw"
        else:
            self.turn = "O" if symbol == "X" else "X"
        return None


async def play(request):
    game = request.app["game"]
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    if len(game.players) >= 2:
        await ws.close(code=1008, message=b"Game full")
        return ws
    symbol = "X" if "X" not in game.players.values() else "O"
    game.players[ws] = symbol
    await ws.send_json({"type": "welcome", "symbol": symbol})
    if len(game.players) == 2 and game.status == "waiting":
        game.status = "playing"
    await game.publish()
    try:
        async for message in ws:
            if message.type != WSMsgType.TEXT:
                continue
            try:
                data = message.json()
                error = game.move(symbol, data["cell"])
            except (ValueError, KeyError, TypeError):
                error = "Expected JSON with cell"
            if error:
                await ws.send_json({"type": "error", "message": error})
            else:
                await game.publish()
    finally:
        game.players.pop(ws, None)
        if game.status in {"waiting", "playing"}:
            game.status = "disconnected"
        await game.publish()
    return ws


def create_app():
    app = web.Application()
    app["game"] = Game()
    app.router.add_get("/ws", play)
    return app
