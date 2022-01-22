# -*- coding: utf-8 -*-
# @Time    : 2022/1/22 15:37
# @Author  : Kenny Zhou
# @FileName: test.py.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
import numpy as np

from maze.core import *
if __name__ == "__main__":
	from maze.agent import Agent
	from neural.network.building import BuildingNetwork

	rows = 32
	cols = 32
	MG = Maze(num_rows=rows, num_cols=cols, type="twist",
						load_file='./maze/MAZE/2022-01-10 18:56:08.997395-(32, 32).npz')  # load_file="./MAZE/2022-01-10 18:20:26.823120-(5, 5).npz"

	a = Agent(MG, footprints=True, filled=True, )
	MG.enableArrowKey(a)
	MG.enableWASD(a)
	MG.enableMove(a)
	contour = Contour(MG.object_map)
	contour.draw()

	N = BuildingNetwork(input_shape=(1, 5), output_shape=(1, 4))
	# output = N.activation(input)
	# res = random.uniform(0.5, 2)
	# N.reward_punishment(res)

	move_list=['L','U','R','D']

	def close():
		global a
		global N
		global MG
		global move_list
		global contour
		input = MG.map[a.y-1,a.x-1]
		input[-1] = contour.map[a.y-1,a.x-1]

		out = N.activation(input)
		# if np.isnan(out[:,np.argmax(out, axis=1)[0]]):
		# 	move = random.choice(['L', 'R', 'U', 'D'])
		# else:
		# 	move = move_list[np.argmax(out, axis=1)[0]]
		move = move_list[np.argmax(out, axis=1)[0]]
		MG.randomMove(move)
		print(input,move,out)
		a.steps += 1
		N.reward_punishment(a.steps/10)#min(a.steps/5,100)
		if a.x == a.goal[0] and a.y == a.goal[1]:
			return True
		else:
			return False


	MG.run(close)

	print("总步数:", a.steps)