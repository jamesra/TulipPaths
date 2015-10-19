from unittest import TestCase
from tulip import *
import tulippaths as tp

class TestFindPaths(TestCase):

    def test_findPathZero(self):
        graphFile = '../data/test_zero.tlp'
        graph = tlp.loadGraph(graphFile)
        sourceId = 176
        targetId = 606
        maxNumHops = 1

        sourceNode = tp.getNodeById(sourceId, graph)
        targetNode = tp.getNodeById(targetId, graph)

        finder = tp.PathFinder(graph)
        finder.findPaths(sourceNode, targetNode, maxNumHops)

        self.assertTrue(len(finder.valid) == 1)
        self.assertTrue(finder.valid[0].isSane())
        self.assertTrue(len(finder.failed) == 0)

    def test_findPathOne(self):
        tp.VERBOSE = True
        graphFile = '../data/test_one.tlp'
        sourceId = 176
        targetId = 606
        maxNumHops = 4

        graph = tlp.loadGraph(graphFile)
        sourceNode = tp.getNodeById(sourceId, graph)
        targetNode = tp.getNodeById(targetId, graph)

        finder = tp.PathFinder(graph)
        finder.findPaths(sourceNode, targetNode, maxNumHops)

        self.assertTrue(len(finder.valid) == 4)
        self.assertTrue(len(finder.failed) == 1)
        for path in finder.valid:
            self.assertTrue(path.isSane())