# -*- coding: utf-8 -*-
# @Time    : 2022/1/10 15:45
# @Author  : Kenny Zhou
# @FileName: agent.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
import random,datetime,csv,os
from tkinter import *
from enum import Enum
from collections import deque
from setting import COLOR
from core import Maze


class Agent:
	'''
	The agents can be placed on the maze.
	They can represent the virtual object just to indcate the cell selected in Maze.
	Or they can be the physical agents (like robots)
	They can have two shapes (square or arrow)
	'''

	def __init__(self, parentMaze, y=None, x=None, shape='square', goal=None, filled=False, footprints=False,
							 color: COLOR = COLOR.blue):
		'''
		parentmaze-->  The maze on which agent is placed.
		x,y-->  Position of the agent i.e. cell inside which agent will be placed
						Default value is the lower right corner of the Maze
		shape-->    square or arrow (as string)
		goal-->     Default value is the goal of the Maze
		filled-->   For square shape, filled=False is a smaller square
								While filled =True is a biiger square filled in complete Cell
								This option doesn't matter for arrow shape.
		footprints-->   When the aganet will move to some other cell, its footprints
										on the previous cell can be placed by making this True
		color-->    Color of the agent.

		_orient-->  You don't need to pass this
								It is used with arrow shape agent to shows it turning
		position--> You don't need to pass this
								This is the cell (x,y)
		_head-->    You don't need to pass this
								It is actually the agent.
		_body-->    You don't need to pass this
								Tracks the body of the agent (the previous positions of it)
		'''
		self._parentMaze = parentMaze
		self.color = color
		if (isinstance(color, str)):
			if (color in COLOR.__members__):
				self.color = COLOR[color]
			else:
				raise ValueError(f'{color} is not a valid COLOR!')
		self.filled = filled
		self.shape = shape
		self._orient = 0
		self.footprints = footprints
		self._parentMaze._agents.append(self)
		if goal == None:
			self.goal = self._parentMaze._goal
		else:
			self.goal = goal
		self._body = []
		if x is None: x = self.goal[0]
		if y is None: y = self.goal[1]
		self.x = x + 1
		self.y = y + 1
		self.position = (self.x, self.y)

	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, newX):
		self._x = newX

	@property
	def y(self):
		return self._y

	@y.setter
	def y(self, newY):
		self._y = newY
		w = self._parentMaze._cell_width
		x = self.x * w - w + self._parentMaze._LabWidth
		y = self.y * w - w + self._parentMaze._LabWidth
		if self.shape == 'square':
			if self.filled:
				self._coord = (y, x, y + w, x + w)
			else:
				self._coord = (y + w / 2.5, x + w / 2.5, y + w / 2.5 + w / 4, x + w / 2.5 + w / 4)
		else:
			self._coord = (y + w / 2, x + 3 * w / 9, y + w / 2, x + 3 * w / 9 + w / 4)

		if (hasattr(self, '_head')):
			if self.footprints is False:
				self._parentMaze._canvas.delete(self._head)
			else:
				if self.shape == 'square':
					self._parentMaze._canvas.itemconfig(self._head, fill=self.color.value[1], outline="")
					self._parentMaze._canvas.tag_raise(self._head)
					try:
						self._parentMaze._canvas.tag_lower(self._head, 'ov')
					except:
						pass
					if self.filled:
						lll = self._parentMaze._canvas.coords(self._head)
						oldcell = (round(((lll[1] - 26) / self._parentMaze._cell_width) + 1),
											 round(((lll[0] - 26) / self._parentMaze._cell_width) + 1))
						self._parentMaze._redrawCell(*oldcell, self._parentMaze.theme)
				else:
					self._parentMaze._canvas.itemconfig(self._head, fill=self.color.value[1])  # ,outline='gray70')
					self._parentMaze._canvas.tag_raise(self._head)
					try:
						self._parentMaze._canvas.tag_lower(self._head, 'ov')
					except:
						pass
				self._body.append(self._head)
			if not self.filled or self.shape == 'arrow':
				if self.shape == 'square':
					self._head = self._parentMaze._canvas.create_rectangle(*self._coord, fill=self.color.value[0],
																																 outline='')  # stipple='gray75'
					try:
						self._parentMaze._canvas.tag_lower(self._head, 'ov')
					except:
						pass
				else:
					self._head = self._parentMaze._canvas.create_line(*self._coord, fill=self.color.value[0], arrow=FIRST,
																														arrowshape=(3 / 10 * w, 4 / 10 * w,
																																				4 / 10 * w))  # ,outline=self.color.name)
					try:
						self._parentMaze._canvas.tag_lower(self._head, 'ov')
					except:
						pass
					o = self._orient % 4
					if o == 1:
						self._RCW()
						self._orient -= 1
					elif o == 3:
						self._RCCW()
						self._orient += 1
					elif o == 2:
						self._RCCW()
						self._RCCW()
						self._orient += 2
			else:
				self._head = self._parentMaze._canvas.create_rectangle(*self._coord, fill=self.color.value[0],
																															 outline='')  # stipple='gray75'
				try:
					self._parentMaze._canvas.tag_lower(self._head, 'ov')
				except:
					pass
				self._parentMaze._redrawCell(self.x, self.y, theme=self._parentMaze.theme)
		else:
			self._head = self._parentMaze._canvas.create_rectangle(*self._coord, fill=self.color.value[0],
																														 outline='')  # stipple='gray75'
			try:
				self._parentMaze._canvas.tag_lower(self._head, 'ov')
			except:
				pass
			self._parentMaze._redrawCell(self.x, self.y, theme=self._parentMaze.theme)

	@property
	def position(self):
		return (self.x, self.y)

	@position.setter
	def position(self, newpos):
		self.x = newpos[0]
		self.y = newpos[1]
		self._position = newpos

	def _RCCW(self):
		'''
		To Rotate the agent in Counter Clock Wise direction
		'''

		def pointNew(p, newOrigin):
			return (p[0] - newOrigin[0], p[1] - newOrigin[1])

		w = self._parentMaze._cell_width
		x = self.x * w - w + self._parentMaze._LabWidth
		y = self.y * w - w + self._parentMaze._LabWidth
		cent = (y + w / 2, x + w / 2)
		p1 = pointNew((self._coord[0], self._coord[1]), cent)
		p2 = pointNew((self._coord[2], self._coord[3]), cent)
		p1CW = (p1[1], -p1[0])
		p2CW = (p2[1], -p2[0])
		p1 = p1CW[0] + cent[0], p1CW[1] + cent[1]
		p2 = p2CW[0] + cent[0], p2CW[1] + cent[1]
		self._coord = (*p1, *p2)
		self._parentMaze._canvas.coords(self._head, *self._coord)
		self._orient = (self._orient - 1) % 4

	def _RCW(self):
		'''
		To Rotate the agent in Clock Wise direction
		'''

		def pointNew(p, newOrigin):
			return (p[0] - newOrigin[0], p[1] - newOrigin[1])

		w = self._parentMaze._cell_width
		x = self.x * w - w + self._parentMaze._LabWidth
		y = self.y * w - w + self._parentMaze._LabWidth
		cent = (y + w / 2, x + w / 2)
		p1 = pointNew((self._coord[0], self._coord[1]), cent)
		p2 = pointNew((self._coord[2], self._coord[3]), cent)
		p1CW = (-p1[1], p1[0])
		p2CW = (-p2[1], p2[0])
		p1 = p1CW[0] + cent[0], p1CW[1] + cent[1]
		p2 = p2CW[0] + cent[0], p2CW[1] + cent[1]
		self._coord = (*p1, *p2)
		self._parentMaze._canvas.coords(self._head, *self._coord)
		self._orient = (self._orient + 1) % 4

	def moveRight(self, event):
		if self._parentMaze.map[self.x-1, self.y-1][2] == 1:
			self.y = self.y + 1

	def moveLeft(self, event):
		if self._parentMaze.map[self.x-1, self.y-1][0] == 1:
			self.y = self.y - 1

	def moveUp(self, event):
		if self._parentMaze.map[self.x-1, self.y-1][1] == 1:
			self.x = self.x - 1
			self.y = self.y

	def moveDown(self, event):
		if self._parentMaze.map[self.x-1, self.y-1][3] == 1:
			self.x = self.x + 1
			self.y = self.y