from fastapi import FastAPI, WebSocket
import chess
import uuid

app = FastAPI()

games = {}  # game_id -> chess.Board
connections = {}  # game_id -> list of websockets


@app.websocket("/ws/{game_id}")
async def websocket_endpoint(ws: WebSocket, game_id: str):
    await ws.accept()

    if game_id not in games:
        games[game_id] = chess.Board()
        connections[game_id] = []

    connections[game_id].append(ws)

    board = games[game_id]

    # Send current board
    await ws.send_text(board.fen())

    try:
        while True:
            move_uci = await ws.receive_text()

            try:
                move = chess.Move.from_uci(move_uci)
                if move in board.legal_moves:
                    board.push(move)

                    for conn in connections[game_id]:
                        await conn.send_text(board.fen())
            except:
                pass

    except:
        connections[game_id].remove(ws)
