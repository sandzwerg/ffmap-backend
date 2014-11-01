#!/usr/bin/env python3
import subprocess
import time
import os
from GlobalRRD import GlobalRRD
from NodeRRD import NodeRRD

class rrd:
  def __init__( self
              , databaseDirectory
              , imagePath
<<<<<<< HEAD
              , displayTimeMonthly = "31d"
=======
              , displayTimeMontly = "31d"
>>>>>>> 9282d39285c243e0ca38a65465f07473deffb5f8
              , displayTimeGlobal = "7d"
              , displayTimeNodeMonthly = "28d"
              , displayTimeNode = "3d"
              ):
    self.dbPath = databaseDirectory
    self.globalDb = GlobalRRD(self.dbPath)
    self.imagePath = imagePath
<<<<<<< HEAD
    self.displayTimeMonthly = displayTimeMonthly
=======
    self.displayTimeMontly = displayTimeMontly
>>>>>>> 9282d39285c243e0ca38a65465f07473deffb5f8
    self.displayTimeGlobal = displayTimeGlobal
    self.displayTimeNode = displayTimeNode
    self.displayTimeNodeMonthly = displayTimeNodeMonthly

    self.currentTimeInt = (int(time.time())/60)*60
    self.currentTime    = str(self.currentTimeInt)

    try:
      os.stat(self.imagePath)
    except:
      os.mkdir(self.imagePath)

  def update_database(self,db):
    nodes = {}
    clientCount = 0
    for node in db.get_nodes():
      if node.flags['online']:
        if not node.flags['client']:
          nodes[node.id] = node
          node.clients = 0;
          if 'legacy' in node.flags and node.flags['legacy']:
            clientCount -= 1
        else:
          clientCount += 1
    for link in db.get_links():
      source = link.source.interface
      target = link.target.interface
      if source in nodes and not target in nodes:
        nodes[source].clients += 1
      elif target in nodes and not source in nodes:
        nodes[target].clients += 1
      elif link.type == 'client':
        nodes[db.get_nodes()[link.source.id].id].clients += 1

    self.globalDb.update(len(nodes), clientCount)
    for node in nodes.values():
      rrd = NodeRRD(
        os.path.join(self.dbPath, str(node.id).replace(':', '') + '.rrd'),
        node
      )
      rrd.update()

  def update_images(self):
    """ Creates an image for every rrd file in the database directory.
    """

    self.globalDb.graph(os.path.join(self.imagePath, "globalGraph.png"), self.displayTimeGlobal)
<<<<<<< HEAD
    self.globalDb.graphMonthly(os.path.join(self.imagePath, "globalGraphMonthly.png"), self.displayTimeMonthly)
=======
    self.globalDb.graphMonthly(os.path.join(self.imagePath, "globalGraphMonthly.png"), self.displayTimeMontly)
>>>>>>> 9282d39285c243e0ca38a65465f07473deffb5f8

    nodeDbFiles = os.listdir(self.dbPath)

    for fileName in nodeDbFiles:
      if not os.path.isfile(os.path.join(self.dbPath, fileName)):
        continue

      nodeName = os.path.basename(fileName).split('.')
      if nodeName[1] == 'rrd' and not nodeName[0] == "nodes":
        rrd = NodeRRD(os.path.join(self.dbPath, fileName))
        rrd.graph(self.imagePath, self.displayTimeNode)
        #rrd.graphMonthly(self.imagePath, self.displayTimeNodeMonthly)
