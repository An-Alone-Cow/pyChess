class InvalidMoveError ( Exception ):
	pass
#####

class EmptyField:
	def __init__ ( self, x = 0, y = 0, side = 0, board = 0 ):
		pass

	def __str__ ( self ):
		return "0"

	def parsed ( self ):
		return '.'

	def __bool__ ( self ):
		return False
#####

class Pos:
	def __init__ ( self, *v ):
		self._x, self._y = v

	def __del__ ( self ):
		del self._x, self._y

	def __str__ ( self ):
		return str ( self._x ) + " " + str ( self._y )

	def __eq__ ( self, v ):
		return (self._x == v._x and self._y == v._y)

	def __bool__ ( self ):
		if ( 0 <= self._x < 8 and 0 <= self._y < 8 ):
			return True
		else:
			return False

	def __add__ ( self, v ):
		if ( isinstance ( v, Pos ) ):
			x, y = v._x, v._y
		else:
			x, y = v

		return Pos ( self._x + x, self._y + y )
	__radd__ = __add__

	def __iadd__ ( self, v ):
		if ( isinstance ( v, Pos ) ):
			x, y = v._x, v._y
		else:
			x, y = v

		self._x += x
		self._y += y

		return self

class Piece:
	def __init__ ( self, x, y, side, val, board ):
		self._pos = Pos ( x, y )
		self._side = side
		self._val = val
		self._board = board

	def __del__ ( self ):
		del self._pos, self._side, self._val

	def __bool__ ( self ):
		return True

	def gen ( self, vec ):
		arr = self._board

		for v in vec:
			p = self._pos + v
			while ( p and not arr [ p ] ):
				yield ( p )
				p += v
			if ( p and arr [ p ]._side * arr [ self ]._side == -1 ):
				yield ( p )

