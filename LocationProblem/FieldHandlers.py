import math
import os
from Cell import Cell

def GetLengthBetween2Points(point1, point2):
	return (math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2))

def GetClosest(aims_1d):
	point1 = aims_1d[0]
	point2 = aims_1d[1]
	minLen = GetLengthBetween2Points(point1, point2)
	
	for i in range(len(aims_1d)):
		for j in range(i + 1, len(aims_1d)):
			newLen = GetLengthBetween2Points(aims_1d[i], aims_1d[j])
			if minLen > newLen:
				minLen = newLen
				point1 = aims_1d[i]
				point2 = aims_1d[j]

	return (point1, point2)

def GetClosest_ForPoint(aims_1d, point, exclude):
	aims = aims_1d
	for elem in exclude:
		aims.remove(elem)
	
	pointClosest = aims[0]
	minLen = GetLengthBetween2Points(point, aims[0])

	for i in range(1, len(aims)):
		newLen = GetLengthBetween2Points(point, aims[i])
		if minLen > newLen:
			minLen = newLen
			pointClosest = aims[i]

	return (pointClosest)


############################################################################
def PrintMatrix(field):
	#os.system('clear')
	os.system('cls')
	for line in field:
		for elem in line:
			if elem.type == 'wall':
				print('|', end=' ')
			else:
				print(elem.weight, end=' ')
		print()
############################################################################	Peer-to-Peer

def CreateTheWay(point1, point2, field):
	way1 = [point1]
	way2 = [point2]

	while True:
		if way1[0].previous.type == 'aim':
			way1.remove(way1[0])
			break
		way1.insert(0, way1[0].previous)

	while True:
		if (way2[len(way2) - 1].type == 'aim') or (way2[len(way2) - 1].previous.type == 'aim'):
			field[way2[len(way2) - 1].y][way2[len(way2) - 1].x].type = 'wall'
			way2.remove(way2[len(way2) - 1])
			break
		way2.append(way2[len(way2) - 1].previous)

	return way1 + way2

def CheckCell(field, pointPrev, point):
	if (pointPrev.type == '1' and point.type == '2') or (pointPrev.type == '2' and point.type == '1'):
		return ('finish')
	if (point.x == pointPrev.previous.x and point.y == pointPrev.previous.y) or (point.weight != 0 and point.weight <= pointPrev.weight):
		return ('the_same')


	if (abs(point.x - pointPrev.previous.x) == 2) or (abs(point.y - pointPrev.previous.y) == 2):
		if point.weight == pointPrev.weight + 1:
			return ('the_same')
		point.weight = pointPrev.weight + 1
	else:
		if (point.weight == pointPrev.weight + 1) or (point.weight == pointPrev.weight + 2):
			return ('the_same')
		point.weight = pointPrev.weight + 2
	
	return 'new_step'

