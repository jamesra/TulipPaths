import unittest
from unittest import TestCase
from tulip import *
import tulippaths as tp


class TestPath(TestCase):
    # Build a very simple path.
    def setUp(self):
        self.graph = tlp.loadGraph('../data/test_one.tlp')
        self.startNodeId = 606

        self.path = tp.Path(self.graph)
        node = tp.getNodeById(self.startNodeId, self.graph)
        self.path.addNode(node)

        edges = self.graph.getOutEdges(node)

        for edge in edges:
            self.path.addEdge(edge)
            self.lastNode = self.graph.target(edge)
            self.path.addNode(self.lastNode)
            break

    # Do some sanity checking on the path
    def test_basicFunctions(self):
        path = self.path
        self.assertTrue(len(path.edges) == 1)
        self.assertTrue(len(path.nodes) == 2)
        self.assertTrue(path.isSane())
        self.assertTrue(path.getLastNode() == self.lastNode)
        self.assertTrue(path.size() == 2)

    def test_isSameType(self):
        otherPath = tp.Path(self.graph)
        self.assertFalse(otherPath.isSameType(self.path))
        self.assertTrue(self.path.isSameType(self.path))

    def test_toString(self):
        self.assertTrue(self.path.toString() == '<node 1>, <edge 3>, <node 2>')

    def test_toStringOfTypes(self):
        self.assertTrue(self.path.toStringOfTypes() == 'GC ON, Adherens, CBb4w')

    def test_isInTypeConstraints(self):
        graphFile = '../data/test_one.tlp'
        graph = tlp.loadGraph(graphFile)

        source = tp.utils.getNodeById(176, graph)
        target = tp.utils.getNodeById(5530, graph)

        pathFinder = tp.PathFinder(graph)

        pathFinder.findPaths(source, target, 2)

        for path in pathFinder.valid:
            if path.size() < 3:
                continue
            else:
                constrainedEdges = ["Ribbon Synapse", "Adherens"]
                constrainedNodes = ["CBb3-4i", "GC ON", "CBb4w"]
                self.assertTrue(path.isInTypeConstraints(constrainedEdges, constrainedNodes))

    def test_isInRegexTypeConstraints(self):
        graphFile = '../data/test_one.tlp'
        graph = tlp.loadGraph(graphFile)

        source = tp.utils.getNodeById(176, graph)
        target = tp.utils.getNodeById(5530, graph)

        pathFinder = tp.PathFinder(graph)

        pathFinder.findPaths(source, target, 2)

        for path in pathFinder.valid:
            if path.size() < 3:
                continue
            else:
                # Make sure the path satisfies valid regex constraints
                constrainedEdgeRegexes = [ "R.* Synapse", "Adh[a-z]rens" ]
                constrainedNodeRegexes = [ "CBb3-[1-9]i", "^GZ?C ON$", "C[A-Z]b4w" ]
                self.assertTrue(path.isInRegexTypeConstraints(
                    constrainedNodeRegexes, constrainedEdgeRegexes))
                # Make sure the path does not satisfy invalid regex constraints
                constrainedEdgeRegexes = [ "Cthulhu F'taghn", "R'lyeh Synapse" ]
                constrainedNodeRegexes = [ "^Nyarlathotep$", "^$", "[0-1].*" ]
                self.assertFalse(path.isInRegexTypeConstraints(
                    constrainedNodeRegexes, constrainedEdgeRegexes))


    def test_isSynapticPath(self):

        graphFile = '../data/test_one.tlp'
        graph = tlp.loadGraph(graphFile)

        source = tp.utils.getNodeById(176, graph)
        target = tp.utils.getNodeById(5530, graph)

        pathFinder = tp.PathFinder(graph)

        pathFinder.findPaths(source, target, 2)

        for path in pathFinder.valid:
            if path.toStringOfTypes() == 'CBb3-4i, Unknown, CBb4w':
                self.assertTrue(path.isSynapticPath())
            elif path.toStringOfTypes() == 'CBb3-4i, Ribbon Synapse, GC ON, Adherens, CBb4w':
                self.assertFalse(path.isSynapticPath())
            else:
                self.assertTrue(False) # Should never get here.


if __name__ == "__main__":
    unittest.main()
