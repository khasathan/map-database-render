'''

Author: 
  KHASATHAN

Required:   
  - Python 2.7
  - Matplotlib

'''

#!/use/bin/env python
#-*- coding: utf8 -*-

import sys
import struct
import matplotlib.pyplot as plt

BLOCK_SIZE = 2
DATA_START_IDX = 216
MESH_COOR_OFFSET = 10
MESH_COOR_BLOCK_SIZE = 4

class Map:

  def __init__(self):
    ''' '''

  def readMeshFile(self, path):
    data = []
    
    # read data
    fp = open(path, 'rb')
    bindata = fp.read()
    fp.close()
    
    # skip header
    bindata = bindata[DATA_START_IDX * BLOCK_SIZE:]
    
    # data size in bytes
    data_size = len(bindata) * BLOCK_SIZE

    # amount of coordinate data
    amount = struct.unpack('h', bindata[0] + bindata[1])[0]

    # initial index of coordinate data
    mesh_start = 0
    mesh_end = mesh_start + amount
    
    while mesh_end < data_size:
      bulk_coor = []
      
      # jump to coordinate data
      mesh_start += MESH_COOR_OFFSET * BLOCK_SIZE
      
      for i in range(mesh_start, mesh_end, MESH_COOR_BLOCK_SIZE):
        coor = struct.unpack('hh', bindata[i]
        + bindata[i+1] + bindata[i+2] + bindata[i+3])
        bulk_coor.append(coor)
      
      data.append(bulk_coor)
      
      # if cannot read amount of bytes of next mesh
      # it means end of file
      try:
        amount = struct.unpack('h', bindata[mesh_end] + bindata[mesh_end + 1])[0]
        mesh_start = mesh_end
        mesh_end = mesh_start + amount
      except Exception, e:
        break
      
    return data


  def readCsvFile(self, path):
    data = []
    fp = open(path, 'r')
    lines = fp.readlines()
    fp.close()
    
    for line in lines:
      line = line.replace('\r\n', '').strip()
      if len(line) == 0:
        continue
      data.append(line)
    
    return data

  
if __name__ == '__main__':
  map = Map()
  meshdef = map.readCsvFile('meshdef.csv')
  fig = plt.figure(figsize=(100, 100), facecolor='white')
  subplot = plt.subplot()

  for i in range(1, len(meshdef)):
    meshdata = meshdef[i].split(',')
    meshfile = 'MeshData/' + meshdata[0] + '.mfv'
    minX = int(meshdata[2])
    minY = int(meshdata[3])
    bulk_coor = map.readMeshFile(meshfile)

    for bc in bulk_coor:
      x_list = []
      y_list = []
      for coor in bc:
        x = coor[0] + minX
        y = coor[1] + minY
        x_list.append(x)
        y_list.append(y)
      subplot.plot(x_list, y_list, color='k', linewidth=0.2, linestyle='-', figure=fig)

  subplot.autoscale(True)
  fig.add_subplot(subplot)
  plt.axis('off')
  plt.show()
