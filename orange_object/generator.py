import numpy as np
import random

def object_generator(shape,goal=None):
	object_map = np.zeros(shape, dtype=np.uint8)

	if goal==None:
		index = random.randint(0, shape[0]*shape[1]-1)
		row = index//shape[1]
		col = index%shape[1]
	else:
		row,col=goal

	object_map[row,col] = 1
	return object_map,row,col

if __name__ == "__main__":
	shape = (3,4)
	print(object_generator(shape))