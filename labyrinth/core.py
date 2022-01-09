import numpy as np
from matplotlib import pyplot as plt
from build_laby_func import *
from path_searcher import *
from orange_object.generator import object_generator
from analysis.time_tools import time_keep
from numba import jit

class Labyrinth:
    """
        map的结构:
        [num_rows,num_cols,5]
        最后一个维度表示:
        为1代表可以走
                1 ↑
            0 ←     2 →
                3 ↓
        4 表示已经遍历

    """
    def __init__(self,num_rows,num_cols,type):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.shape = (self.num_rows,self.num_cols)
        self.object_map = object_generator(self.shape)
        self.image = np.zeros((self.num_rows * 10, self.num_cols * 10), dtype=np.uint8)
        if type == 'twist':
            self.build = build_twist
        else:
            self.build = build_tortuous

        self.map = self.build(self.num_rows, self.num_cols)

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

    def save_map(self):
        self.map_fig.savefig('./img/map.png', format='png', transparent=True, dpi=300, pad_inches=0)

    def draw_path(self):
        move_list,attempted_steps = solve_fill(self.num_rows, self.num_cols, self.map,object_map=self.object_map)
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

    def save_path(self):
        self.path_fig.savefig('./img/path.png', format='png', transparent=True, dpi=300, pad_inches=0)

    def draw(self, m, object_map=None):
        """
            绘制迷宫
        :param m:
        :type m:
        :return:
        :rtype:
        """
        for row in range(0, self.num_rows):
            for col in range(0, self.num_cols):
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


if __name__ == "__main__":
    # rows = int(input("Rows: "))
    # cols = int(input("Columns: "))
    rows = 128
    cols = 128
    MG = Labyrinth(num_rows=rows,num_cols=cols,type="twistN")

    MG.draw_map()
    MG.show()
    MG.draw_path()
    MG.show()
    MG.save_map()
    MG.save_path()
    a = MG.map
    b = MG.move_list

