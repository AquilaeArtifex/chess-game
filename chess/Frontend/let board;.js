let board;
let game = new Chess();
let socket;

function start() {
  const gameId = document.getElementById("gameId").value;

  socket = new WebSocket(
    `wss://YOUR-BACKEND-URL/ws/${gameId}`
  );

  socket.onmessage = (event) => {
    game.load(event.data);
    board.position(game.fen());
  };

  board = Chessboard('board', {
    draggable: true,
    position: 'start',
    onDrop: (source, target) => {
      const move = game.move({
        from: source,
        to: target,
        promotion: 'q'
      });

      if (move === null) return 'snapback';

      socket.send(source + target);
    }
  });
}
