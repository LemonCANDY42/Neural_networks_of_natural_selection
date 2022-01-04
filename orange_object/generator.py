import numpy as np
import random

def object_generator(shape):
	object_map = np.zeros(shape, dtype=np.uint8)

	index = random.randint(0, shape[0]*shape[1]-1)

	row = index//shape[1]
	col = index%shape[1]
	print(index,row,col)
	object_map[row,col] = 1
	return object_map

if __name__ == "__main__":
	shape = (3,4)
	print(object_generator(shape))