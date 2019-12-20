from Cell import Cell

from FieldHandlers import GetClosest, Method_OncomingWave, Method_OneBigWay
import numpy as np
import os, sys
from copy import copy, deepcopy

def PrintMatrix(field):
	#os.system('clear')
	os.system('cls')

	print('  |', end=' ')
	for i in range(len(field[0])):
		print(i%10, end=' ')
	print()
	print('_ |', end=' ')
	for i in range(len(field[0])):
		print('_', end=' ')
	print()

	for i, line in enumerate(field):
		print(i%10, end=' ')
		print('|', end=' ')
		for elem in line:
			if elem.type == 'cabel':
				print('W', end=' ')
			elif elem.type == 'wall':
				print('|', end=' ')
			elif elem.type == 'aim':
				print('A', end=' ')
			else:
				print('•', end=' ')
		print()

def GetAimCoords(field):
	aims_coords = []

	while True:
		PrintMatrix(field)
		print()
		print("Press Enter to finish")
		string = input("Input X and Y of Aim (\"X Y\"): ")
		if string == '':
			return (aims_coords)

		x, y = [int(i) for i in string.split() if i.isdigit()]
		aims_coords.append([y, x])
		field[y][x].type = 'aim'



def GetMatrix():
	field = []
	matrix = []
	with open('matrix.txt') as f:
		matrix = [list(map(int, row.split())) for row in f.readlines()]

	for y, line in enumerate(matrix):
		field_line = []
		for x, elem in enumerate(line):
			field_line.append(Cell('way',x, y))
			if elem == 7:
				field_line[-1].type='wall'
		field.append(field_line)

	return (field)


def main():
	aims_1d = []
	field_2d = GetMatrix()

	# Set Aims
	aims_coords = []
	aims_coords = GetAimCoords(field_2d)
	#aims_coords.append([0, 0])
	#aims_coords.append([0, 5])

	if len(aims_coords) < 2:
		sys.exit()

	for elem in aims_coords:
		aims_1d.append(field_2d[elem[0]][elem[1]])

	for i, elem in enumerate(aims_1d):
		elem.type = 'aim'
		elem.weight = 1

	# Connect the closest
	field_2d_Copy = deepcopy(field_2d)
	point1, point2 = GetClosest(aims_1d)
	
	way = Method_OncomingWave(field_2d_Copy, deepcopy(point1), deepcopy(point2))

	for elem in way:
		field_2d[elem.y][elem.x].weight = elem.weight
		field_2d[elem.y][elem.x].type = 'cabel'

	PrintMatrix(field_2d)

	# Connect anothers
	# Prepare
	print("\nPress Enter...", end = '')
	input()

	aims_1d.remove(point1)
	aims_1d.remove(point2)

	if len(aims_1d) < 1:
		sys.exit()

	# Start
	field_2d_Copy = deepcopy(field_2d)
	
	for i, elem in enumerate(way):
		way[i] = field_2d_Copy[elem.y][elem.x]

	field_2d_Copy[point1.y][point1.x].type = 'wall'
	field_2d_Copy[point2.y][point2.x].type = 'wall'

	ways = Method_OneBigWay(field_2d_Copy, way, aims_1d)

	for way in ways:
		for elem in way:
			field_2d[elem.y][elem.x].weight = elem.weight
			field_2d[elem.y][elem.x].type = 'cabel'


	PrintMatrix(field_2d)
	print("\nPress Enter...", end = '')
	input()

if __name__ == "__main__":
	main()