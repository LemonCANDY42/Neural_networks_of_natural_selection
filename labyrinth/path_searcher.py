# -*- coding: utf-8 -*-
# @Time    : 2022/1/9 23:05
# @Author  : Kenny Zhou
# @FileName: test.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
import random

def solve_fill(num_rows, num_cols, m, object_map=None):  # 填坑法
    map_arr = m.copy()	# 拷贝一份迷宫来填坑
    map_arr[0, 0, 0] = 0
    map_arr[num_rows-1, num_cols-1, 2] = 0
    move_list = []
    xy_list = []
    r, c = (0, 0)
    attempted_steps = 0
    while True:
        if object_map is None:
            if (r == num_rows-1) and (c == num_cols-1):
                break
        else:
            if object_map[r,c] == 1:
                break
        attempted_steps += 1
        xy_list.append((r, c))
        wall = map_arr[r, c]
        way = []
        if wall[0] == 1:
            way.append('L')
        if wall[1] == 1:
            way.append('U')
        if wall[2] == 1:
            way.append('R')
        if wall[3] == 1:
            way.append('D')
        if len(way) == 0:
            return False
        elif len(way) == 1:	# 在坑中
            go = way[0]
            move_list.append(go)
            if go == 'L':	# 填坑
                map_arr[r, c, 0] = 0
                c = c - 1
                map_arr[r, c, 2] = 0
            elif go == 'U':
                map_arr[r, c, 1] = 0
                r = r - 1
                map_arr[r, c, 3] = 0
            elif go == 'R':
                map_arr[r, c, 2] = 0
                c = c + 1
                map_arr[r, c, 0] = 0
            elif go == 'D':
                map_arr[r, c, 3] = 0
                r = r + 1
                map_arr[r, c, 1] = 0
        else:
            if len(move_list) != 0:	# 不在坑中
                come = move_list[len(move_list)-1]
                if come == 'L':
                    if 'R' in way:
                        way.remove('R')
                elif come == 'U':
                    if 'D' in way:
                        way.remove('D')
                elif come == 'R':
                    if 'L' in way:
                        way.remove('L')
                elif come == 'D':
                    if 'U' in way:
                        way.remove('U')
            go = random.choice(way)	# 随机选一个方向走
            move_list.append(go)
            if go == 'L':
                c = c - 1
            elif go == 'U':
                r = r - 1
            elif go == 'R':
                c = c + 1
            elif go == 'D':
                r = r + 1
    r_list = xy_list.copy()
    r_list.reverse()	# 行动坐标记录的反转
    i = 0
    while i < len(xy_list)-1:	# 去掉重复的移动步骤
        j = (len(xy_list)-1) - r_list.index(xy_list[i])
        if i != j:	# 说明这两个坐标之间的行动步骤都是多余的，因为一顿移动回到了原坐标
            del xy_list[i:j]
            del move_list[i:j]
            r_list = xy_list.copy()
            r_list.reverse()
        i = i + 1
    return move_list,attempted_steps

def solve_backtrack(num_rows, num_cols, map_arr):  # 回溯法
    move_list = ['R']
    m = 1	# 回溯点组号
    mark = []
    r, c = (0, 0)
    attempted_steps = 0
    while True:
        attempted_steps += 1
        if (r == num_rows-1) and (c == num_cols-1):
            break
        wall = map_arr[r, c]
        way = []
        if wall[0] == 1:
            way.append('L')
        if wall[1] == 1:
            way.append('U')
        if wall[2] == 1:
            way.append('R')
        if wall[3] == 1:
            way.append('D')
        come = move_list[len(move_list) - 1]
        if come == 'L':
            way.remove('R')
        elif come == 'U':
            way.remove('D')
        elif come == 'R':
            way.remove('L')
        elif come == 'D':
            way.remove('U')
        while way:
            mark.append((r, c, m, way.pop()))	# 记录当前坐标和可行移动方向
        if mark:
            r, c, m, go = mark.pop()
            del move_list[m:]	# 删除回溯点之后的移动
        else:
            return False
        m = m + 1
        move_list.append(go)
        if go == 'L':
            c = c - 1
        elif go == 'U':
            r = r - 1
        elif go == 'R':
            c = c + 1
        elif go == 'D':
            r = r + 1
    del move_list[0]
    return move_list,attempted_steps
