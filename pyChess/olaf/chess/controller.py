from olaf.chess.AI import decide
from olaf.chess.models import GameBoard as ChessBoard
from olaf.chess.models import InvalidMoveError, Pos

from olaf.models import GameBoard
from olaf.forms import MoveForm as FORM

def chess_move_parse ( s ):
	s = s.lower ()
	return Pos ( int ( s [ 1 ] ) - 1 ,ord ( s [ 0 ] ) - ord ( 'a' ) )

def proccess_move ( request ):
	if ( request.method != "POST" ):
		return None

	if ( request.POST.get ( 'move' ) is None ):
		return None

	form = FORM  ( request.POST )
	if ( not form.is_valid () ):
		request.session [ 'message' ] = "Invalid Move"
		return None

	if ( request.session.get ( 'game_id' ) is None ):
		request.session [ 'message' ] = "No Active Game"
		return None

	if ( GameBoard.objects.filter ( id = request.session [ 'game_id' ] ).first () is None ):
		del request.session [ 'game_id' ]
		request.session [ 'message' ] = "No Active Game"
		return None

	gameboard = GameBoard.objects.filter ( id = request.session [ 'game_id' ] ).first ()

	if ( gameboard.result != 0 ):
		del request.session [ 'game_id' ]		
		request.session [ 'message' ] = "The game is over already"
		return None
		
	g = ChessBoard ( gameboard.state )
	s, t = request.POST [ 'move' ].split ()

	try:
		g.move ( chess_move_parse ( s ), chess_move_parse ( t ), 1 )
	except InvalidMoveError:
		request.session [ 'message' ] = "Invalid Move"
		return None

	gameboard.state = str  ( g )
	gameboard.save ()

	if ( g.is_mate ( -1 ) ):
		print ( g._is_check ( -1 ) )
		gameboard.result = 1
		gameboard.save ()

		us = gameboard.user
		us.wins = us.wins + 1
		us.save ()
		
		request.session [ 'message' ] = "You've Won"
		return None

	if ( g.is_pot ( -1 ) ):
		gameboard.result = 3
		gameboard.save ()

		us = gameboard.user
		us.ties = us.ties + 1
		us.save ()
		
		request.session [ 'message' ] = "The game is Tied"
		return None

	print ( "before decide" )
	gameboard.state = decide ( g )[ 1 ]
	gameboard.save ()
	print ( "after decide" )

	g = ChessBoard ( gameboard.state )

	if ( g.is_mate ( 1 ) ):
		gameboard.result = 2
		gameboard.save ()

		us = gameboard.user
		us.loses = us.loses + 1
		us.save ()
		
		request.session [ 'message' ] = "You've Lost"
		return None

	if ( g.is_pot ( 1 ) ):
		gameboard.result = 3
		gameboard.save ()

		us = gameboard.user
		us.ties = us.ties + 1
		us.save ()
		
		request.session [ 'message' ] = "The game is Tied"
		return None

	return None