class Soldier ( Piece ):
	def __init__ ( self, x, y, side, board ):
		super ().__init__ ( x, y, side, 1, board )

	def __str__ ( self ):
		return hex ( (self._side + 1) // 2 + self._val * 2 - 1 )[ 2 ]

	def parsed ( self ):
		return 'P' if self._side == 1 else 'p'

	def __call__ ( self ):
		arr = self._board
		x, y = self._pos._x, self._pos._y

		if ( (self._pos + (self._side, 0)) and not arr [ self._pos + (self._side, 0) ] ):
			yield ( self._pos + (self._side, 0) )

		if ( x == ((7 + self._side) % 7) and (not arr [ self._pos + (self._side, 0) ]) and (not arr [ self._pos + (2 * self._side, 0 ) ]) ):
			yield ( self._pos + (self._side * 2, 0) )
		
		if ( (self._pos + (self._side, 1)) and arr [ self._pos + (self._side, 1) ] and arr [ self._pos + (self._side, 1) ]._side * self._side == -1 ):
			yield ( self._pos + (self._side, 1) )
		if ( (self._pos + (self._side, -1)) and arr [ (self._pos + (self._side, -1)) ] and arr [ (self._pos + (self._side, -1)) ]._side * self._side == -1 ):
			yield ( self._pos + (self._side, -1) )

class Rook ( Piece ):
	def __init__ ( self, x, y, side, board ):
		super ().__init__ ( x, y, side, 2, board )

	def __str__ ( self ):
		return hex ( (self._side + 1) // 2 + self._val * 2 - 1 )[ 2 ]

	def parsed ( self ):
		return 'R' if self._side == 1 else 'r'

	def __call__ ( self ):
		return self.gen ( [ (0, 1), (0, -1), (1, 0), (-1, 0) ] )

class Bishop ( Piece ):
	def __init__ ( self, x, y, side, board ):
		super ().__init__ ( x, y, side, 3, board )

	def __str__ ( self ):
		return hex ( (self._side + 1) // 2 + self._val * 2 - 1 )[ 2 ]

	def parsed ( self ):
		return 'B' if self._side == 1 else 'b'

	def __call__ ( self ):
		return self.gen ( [ (1, 1), (1, -1), (-1, 1), (-1, -1) ] )

class Knight ( Piece ):
	def __init__ ( self, x, y, side, board ):
		super ().__init__ ( x, y, side, 4, board )

	def __str__ ( self ):
		return hex ( (self._side + 1) // 2 + self._val * 2 - 1 )[ 2 ]

	def parsed ( self ):
		return 'K' if self._side == 1 else 'k'

	def __call__ ( self ):
		vec = [ (1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1) ]
		arr = self._board
		for v in vec:
			p = self._pos + v
			if ( p and ((not arr [ p ]) or (arr [ p ] and arr [ p ]._side * self._side != 1)) ):
				yield p

class Queen ( Piece ):
	def __init__ ( self, x, y, side, board ):
		super ().__init__ ( x, y, side, 5, board )

	def __str__ ( self ):
		return hex ( (self._side + 1) // 2 + self._val * 2 - 1 )[ 2 ]

	def parsed ( self ):
		return 'Q' if self._side == 1 else 'q'

	def __call__ ( self ):
		return self.gen ( [ (i, j) for i in range ( -1, 2 ) for j in range ( -1, 2 ) if not (i == 0 and j == 0) ] )

class King ( Piece ):
	def __init__ ( self, x, y, side, board ):
		super ().__init__ ( x, y, side, 6, board )

	def __str__ ( self ):
		return hex ( (self._side + 1) // 2 + self._val * 2 - 1 )[ 2 ]

	def parsed ( self ):
		return 'M' if self._side == 1 else 'm'

	def __call__ ( self ):
		vec = [ (i, j) for i in range ( -1, 2 ) for j in range ( -1, 2 ) if not (i == 0 and j == 0) ]
		arr = self._board
		for v in vec:
			p = self._pos + v
			if ( p and arr [ p ]._side * self._side != 1 ):
				yield p
#####

class GameBoard:
	class GameBoard_iterator:
		def __init__ ( self, board ):
			self.__i = 0
			self.__j = 0
			self.__board = board

		def __iter__ ( self ):
			return self
		def __next__ ( self ):
			if ( self.__i == 8 ):
				raise StopIteration

			res = self.__board._mat [ self.__i ][ self.__j ]

			self.__j += 1
			self.__i += self.__j // 8
			self.__j %= 8

			return res

	def int_to_hs ( self, x ):
		ref = [ str (i) for i in range ( 10 ) ]+[ chr (i) for i in range ( ord ('a'), ord ('z') + 1 ) ]+[ chr (i) for i in range ( ord ('A'), ord ('Z') + 1 ) ]
		res = []
		while ( x ):
			res.append ( ref [ x % 62 ] )
			x //= 62

		return ''.join ( reversed ( res ) )

	def hs_to_int ( self, s ):
		ref = [ str (i) for i in range ( 10 ) ]+[ chr (i) for i in range ( ord ('a'), ord ('z') + 1 ) ]+[ chr (i) for i in range ( ord ('A'), ord ('Z') + 1 ) ]
		dic = { c : i for i, c in enumerate ( ref, start = 0 ) }
		x = 0

		for c in s:
			x *= 62
			x += dic [ c ]

		return x
	
	def __init__ ( self, state ):
		state = self.hs_to_int ( state )

		self._pre = []
		self._undo = []

		self._enpass = state & 127
		state >>= 7
		self._bc = state & 1
		state >>= 1
		self._wc = state & 1
		state >>= 1

		res = []
		while ( state ):
			res.append ( (state % 13) + 1 )
			state //= 13
		state = list ( reversed ( res ) )
		state = state [ 1: ]

		piece_list = [ EmptyField, Soldier, Rook, Bishop, Knight, Queen, King ]
		self._mat = [ [ piece_list [ state [ 8 * i + j ] // 2 ]( i, j, (state [ 8 * i + j ] & 1) * 2 - 1, self ) for j in range ( 8 ) ] for i in range ( 8 ) ]

	def __str__ ( self ):
		ret = int ( '1' + ''.join ( [ str ( self._mat [ i ][ j ] ) for i in range ( 8 ) for j in range ( 8 ) ] ), 13 )

		ret *= 2
		ret += self._wc

		ret *= 2
		ret += self._bc

		ret *= 128
		ret += self._enpass

		return self.int_to_hs ( ret )

	def __del__ ( self ):
		for p in self._mat:
			for x in p:
				del x
		del self._enpass, self._wc, self._bc, self._pre, self._undo

	def __getitem__ ( self, v ):
		if ( isinstance ( v, Pos ) ):
			x, y = v._x, v._y
		if ( isinstance ( v, tuple ) ):
			x, y = v
		if ( isinstance ( v, Piece ) ):
			x, y = v._pos._x, v._pos._y

		if ( Pos ( x, y ) ):
			return self._mat [ x ][ y ]
		else:
			return None

	def __setitem__ ( self, v, val ):
		if ( isinstance ( v, Pos ) ):
			x, y = v._x, v._y
		if ( isinstance ( v, tuple ) ):
			x, y = v
		if ( isinstance ( v, Piece ) ):
			x, y = v._pos._x, v._pos._y

		if ( Pos ( x, y ) ):
			self._mat [ x ][ y ] = val
			return self._mat [ x ][ y ]
		else:
			return None

	def __iter__ ( self ):
		return GameBoard.GameBoard_iterator ( self )

	@property
	def translated ( self ):
		return [ list ( map ( lambda x : x.parsed () , p ) ) for p in self._mat ]

	def _is_check ( self, side, p = None ):
		if ( p is None ):
			for piece in self:
				if ( isinstance ( piece, King ) and piece._side == side ):
					p = piece._pos

		for piece in self:
			if ( piece and piece._side * side == -1 ):
				if ( p in piece () ):
					return True

		return False

	def _is_castle ( self, p1, p2, side ):
		if ( side == 1 ):
			if ( not self._wc ):
				return False
		else:
			if ( not self._bc ):
				return False

		if ( p1 and self [ p1 ]._side * side == 1 and p2 and self [ p2 ]._side * side == 1 ):
			if ( isinstance ( self [ p2 ], King ) ):
				p1, p2 = p2, p1

			if ( isinstance ( self [ p1 ], King ) and isinstance ( self [ p2 ], Rook ) ):
				for y in range ( min ( p1._y, p2._y) + 1, max ( p1._y, p2._y ) ):
					if ( self [ ( p1._x, y ) ] ):
						return False

				if ( p2._y == 0 ):
					k = -1
				else:
					k = 1

				if ( self._is_check ( p1 + (0, k) ) or self._is_check ( side, p1 + (0, 2*k) ) ):
					return False
			else:
				return False
		else:
			return False

		return True

	def _is_enpass ( self, p1, p2, side ):
		if ( 0 <= self._enpass < 64 ):
			pass
		else:
			return False

		x, y = self._enpass // 8, self._enpass % 8
		if ( isinstance ( self [ p1 ], Soldier ) and self [ p1 ]._side * side == 1 ):
			if ( p1._x == x and abs ( p1.y - y ) == 1 ):
				return True
		return False

	def _move ( self, p1, p2 ):
		x1, y1 = p1._x, p1._y
		x2, y2 = p2._x, p2._y

		self._pre.append ( (self [ p2 ], Pos ( x1, y1 ), Pos ( x2, y2 ), self._wc, self._bc, self._enpass) )
		self._undo.append ( self._undo_move )

		self [ p2 ] = self [ p1 ]
		self [ p1 ]._pos = Pos ( x2, y2 )
		self [ p1 ] = EmptyField ()

	def _undo_move ( self ):
		piece, p1, p2, wc, bc, enpass = self._pre [ -1 ]

		self._wc, self._bc, self._enpass = wc, bc, enpass

		x1, y1 = p1._x, p1._y
		x2, y2 = p2._x, p2._y
		self [ p1 ] = self [ p2 ]
		self [ p1 ]._pos = p1 + (0, 0)
		self [ p2 ] = piece

	def _move_castle ( self, p1, p2 ):
		if ( isinstance ( self [ p2 ], King ) ):
			p1, p2 = p2, p1

		if ( p2._y == 0 ):
			k = -1
		else:
			k = 1

		self [ p1 ]._pos += (0, 2 * k)
		self [ p1 ], self [ p1 + (0, 2 * k) ] = self [ p1 + (0, 2 * k) ], self [ p1 ]
		self [ p2 ]._pos = p1 + (0, k)
		self [ p2 ], self [ p1 + (0, k) ] = self [ p1 + (0, k) ], self [ p2 ]

		if ( p1._x ):
			self._bc = False
		else:
			self._wc = False

		self._pre.append ( (p1 + (0, 0), p2 + (0, 0)) )
		self._undo.append ( self._undo_castle )

	def _undo_castle ( self ):
		p1, p2 = self._pre [ -1 ]

		if ( p2._y == 0 ):
			k = -1
		else:
			k = 1

		self [ p1 ], self [ p1 + (0, 2 * k) ] = self [ p1 + (0, 2 * k) ], self [ p1 ]
		self [ p1 ]._pos = p1 + (0, 0)
		self [ p2 ], self [ p1 + (0, k) ] = self [ p1 + (0, k) ], self [ p2 ]
		self [ p2 ]._pos = p2 + (0, 0)

		if ( p1._x ):
			self._bc = True
		else:
			self._wc = True

	def _move_enpass ( self, p1, p2, side ):
		self._undo.append ( self._undo_enpass )
		self._pre.append ( (self [ p2 + (-side, 0) ], p1 + (0, 0), p2 + (0, 0), self._enpass, side ) )

		self [ p1 ]._pos = p2 + (0, 0)
		self [ p1 ], self [ p2 ] = self [ p2 ], self [ p1 ]
		self [ p2 + (-side, 0) ] = EmptyField ()
		self._enpass = 64

	def _undo_enpass ( self ):
		piece, p1, p2, enpass, side = self._undo [ -1 ]

		self [ p1 ], self [ p2 ] = self [ p2 ], self [ p1 ]
		self [ p1 ]._pos = p2 + (0, 0)
		self [ p2 + (-side, 0) ] = piece
		self._enpass = enpass

	def undo ( self ):
		self._undo [ -1 ]()

		self._undo.pop ()
		self._pre.pop ()

	def check_move ( self, p1, p2, side ):
		res = False

		if ( self [ p1 ] and self [ p1 ]._side * side == 1 and (p2 in self [ p1 ] ()) ):
			self._move ( p1, p2 )

			if ( not self._is_check ( side ) ):
				res = True
			self.undo ()

		return res

	def move ( self, p1, p2, side ):
		if ( p1 and p2 ):
			pass
		else:
			raise InvalidMoveError ( "Move is not valid." )

		if ( self [ p1 ] and self [ p1 ]._side == side ):
			pass
		else:
			raise InvalidMoveError ( "Move is not valid." )

		if ( self._is_castle ( p1, p2, side ) ):
			self._move_castle ( p1, p2 )
			return None

		if ( self._is_enpass ( p1, p2, side ) ):
				self._move_enpass ( p1, p2 )

				if ( self._is_check ( side ) ):
					self.undo ()
					raise InvalidMoveError ( "Move is not valid." )
				else:
					return None

		if ( self.check_move ( p1, p2, side ) ):
			self._move ( p1, p2 )

			self._enpas = 64
			if ( isinstance ( self [ p1 ], Soldier ) and p1._x == (7 + side) % 7 and abs(p2._x - p1._x) == 2 ):
				self._enpas = 8 * p2._x + p2._y

			if ( p1 == Pos ( (8 + side) % 9, 0 ) or p1 == Pos ( (8 + side) % 9, 7 ) or p1 == Pos ( (8 + side) % 9, 4 ) ):
				if ( side == 1 ):
					self._wc = False
				else:
					self._bc = False
		else:
			raise InvalidMoveError ( "Move is not valid." )

	def promote ( self, p, side, obj ):
		self._pre.append ( (p + (0, 0), side) )
		self._undo.append ( self._undo_promote )

		self [ p ] = obj ( p._x, p._y, side, self )

	def _undo_promote ( self ):
		p, side = self._pre [ -1 ]

		self [ p ] = Soldier ( p._x, p._y, side, self )

	def __call__ ( self, side ):
		for piece in self:
			if ( piece and piece._side == side ):
				lst = [ piece._pos + (side, 1), piece._pos + (side, -1) ]

				for dest in piece ():
					if ( dest in lst ):
						lst.remove ( dest )

					try:
						self.move ( piece._pos, dest, side )
						yield str ( self )
						self.undo ()
					except InvalidMoveError:
						pass

				for dest in lst:
					try:
						self.move ( piece._pos, dest, side )
						yield str ( self )
						self.undo ()
					except InvalidMoveError:
						pass

		lst = [ (Pos (0, 0), Pos ( 0, 4 )), (Pos (0, 7), Pos ( 0, 4 )), (Pos (7, 0), Pos ( 7, 4 )), (Pos (7, 7), Pos ( 7, 4 )) ]
		for ( p1, p2 ) in lst:
			if ( self [ p1 ] and self [ p2 ] and self [ p1 ]._side == side == self [ p2 ]._side ):
				try:
					self.move ( p1, p2, side )
					yield str ( self )
					self.undo ()
				except InvalidMoveError:
					pass

	# configuring first player settings in higher levels

a = GameBoard ( '4qJUX2X8bojZVNRp1nOF053R9sMHhefbMuOkdSf4Uo' )

for s in a ( 1 ):
	print ( *GameBoard ( s ).translated, sep = '\n', end = '\n\n' )
