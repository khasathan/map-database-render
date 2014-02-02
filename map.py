'''

Author:     KHASATHAN
Required:   
  - Python 2.7
  - Matplotlib

'''

#!/use/bin/env python
#-*- coding: utf8 -*-

import sys
import struct
import matplotlib.pyplot as plt
import matplotlib.lines as plt_lines

BLOCK_SIZE = 2
DATA_START_IDX = 216
MESH_COOR_OFFSET = 10
MESH_COOR_BLOCK_SIZE = 4

class Map:
  plt = None
  plt_lines = None
  subplt = None
  line2d = None

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
        print "( %s ,  %s ) " % (coor[0], coor[1])
      
      data.append(bulk_coor)
      
      # if cannot read amount of bytes of next mesh
      # it's mean end of file
      try:
        amount = struct.unpack('h', bindata[mesh_end] + bindata[mesh_end + 1])[0]
        mesh_start = mesh_end
        mesh_end = mesh_start + amount
      except Exception, e:
        break
      
      print "-------------------------"
    
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
  fig = plt.figure() 
  ax = fig.add_subplot(111)  
  c = 1

  for i in range(1, len(meshdef)):
    meshdata = meshdef[i].split(',')
    meshfile = 'MeshData/' + meshdata[0] + '.mfv'
    print meshfile
    bulk_coor = map.readMeshFile(meshfile)
    #print bulk_coor
    
    
    for bc in bulk_coor:
      x = []
      y = []
      for coor in bc:
        x.append(coor[0])
        y.append(coor[1])
      line = ax.plot(x, y, color='k', linewidth=0.1, linestyle='-')
    

  plt.show()

