from Header import Header
from Node import Node

def constraint_matrix(s=9):
	return [[[Node(r,c,n) for n in range(s)] for c in range(s)] for r in range(s)]

def make(s = 9):
	root = Header()
	curH = root
	
	posM = constraint_matrix(s)
	rowM = constraint_matrix(s)
	colM = constraint_matrix(s)
	boxM = constraint_matrix(s)
	
	# Vertical Linking
	
	# Position Constraints
	for r in range(s):
		for c in range(s):
			h = Header(r,c)
			h.numRows = s
			curH.addRight(h)
			curH = curH.right
			curR = curH
			for n in range(s):
				curR.addDown(posM[r][c][n])
				curR = curR.down
				
	# Row Constraints
	for r in range(s):
		for n in range(s):
			h = Header(r,-1,n)
			h.numRows = s
			curH.addRight(h)
			curH = curH.right
			curR = curH
			for c in range(s):
				curR.addDown(rowM[r][c][n])
				curR = curR.down
	
	# Column Constraints
	for c in range(s):
		for n in range(s):
			h = Header(-1,c,n)
			h.numRows = s
			curH.addRight(h)
			curH = curH.right
			curR = curH
			for r in range(s):
				curR.addDown(colM[r][c][n])
				curR = curR.down
	
	# Box Constraints
	for br in range(int(s**.5)):
		for bc in range(int(s**.5)):
			for n in range(s):
				h = Header(br,bc,n)
				h.numRows = s
				curH.addRight(h)
				curH = curH.right
				curR = curH
				for r in range(int(br*s**.5),
				               int(br*s**.5+s**.5)):
					for c in range(int(bc*s**.5),
					               int(bc*s**.5+s**.5)):
						curR.addDown(boxM[r][c][n])
						curR = curR.down
						
	# Horizontal Linking
	for r in range(s):
		for c in range(s):
			for n in range(s):
				pn = posM[r][c][n]
				rn = rowM[r][c][n]
				cn = colM[r][c][n]
				bn = boxM[r][c][n]
				pn.addRight(rn)
				rn.addRight(cn)
				cn.addRight(bn)
	
	return root
	
if __name__ == '__main__':
	m = make(9)
	print(m)
