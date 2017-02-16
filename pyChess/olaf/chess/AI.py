from olaf.chess.models import *

def value ( g ):
	q, r, b, n, p, d, iso = ( { 1:0 , -1:0 } for i in range ( 7 ) )

	for piece in g:
		if ( piece ):
			if ( isinstance ( piece, Queen ) ):
				q [ piece._side ] += 1
			if ( isinstance ( piece, Rook ) ):
				r [ piece._side ] += 1
			if ( isinstance ( piece, Bishop ) ):
				b [ piece._side ] += 1
			if ( isinstance ( piece, Knight ) ):
				n [ piece._side ] += 1
			if ( isinstance ( piece, Soldier ) ):
				p [ piece._side ] += 1

				if ( (piece._pos + Pos (1, 0)) and g [piece._pos + Pos (1, 0)] and g [piece._pos + Pos (1, 0)]._side == g [piece._pos]._side and isinstance ( g[piece._pos + Pos (1, 0)], Soldier ) ):
					d [ piece._side ] += 1

				val = 1
				for i in range ( -1, 2 ):
					for j in range ( -1, 2 ):
						if ( i == j == 0 ):
							continue
						pos = Pos ( i, j)
						if ( (piece._pos + pos) and g [piece._pos + pos] and g [piece._pos + pos]._side == g [piece._pos]._side and isinstance ( g[piece._pos + pos], Soldier ) ):
							val = 0
				iso [ piece._side ] = val

	ret = 0
	ret += 90 * ( q [ -1 ] - q [ 1 ] )
	ret += 50 * ( r [ -1 ] - r [ 1 ] )
	ret += 30 * ( b [ -1 ] - b [ 1 ] )
	ret += 55 * ( n [ -1 ] - n [ 1 ] )
	ret += 10 * ( p [ -1 ] - p [ 1 ] )
	ret += 5 * ( d [ -1 ] - d [ 1 ] )
	ret += 5 * ( iso [ 1 ] - iso [ -1 ] )
	ret += 2 * ( sum ( 1 for x in g ( -1 )) - sum ( 1 for x in g ( 1 )) )

	if ( g.is_pot ( 1 ) or g.is_pot ( -1 ) ):
		ret += 300
	if ( g.is_mate ( 1 ) ):
		ret += 10000
	if ( g.is_mate ( -1 ) ):
		ret -= 10000

	return ret

def decide ( g, side = -1, depth = 2 ):
	if ( not depth ):
		return (value ( g ), str ( g ))

	if ( g.is_mate ( side ) or g.is_pot ( side ) ):
		return (value ( g ), str ( g ))

	st = ""
	if ( side == 1 ):
		val = 100000

		for i in g ( side ):
			next_val = decide ( g, side * -1, depth - 1 )[0]

			if ( next_val <= val ):
				val = next_val
				st = str ( g )
	else:
		val = -100000

		for i in g ( side ):
			next_val = decide ( g, side * -1, depth - 1 )[0]

			if ( next_val >= val ):
				val = next_val
				st = str ( g )

	return ( val, st )#can be improved