def NearestCells(field, point, type):
	nextCells = []

	#	Left
	if point.x - 1 >= 0:
		if field[point.y][point.x - 1].type != 'wall':
			if type == 'wave':
				flagType = CheckCell_Wave(field, point, field[point.y][point.x - 1])
			else:
				flagType = CheckCell(field, point, field[point.y][point.x - 1])
			if flagType == 'finish':
				nextCells = CreateTheWay(point, field[point.y][point.x - 1], field)
				return (nextCells, True)
			if flagType != 'the_same':
				field[point.y][point.x - 1].previous = point
				field[point.y][point.x - 1].type = point.type
				nextCells.append(field[point.y][point.x - 1])
	#	Right
	if point.x + 1 < len(field[0]):
		if field[point.y][point.x + 1].type != 'wall':
			if type == 'wave':
				flagType = CheckCell_Wave(field, point, field[point.y][point.x + 1])
			else:
				flagType = CheckCell(field, point, field[point.y][point.x + 1])
			if flagType == 'finish':
				nextCells = CreateTheWay(point, field[point.y][point.x + 1], field)
				return (nextCells, True)
			if flagType != 'the_same':
				field[point.y][point.x + 1].previous = point
				field[point.y][point.x + 1].type = point.type
				nextCells.append(field[point.y][point.x + 1])
	
	#	Up
	if point.y - 1 >= 0:
		if field[point.y - 1][point.x].type != 'wall':
			if type == 'wave':
				flagType = CheckCell_Wave(field, point, field[point.y - 1][point.x])
			else:
				flagType = CheckCell(field, point, field[point.y - 1][point.x])
			if flagType == 'finish':
				nextCells = CreateTheWay(point, field[point.y - 1][point.x], field)
				return (nextCells, True)
			if flagType != 'the_same':
				field[point.y - 1][point.x].previous = point
				field[point.y - 1][point.x].type = point.type
				nextCells.append(field[point.y - 1][point.x])
	#	Down
	if point.y + 1 < len(field):
		if field[point.y + 1][point.x].type != 'wall':
			if type == 'wave':
				flagType = CheckCell_Wave(field, point, field[point.y + 1][point.x])
			else:
				flagType = CheckCell(field, point, field[point.y + 1][point.x])
			if flagType == 'finish':
				nextCells = CreateTheWay(point, field[point.y + 1][point.x], field)
				return (nextCells, True)
			if flagType != 'the_same':
				field[point.y + 1][point.x].previous = point
				field[point.y + 1][point.x].type = point.type
				nextCells.append(field[point.y + 1][point.x])

	return (nextCells, False)

def Method_OncomingWave(field, point1, point2):
	point1.type = '1'
	point1.previous = Cell()
	point1.previous.type = 'aim'
	point1.previous.x = point1.x - 2
	point1.previous.y = point1.y - 2

	point2.type = '2'
	point2.previous = Cell()
	point2.previous.type = 'aim'
	point2.previous.x = point2.x - 2
	point2.previous.y = point2.y - 2

	nextView = []
	curView = []

	# Prepare
	nextCells, flagFinish = NearestCells(field, point1, 'line')
	PrintMatrix(field)
	if flagFinish:
		return nextCells
	curView = curView + nextCells

	nextCells, flagFinish = NearestCells(field, point2, 'line')
	PrintMatrix(field)
	if flagFinish:
		return nextCells
	curView = curView + nextCells

	# Search

	while True:
		for elem in curView:
			nextCells, flagFinish = NearestCells(field, elem, 'line')
			PrintMatrix(field)
			if flagFinish:
				return nextCells
			nextView = nextView + nextCells
		if (curView == nextView) or nextView == []:
			return []
		curView = nextView
		nextView = []

############################################################################	Wave-to-Peers

def CheckCell_Wave(field, pointPrev, point):
	if (point.type == 'aim'):
		return ('finish')
	if (point.x == pointPrev.previous.x and point.y == pointPrev.previous.y) or (point.weight != 0 and point.weight <= pointPrev.weight):
		return ('the_same')


	if (abs(point.x - pointPrev.previous.x) == 2) or (abs(point.y - pointPrev.previous.y) == 2):
		if point.weight == pointPrev.weight + 1:
			return ('the_same')
		point.weight = pointPrev.weight + 1
	else:
		if (point.weight == pointPrev.weight + 1) or (point.weight == pointPrev.weight + 2):
			return ('the_same')
		point.weight = pointPrev.weight + 2
	
	return 'new_step'

def Method_OneBigWay(field, way, aims):
	ways = []
	aims_count = len(aims)

	nextView = []
	curView = way

	# Prepare
	for elem in curView:
		elem.weight = 1
		elem.previous = Cell()
		elem.previous.type = 'aim'
		elem.previous.x = elem.x - 2
		elem.previous.y = elem.y - 2

	# Search
	PrintMatrix(field)
	while True:
		for elem in curView:
			nextCells, flagFinish = NearestCells(field, elem, 'wave')
			PrintMatrix(field)
			if flagFinish:
				ways.append(nextCells)
				aims_count = aims_count - 1
				if aims_count == 0 : 
					return ways
			nextView = nextView + nextCells
		if (curView == nextView) or nextView == []:
			return []
		curView = nextView
		nextView = []