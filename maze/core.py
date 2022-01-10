# -*- coding: utf-8 -*-
# @Time    : 2022/1/9 23:05
# @Author  : Kenny Zhou
# @FileName: test.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
import numpy as np
from matplotlib import pyplot as plt
from build_laby_func import *
from setting import COLOR
from path_searcher import *
from orange_object.generator import object_generator
from analysis.time_tools import time_keep
from numba import jit
import random,datetime,csv,os
from tkinter import *

class textLabel:
    '''
    This class is to create Text Label to show different results on the window.
    '''
    def __init__(self,parentMaze,title,value):
        '''
        parentmaze-->   The maze on which Label will be displayed.
        title-->        The title of the value to be displayed
        value-->        The value to be displayed
        '''
        self.title=title
        self._value=value
        self._parentMaze=parentMaze
        # self._parentMaze._labels.append(self)
        self._var=None
        self.drawLabel()
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,v):
        self._value=v
        self._var.set(f'{self.title} : {v}')
    def drawLabel(self):
        self._var = StringVar()
        self.lab = Label(self._parentMaze._canvas, textvariable=self._var, bg="white", fg="black",font=('Helvetica bold',12),relief=RIDGE)
        self._var.set(f'{self.title} : {self.value}')
        self.lab.pack(expand = True,side=LEFT,anchor=NW)

