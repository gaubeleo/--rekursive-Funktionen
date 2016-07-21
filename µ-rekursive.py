import inspect

# 1. Nachfolgerfunktion
def Next(x):
	return x+1

# 2. Konstantenfunktion
def K(k, c):
	def _K(*args):
		return c
	
	return _K

# 3. Produktionsfunktion
def P(k, i):
	def _P(*args):
		# i-1 because Python's list index starts with 0
		return args[i-1]

	return _P 

# 4. Kompsfunktion
def Komp(f, gs=[]):
	def _Komp(*args):
		#print gs
		if type(gs) == tuple or type(gs) == list:
			return f(*[g(*args) for g in gs])
		else:
			return f(gs(*args))

	return _Komp

# 5. Induktionsfunktion
def Ind(_f, _g):
	def _Ind(*args):
		x1 = args[0]
		args = args[1:]
		if x1 == 0:
			return _f(*args)
		else:
			return _g(_Ind(x1-1, *args), x1-1, *args)

	return _Ind

############## Custom ##############


def Plus(x, y):
	return Ind(P(1, 1), Komp(Next, P(3, 1)))(x, y)

def Times(x, y):
	return Ind(K(1, 0), Komp(Plus, (P(3, 1), P(3, 3))))(x, y)

def Previous(x):
	return Ind(K(0, 0), P(2, 2))(x)

def _Monus(y, x):
	return Ind(P(1, 1), Komp(Previous, P(3, 1)))(y, x)

def Monus(x, y):
	return Komp(_Monus, (P(2, 2), P(2, 1)))(x, y)

def Min(x, y):
	return Komp(Monus, (P(2, 2), Komp(Monus, (P(2, 2), P(2, 1)))))(x, y)

def Max(x, y):
	return Komp(Plus, (P(2, 2), Komp(Monus, (P(2, 1), P(2, 2)))))(x, y)

def Max3(x, y, z):
	return isGreater(Komp(isGreater(P(3, 1), P(3, 2)), (P(3, 1), P(3, 3), P(3, 2))), Komp(isGreater(P(3, 1), P(3, 2)), (P(3, 2), P(3, 3), P(3, 1))))(x, y, z)

#--------------------------------------------------------------------------------------------

#Helper
def _f(*args):
	return args

#Helper
def Pk(k, start, end):
	results = []
	for i in range(start, end+1):
		results.append(P(k, i))
	return results

#--------------------------------------------------------------------------------------------

def isZero(_Then, _Else):
	def _isZero(x1, *args):
		k = len(args) 
		return Ind(_Then, Komp(_Else, Pk(k+2, 3, k+2)))(x1, *args)

	return _isZero

def isEqual(_Then, _Else):
	def _isEqual(x, y, *args):
		k = len(args)
		return Komp(isZero(_Then, _Else), _f(Komp(Max, (Komp(Monus, (P(k+2, 1), P(k+2, 2))), Komp(Monus, (P(k+2, 2), P(k+2, 1))))), *Pk(k+2, 1, k+2)))(x, y, *args)

	return _isEqual

def isGreater(_Then, _Else):
	def _isGreater(x, y, *args):
		k = len(args)
		return Komp(isZero(_Then, _Else), _f(Komp(Monus, (Komp(Next, P(k+2, 2)), P(k+2, 1))), *Pk(k+2, 1, k+2)))(x, y, *args)

	return _isGreater

if __name__ == "__main__":
	print "Tests:"
	print Plus(4, 9) == 13
	print Times(7, 8) == 56
	print Previous(8) == 7
	print Monus(9, 7) == 2
	print Monus(7, 9) == 0
	print Min(5, 9) == 5
	print Min(9, 5) == 5
	print Max(5, 15) == 15
	print Max(15, 5) == 15
	
	print
	print "isZero:"
	print isZero(P(2, 1), P(2, 2))(0, 3, 4) == 3
	print isZero(P(3, 1), P(3, 3))(2, 3, 4, 5) == 5
	
	print
	print "isEqual:"
	print isEqual(P(4, 3), P(4, 4))(8, 8, 3, 5) == 3
	print isEqual(P(4, 3), P(4, 4))(8, 9, 3, 5) == 5
	print isEqual(P(4, 3), P(4, 4))(9, 8, 3, 5) == 5

	print
	print "isGreater:"
	print isGreater(K(2, 3), K(2, 5))(8, 9) == 5
	print isGreater(P(4, 3), P(4, 4))(8, 8, 3, 5) == 5
	print isGreater(P(4, 3), P(4, 4))(8, 9, 3, 5) == 5
	print isGreater(P(4, 3), P(4, 4))(9, 8, 3, 5) == 3
	
	print
	print "Max3:"
	print Max3(4, 5, 6) == 6
	print Max3(4, 6, 5) == 6
	print Max3(5, 4, 6) == 6
	print Max3(5, 6, 4) == 6
	print Max3(6, 4, 5) == 6
	print Max3(6, 5, 4) == 6
