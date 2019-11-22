'''
THIS IS A FUNCTION TO CONVERT THE ROOM AND MAZE ENVIRONMENT
'''
import numpy as np
import math
insName = 'dr_dungeon.map'
insName = 'bootybay.map'
insName = 'ht_chantry.map'
insName = '16room_000.map'
insName = '8room_000.map'
insName = 'maze512-8-8.map'
fileName  = './/originMapData//' + insName

obstacleLst = []
with open(fileName) as mapData:
    lines = mapData.readlines()
    for line in lines:
        lineData = line.split()
        if len(lineData) == 1:
            if 'map' == lineData[0]:
                mat = np.zeros((mat_height,mat_width),dtype = int)
                rowInd = 0
            if '.' in lineData[0] or '@' in lineData[0]:
                # mat_width = int(lineData[1])
                for i,unit in enumerate(lineData[0]):
                    if unit == '.':
                        mat[rowInd][i] = 0
                        obstacleLst.append(0)
                    if unit == '@':
                        mat[rowInd][i] = 1
                        obstacleLst.append(1)
                    if unit == 'T':
                        obstacleLst.append(1)
                        mat[rowInd][i] = 1
                    if unit == 'W':
                        obstacleLst.append(1)
                        mat[rowInd][i] = 1
                    if unit == 'S':
                        mat[rowInd][i] = 0
                        obstacleLst.append(0)
                rowInd += 1
                # print(lineData)
        if len(lineData) == 2:
            if lineData[0] == 'height':
                mat_height = int(lineData[1])
            if lineData[0] == 'width':
                mat_width = int(lineData[1])
'''
get date from the origin map 
'''
from PIL import Image
# import numpy as np
# pixels  = []
# for row in mat:
#     unit = []
#     for x in row:
#         if x == 1:
#             unit.append((0,0,0))
#         else:
#             unit.append((255,255,255))
#     pixels.append(unit)
# # Convert the pixels into an array using numpy
# array = np.array(pixels, dtype=np.uint8)
# # Use PIL to create an image from the new array of pixels
# new_image = Image.fromarray(array)
# new_image.save('new.png')

typeBoolean = True
'''
False for the obstacle env
True for the room and maze env
'''

if typeBoolean:
    rowNum = 100
    colNum = 100
    pixels = []
    coarseMat = np.zeros((rowNum, colNum), dtype=int)
    for rowInd, row in enumerate(mat):
        unit = []
        if rowInd >= rowNum:
            break
        for colInd, cell in enumerate(row):
            if colInd >= colNum:
                break
            if cell == 1:
                unit.append((0, 0, 0))
                coarseMat[rowInd][colInd] = 1
                # print(rowInd, colInd)
            else:
                unit.append((255, 255, 255))
        pixels.append(unit)
    # array = np.array(pixels, dtype=np.uint8)
    # # Use PIL to create an image from the new array of pixels
    # new_image = Image.fromarray(array)
    # new_image.save('new_2.png')
else:
    coarseMatCellSize = 2
    def containOb(i: int, j: int, mat):
        for p in range(i, i + coarseMatCellSize):
            for q in range(j, j + coarseMatCellSize):
                if mat[i][j] == 1:
                    return True
        return False
    coarseMatRowNum = math.floor(mat.shape[0] / coarseMatCellSize)
    coarseMatColNum = math.floor(mat.shape[1] / coarseMatCellSize)
    coarseMat = np.zeros((coarseMatRowNum, coarseMatColNum), dtype=int)
    for i in range(0, mat.shape[0] - coarseMatCellSize, coarseMatCellSize):
        for j in range(0, mat.shape[1] - coarseMatCellSize, coarseMatCellSize):
            if containOb(i, j, mat):
                coarseMat[int(i / coarseMatCellSize)][int(j / coarseMatCellSize)] = 1