class Maze:
    """
        map的结构:
        [rows,cols,5]
        最后一个维度表示:
        为1代表可以走
                1 ↑
            0 ←     2 →
                3 ↓
        4 表示已经遍历

        _agents-->  A list of aganets on the maze

    """
    def __init__(self,num_rows,num_cols,type,goal=None,load_file=None):
        self._win=None
        self._canvas=None
        self.map_fig = None
        self.path_fig = None
        self._agents = []

        if load_file == None:
            self.rows = num_rows
            self.cols = num_cols

            self.shape = (self.rows, self.cols)
            self.object_map,object_row,object_col = object_generator(self.shape,goal=goal)
            self._goal = (object_row,object_col)


            if type == 'twist':
                self.build = build_twist
            else:
                self.build = build_tortuous

            self.map = self.build(self.rows, self.cols)
        else:
            self._load_maze(file_path=load_file)
            self.rows,self.cols,_state = self.map.shape

            self.shape = (self.rows, self.cols)

            self._goal = (np.where(self.object_map==1)[0][0],np.where(self.object_map==1)[1][0])

        self.image = np.zeros((self.rows * 10, self.cols * 10), dtype=np.uint8)

        self._create_win()

    def draw_map(self):
        self.draw(self.map,object_map=self.object_map)
        plt.imshow(self.image, cmap='hot')
        self.map_fig = plt.gcf()
        self.map_fig.set_size_inches(cols / 10 / 3, rows / 10 / 3)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)

    def show(self):
        plt.show()

    def save_maze(self,file_path=None):
        if file_path==None: file_path=f'./MAZE/{datetime.datetime.now()}-{str(self.shape)}.npz'
        np.savez_compressed(file_path,map=self.map,object_map=self.object_map)

    def _load_maze(self,file_path):
        npzfile = np.load(f'{file_path}')
        self.map = npzfile['map']
        self.object_map = npzfile['object_map']

    def save_pic(self,dir_path='./img/'):

        self.draw_map()
        self.map_fig.savefig(dir_path+f'{datetime.datetime.now()}-map.png', format='png', transparent=True, dpi=300, pad_inches=0)
        self.draw_path()
        self.path_fig.savefig(dir_path+f'{datetime.datetime.now()}-path.png', format='png', transparent=True, dpi=300, pad_inches=0)

    def draw_path(self):
        move_list,attempted_steps = solve_fill(self.rows, self.cols, self.map, object_map=self.object_map)
        step = len(move_list)
        print(f"总步数：{step},尝试次数：{attempted_steps}")
        self.path_image = self.find_path(move_list)

        plt.imshow(self.path_image, cmap='hot')
        self.path_fig = plt.gcf()
        self.path_fig.set_size_inches(cols / 10 / 3, rows / 10 / 3)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)

    def draw(self, m, object_map=None):
        """
            绘制迷宫
        :param m:
        :type m:
        :return:
        :rtype:
        """
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                cell_data = m[row, col]
                for i in range(10 * row + 2, 10 * row + 8):
                    self.image[i, range(10 * col + 2, 10 * col + 8)] = 255
                if cell_data[0] == 1:
                    # 左
                    self.image[range(10 * row + 2, 10 * row + 8), 10 * col] = 255
                    self.image[range(10 * row + 2, 10 * row + 8), 10 * col + 1] = 255
                if cell_data[1] == 1:
                    # 上
                    self.image[10 * row, range(10 * col + 2, 10 * col + 8)] = 255
                    self.image[10 * row + 1, range(10 * col + 2, 10 * col + 8)] = 255
                if cell_data[2] == 1:
                    # 右
                    self.image[range(10 * row + 2, 10 * row + 8), 10 * col + 9] = 255
                    self.image[range(10 * row + 2, 10 * row + 8), 10 * col + 8] = 255
                if cell_data[3] == 1:
                    # 下
                    self.image[10 * row + 9, range(10 * col + 2, 10 * col + 8)] = 255
                    self.image[10 * row + 8, range(10 * col + 2, 10 * col + 8)] = 255
        if object_map is not None:
            a = np.argwhere(object_map == 1)
            if len(a):
                row,col = a[0]
                for i in range(6):
                    self.image[range(10 * row + 2, 10 * row + 8), 10 * col + i + 2] = 127
        return self.image

    def find_path(self, move_list):
        """
            绘制路径
        :param move_list:
        :type move_list:
        :return:
        :rtype:
        """
        self.move_list = move_list
        row, col = (0, 0)
        path_image = self.image.copy()
        path_image[range(10 * row + 2, 10 * row + 8), 10 * col] = 127
        path_image[range(10 * row + 2, 10 * row + 8), 10 * col + 1] = 127
        for i in range(len(move_list) + 1):
            for x in range(10 * row + 2, 10 * row + 8):
                path_image[x, range(10 * col + 2, 10 * col + 8)] = 127
            if i > 0:
                go = move_list[i - 1]
                if go == 'L':
                    path_image[range(10 * row + 2, 10 * row + 8), 10 * col + 9] = 127
                    path_image[range(10 * row + 2, 10 * row + 8), 10 * col + 8] = 127
                elif go == 'U':
                    path_image[10 * row + 9, range(10 * col + 2, 10 * col + 8)] = 127
                    path_image[10 * row + 8, range(10 * col + 2, 10 * col + 8)] = 127
                elif go == 'R':
                    path_image[range(10 * row + 2, 10 * row + 8), 10 * col] = 127
                    path_image[range(10 * row + 2, 10 * row + 8), 10 * col + 1] = 127
                elif go == 'D':
                    path_image[10 * row, range(10 * col + 2, 10 * col + 8)] = 127
                    path_image[10 * row + 1, range(10 * col + 2, 10 * col + 8)] = 127
            if i >= len(move_list):
                break
            go = move_list[i]
            if go == 'L':
                path_image[range(10 * row + 2, 10 * row + 8), 10 * col] = 127
                path_image[range(10 * row + 2, 10 * row + 8), 10 * col + 1] = 127
            elif go == 'U':
                path_image[10 * row, range(10 * col + 2, 10 * col + 8)] = 127
                path_image[10 * row + 1, range(10 * col + 2, 10 * col + 8)] = 127
            elif go == 'R':
                path_image[range(10 * row + 2, 10 * row + 8), 10 * col + 9] = 127
                path_image[range(10 * row + 2, 10 * row + 8), 10 * col + 8] = 127
            elif go == 'D':
                self.image[10 * row + 9, range(10 * col + 2, 10 * col + 8)] = 127
                self.image[10 * row + 8, range(10 * col + 2, 10 * col + 8)] = 127
            if go == 'L':
                col = col - 1
            elif go == 'U':
                row = row - 1
            elif go == 'R':
                col = col + 1
            elif go == 'D':
                row = row + 1
        for i in range(6):
            path_image[range(10 * row + 2, 10 * row + 8), 10 * col + i+ 2] = 200
        # path_image[range(10 * row + 2, 10 * row + 16), 10 * col + 8] = 200
        return path_image

    def _create_win(self,theme=COLOR.dark):
        if(isinstance(theme,str)):
            if(theme in COLOR.__members__):
                self.theme=COLOR[theme]
            else:
                raise ValueError(f'{theme} is not a valid theme COLOR!')

        self.theme=theme
        self._drawMaze(theme=self.theme)

    def _drawMaze(self, theme):
        '''
        Creation of Tkinter window and maze lines
        '''

        self._LabWidth = 26  # Space from the top for Labels
        self._win = Tk()
        self._win.state('zoomed')
        self._win.title('MAZE WORLD by Kenny')

        scr_width = self._win.winfo_screenwidth()
        scr_height = self._win.winfo_screenheight()
        self._win.geometry(f"{scr_width}x{scr_height}+0+0")
        self._canvas = Canvas(width=scr_width, height=scr_height, bg=theme.value[0])  # 0,0 is top left corner
        self._canvas.pack(expand=YES, fill=BOTH)
        # Some calculations for calculating the width of the maze cell
        k = 3.25
        if self.rows >= 95 and self.cols >= 95:
            k = 0
        elif self.rows >= 80 and self.cols >= 80:
            k = 1
        elif self.rows >= 70 and self.cols >= 70:
            k = 1.5
        elif self.rows >= 50 and self.cols >= 50:
            k = 2
        elif self.rows >= 35 and self.cols >= 35:
            k = 2.5
        elif self.rows >= 22 and self .cols >= 22:
            k = 3
        self._cell_width = round(min(((scr_height - self.rows - k * self._LabWidth) / (self.rows)),
                                     ((scr_width - self.cols - k * self._LabWidth) / (self.cols)), 90), 3)

        # Creating Maze lines
        if self._win is not None:
            if self.map is not None:
                for row in range(self.rows):
                    for col in range(self.cols):
                        w = self._cell_width
                        x = col
                        y = row
                        x+=1
                        y+=1
                        x = x * w - w + self._LabWidth
                        y = y * w - w + self._LabWidth
                        if self.map[col][row][2] == 0:
                            l = self._canvas.create_line(y + w, x, y + w, x + w, width=2, fill=theme.value[1], tag='line')
                        if self.map[col][row][0] == 0:
                            l = self._canvas.create_line(y, x, y, x + w, width=2, fill=theme.value[1], tag='line')
                        if self.map[col][row][1] == 0:
                            l = self._canvas.create_line(y, x, y + w, x, width=2, fill=theme.value[1], tag='line')
                        if self.map[col][row][3] == 0:
                            l = self._canvas.create_line(y, x + w, y + w, x + w, width=2, fill=theme.value[1], tag='line')

    def _redrawCell(self, x, y, theme):
        '''
        To redraw a cell.
        With Full sized square agent, it can overlap with maze lines
        So the cell is redrawn so that cell lines are on top
        '''
        w = self._cell_width
        cell = (x-1, y-1)
        x = x * w - w + self._LabWidth
        y = y * w - w + self._LabWidth
        if self.map[cell][2] == 0:
            self._canvas.create_line(y + w, x, y + w, x + w,width=2,fill=theme.value[1])
        if self.map[cell][0] == 0:
            self._canvas.create_line(y, x, y, x + w,width=2,fill=theme.value[1])
        if self.map[cell][1] == 0:
            self._canvas.create_line(y, x, y + w, x,width=2,fill=theme.value[1])
        if self.map[cell][3] == 0:
            self._canvas.create_line(y, x + w, y + w, x + w,width=2,fill=theme.value[1])

    def enableArrowKey(self, a):
        '''
        To control an agent a with Arrow Keys
        '''
        self._win.bind('<Left>', a.moveLeft)
        self._win.bind('<Right>', a.moveRight)
        self._win.bind('<Up>', a.moveUp)
        self._win.bind('<Down>', a.moveDown)

    def enableWASD(self, a):
        '''
        To control an agent a with keys W,A,S,D
        '''
        self._win.bind('<a>', a.moveLeft)
        self._win.bind('<d>', a.moveRight)
        self._win.bind('<w>', a.moveUp)
        self._win.bind('<s>', a.moveDown)


    def run(self):
        '''
        Finally to run the Tkinter Main Loop
        '''
        self._win.mainloop()

if __name__ == "__main__":
    from agent import Agent
    # rows = int(input("Rows: "))
    # cols = int(input("Columns: "))
    rows = 32
    cols = 32
    MG = Maze(num_rows=rows, num_cols=cols, type="twist",load_file='./MAZE/2022-01-10 18:56:08.997395-(32, 32).npz')#load_file="./MAZE/2022-01-10 18:20:26.823120-(5, 5).npz"

    b = Agent(MG, footprints=True, filled=True,)
    MG.enableArrowKey(b)
    MG.enableWASD(b)

    # MG.draw_map()
    # MG.show()
    # MG.draw_path()
    # MG.show()

    # MG.save_pic()
    # MG.save_maze()

    MG.run()
    a = MG.map