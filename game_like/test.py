# -*- coding: utf-8 -*-
# @Time    : 2022/1/9 23:05
# @Author  : Kenny Zhou
# @FileName: test.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

# https://github.com/MAN1986/pyamaze/raw/main/Demos/demo.py

from pyamaze import maze,COLOR,agent
m=maze(64,32)
# m=maze(20,30)
# m.CreateMaze()
# m.CreateMaze(5,5,pattern='v',theme=COLOR.light)

#By default, the generated maze is Perfect Maze meaning just the one path from any cell to the goal cell.
# However, we can generate a maze with multiple paths by setting the optional argument loopPercent to some positive number.
# loopPercent set to highest value 100 means the maze generation algorithm will maximize the number of multiple paths for example as: m.CreateMaze(loopPercent=100)
m.CreateMaze(saveMaze=True)#loopPercent=100

# a=agent(m,5,4)
# print(a.x)
# print(a.y)
# print(a.position)


a=agent(m,15,15,footprints=True,filled=True,)
b=agent(m,5,5,footprints=True,color='red')
# c=agent(m,4,1,footprints=True,color='green',shape='arrow')

m.enableArrowKey(a)
m.enableWASD(b)

path2=[(5,4),(5,3),(4,3),(3,3),(3,4),(4,4)]
path3='WWNNES'

# l1=textLabel(m,'Total Cells',m.rows*m.cols)
# l1=textLabel(m,'Total Cells',m.rows*m.cols)
# l1=textLabel(m,'Total Cells',m.rows*m.cols)
# l1=textLabel(m,'Total Cells',m.rows*m.cols)

# m.tracePath({a:m.path,},delay=200,kill=True)#,b:path2,c:path3

m.run()