def getNeighbor(envMat,lst = (0,0),row =20, col =20):
    # print(lst)
    resLst = []
    #left
    lstLeft = (lst[0]-1,lst[1])
    if(lstLeft[0]>=0):
        if(envMat[lstLeft[0]][lstLeft[1]]== 0):
            resLst.append(lstLeft)
    #right
    lstRight = (lst[0]+1,lst[1])
    if(lstRight[0]<row):
        if(envMat[lstRight[0]][lstRight[1]]== 0):
            resLst.append(lstRight)
    #top
    lstTop = (lst[0],lst[1]+1)
    if(lstTop[1]<col):
        if(envMat[lstTop[0]][lstTop[1]]== 0):
            resLst.append(lstTop)
    #bottom
    lstBottom = (lst[0],lst[1]-1)
    if(lstBottom[1]>=0):
        if(envMat[lstBottom[0]][lstBottom[1]]== 0):
            resLst.append(lstBottom)
    return resLst

'''
check the connective of env
'''
import networkx as nx

edgeLst = []
sPntx = []
sPnty = []
tPntx = []
tPnty = []
row = coarseMat.shape[0]
col = coarseMat.shape[1]
G = nx.Graph()
for i in range(row):
    for j in range(col):
        centre = (i, j)
        G.add_node((i, j))
        if (coarseMat[i][j] == 1):
            continue
        neiLst = getNeighbor(coarseMat, lst=centre, row=row, col=col)
        # print(neiLst)
        # raise Exception()
        for unit in neiLst:
            sPntx.append(i + 0.5)
            sPnty.append(j + 0.5)
            tPntx.append(unit[0] + 0.5)
            tPnty.append(unit[1] + 0.5)
            G.add_edge(centre, unit)
            if (i, j, unit[0], unit[1]) not in edgeLst or (unit[0], unit[1], i, j) not in edgeLst:
                edgeLst.append((i, j, unit[0], unit[1]))

component = list(nx.connected_components(G))
largest_cc = max(component, key = len)
largest_cc_lst = list(max(component, key = len))
print(largest_cc)
print(len(component))

# exit()

envMat = np.ones((coarseMat.shape[0],coarseMat.shape[1]), dtype = int)

for unit in largest_cc:
    envMat[unit[0]][unit[1]] = 0

import random
import readcfg as rd
import datetime

r_seed = 1
random.seed(r_seed)
robNum = 4
# print(random.choces(largest_cc, k = robNum))
robPosLst = random.choices(largest_cc_lst, k = robNum)


rob_row_lst = []
rob_col_lst = []
for robRow,robCol in robPosLst:
    rob_row_lst.append(robRow)
    rob_col_lst.append(robCol)

_robReachRowLst = []
_robReachColLst = []
for rowInd, colInd in largest_cc:
    _robReachRowLst.append(rowInd)
    _robReachColLst.append(colInd)

_robUnReachRowLst = []
_robUnReachColLst = []
for componentUnit in component:
    if componentUnit == largest_cc:
        continue
    for rowInd,colInd in componentUnit:
        _robUnReachRowLst.append(rowInd)
        _robUnReachColLst.append(colInd)

print(len(_robReachRowLst))
print(len(_robUnReachColLst))
# for


fileCfg = './/benchmarkData//r' + str(robNum) + '_r' + str(row) + '_c' + str(col)  + '_s' + str(r_seed)\
          + insName
f_con = open(fileCfg, 'w')

f_con.write('time ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
rd.writeConf(f_con, 'row', [row])
rd.writeConf(f_con, 'col', [col])
rd.writeConf(f_con, 'robRow', rob_row_lst)
rd.writeConf(f_con, 'robCol', rob_col_lst)
# rd.writeConf(f_con, 'obstacle', obstacleLst)

rd.writeConf(f_con, 'robReachRowLst', _robReachRowLst)
rd.writeConf(f_con, 'robReachColLst', _robReachColLst)
rd.writeConf(f_con, 'robUnReachRowLst', _robUnReachRowLst)
rd.writeConf(f_con, 'robUnReachColLst', _robUnReachColLst)

grid = []
for rowID, colID in np.ndindex(envMat.shape):
    grid.append(int(envMat[rowID][colID]))
rd.writeConf(f_con, 'grid', grid)
f_con.close()


import MCPPinstance
import drawEnv
'''
test and draw
'''
ins = MCPPinstance.MCPPInstance()
ins.loadCfg(fileCfg)
drawEnv.drawPic(ins)
