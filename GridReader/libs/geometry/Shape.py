import numpy as np
from libs.geometry.Point import Point

class Triangle:
	dimension						   = 2
	numberOfInnerFaces				   = 3
	numberOfFacets					   = 3
	subelementTransformedVolumes	   = np.array([1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0])
	innerFaceShapeFunctionValues 	   = np.array([[5.0/12.0, 5.0/12.0, 1.0/6.0],[1.0/6.0, 5.0/12.0, 5.0/12.0],[5.0/12.0, 1.0/6.0, 5.0/12.0]])
	innerFaceShapeFunctionDerivatives  = np.array([[[-1.0/1.0, -1.0/1.0], [1.0/1.0, 0.0/1.0], [0.0/1.0, 1.0/1.0]],[[-1.0/1.0, -1.0/1.0], [1.0/1.0, 0.0/1.0], [0.0/1.0, 1.0/1.0]],[[-1.0/1.0, -1.0/1.0], [1.0/1.0, 0.0/1.0], [0.0/1.0, 1.0/1.0]]])
	innerFaceNeighbourVertices		   = np.array([[0, 1],[1, 2],[2, 0]])
	subelementShapeFunctionValues 	   = np.array([[[-1.0/1.0, -1.0/1.0], [1.0/1.0, 0.0/1.0], [0.0/1.0, 1.0/1.0]],[[-1.0/1.0, -1.0/1.0], [1.0/1.0, 0.0/1.0], [0.0/1.0, 1.0/1.0]],[[-1.0/1.0, -1.0/1.0], [1.0/1.0, 0.0/1.0], [0.0/1.0, 1.0/1.0]]])
	subelementShapeFunctionDerivatives = np.array([[[-1.0/1.0, -1.0/1.0], [1.0/1.0, 0.0/1.0], [0.0/1.0, 1.0/1.0]],[[-1.0/1.0, -1.0/1.0], [1.0/1.0, 0.0/1.0], [0.0/1.0, 1.0/1.0]],[[-1.0/1.0, -1.0/1.0], [1.0/1.0, 0.0/1.0], [0.0/1.0, 1.0/1.0]]])
	facetVerticesIndices 			   = np.array([[1, 0],[2, 1],[0, 2]])
	outerFaceShapeFunctionValues 	   = np.array([[[1.0/4.0, 3.0/4.0, 0.0/1.0],[3.0/4.0, 1.0/4.0, 0.0/1.0]],[[0.0/1.0, 1.0/4.0, 3.0/4.0],[0.0/1.0, 3.0/4.0, 1.0/4.0]],[[3.0/4.0, 0.0/1.0, 1.0/4.0],[1.0/4.0, 0.0/1.0, 3.0/4.0]]])

	def __init__(self, element):
		self.element = element

	@staticmethod
	def _is(elem):
		if len(elem.vertices) == 3:
			return True
		else:
			return False

	@staticmethod
	def getInnerFaceAreaVector(local, elementCentroid, elementVertices):
		vertex1 = elementVertices[Triangle.innerFaceNeighbourVertices[local][0]]
		vertex2 = elementVertices[Triangle.innerFaceNeighbourVertices[local][1]]
		areaVectorCoords = sum([w*vertex.getCoordinates() for w,vertex in zip([1,-0.5,-0.5],[elementCentroid, vertex1, vertex2])])
		return Point(*areaVectorCoords)

class Quadrilateral:
	dimension						   = 2
	numberOfInnerFaces				   = 4
	numberOfFacets 					   = 4
	subelementTransformedVolumes	   = np.array([1.0/4.0, 1.0/4.0, 1.0/4.0, 1.0/4.0])
	innerFaceShapeFunctionValues	   = np.array([[3.0/8.0, 3.0/8.0, 1.0/8.0, 1.0/8.0], [1.0/8.0, 3.0/8.0, 3.0/8.0, 1.0/8.0], [1.0/8.0, 1.0/8.0, 3.0/8.0, 3.0/8.0], [3.0/8.0, 1.0/8.0, 1.0/8.0, 3.0/8.0]])
	innerFaceShapeFunctionDerivatives  = np.array([[[-3.0/4.0, -1.0/2.0], [3.0/4.0, -1.0/2.0], [1.0/4.0, 1.0/2.0], [-1.0/4.0, 1.0/2.0]],[[-1.0/2.0, -1.0/4.0], [1.0/2.0, -3.0/4.0], [1.0/2.0, 3.0/4.0], [-1.0/2.0, 1.0/4.0]],[[-1.0/4.0, -1.0/2.0], [1.0/4.0, -1.0/2.0], [3.0/4.0, 1.0/2.0], [-3.0/4.0, 1.0/2.0]],[[-1.0/2.0, -3.0/4.0], [1.0/2.0, -1.0/4.0], [1.0/2.0, 1.0/4.0], [-1.0/2.0, 3.0/4.0]]])
	innerFaceNeighbourVertices		   = np.array([[0, 1],[1, 2],[2, 3],[3, 0]])
	subelementShapeFunctionValues	   = np.array([[9.0/16.0, 3.0/16.0, 1.0/16.0, 3.0/16.0],[3.0/16.0, 9.0/16.0, 3.0/16.0, 1.0/16.0],[1.0/16.0, 3.0/16.0, 9.0/16.0, 3.0/16.0],[3.0/16.0, 1.0/16.0, 3.0/16.0, 9.0/16.0]])
	subelementShapeFunctionDerivatives = np.array([[[-3.0/4.0, -3.0/4.0], [3.0/4.0, -1.0/4.0], [1.0/4.0, 1.0/4.0], [-1.0/4.0, 3.0/4.0]],[[-3.0/4.0, -1.0/4.0], [3.0/4.0, -3.0/4.0], [1.0/4.0, 3.0/4.0], [-1.0/4.0, 1.0/4.0]],[[-1.0/4.0, -1.0/4.0], [1.0/4.0, -3.0/4.0], [3.0/4.0, 3.0/4.0], [-3.0/4.0, 1.0/4.0]],[[-1.0/4.0, -3.0/4.0], [1.0/4.0, -1.0/4.0], [3.0/4.0, 1.0/4.0], [-3.0/4.0, 3.0/4.0]]])
	facetVerticesIndices 			   = np.array([[1, 0],[2, 1],[3, 2],[0, 3]])
	outerFaceShapeFunctionValues	   = np.array([[[1.0/4.0, 3.0/4.0, 0.0/1.0, 0.0/1.0],[3.0/4.0, 1.0/4.0, 0.0/1.0, 0.0/1.0]],[[0.0/1.0, 1.0/4.0, 3.0/4.0, 0.0/1.0],[0.0/1.0, 3.0/4.0, 1.0/4.0, 0.0/1.0]],[[0.0/1.0, 0.0/1.0, 1.0/4.0, 3.0/4.0],[0.0/1.0, 0.0/1.0, 3.0/4.0, 1.0/4.0]],[[3.0/4.0, 0.0/1.0, 0.0/1.0, 1.0/4.0],[1.0/4.0, 0.0/1.0, 0.0/1.0, 3.0/4.0]]])

	def __init__(self, element):
		self.element = element			

	@staticmethod
	def _is(elem):
		if len(elem.vertices) == 4:
			return True
		else:
			return False

	@staticmethod
	def getInnerFaceAreaVector(local, elementCentroid, elementVertices):
		vertex1 = elementVertices[Triangle.innerFaceNeighbourVertices[local][0]]
		vertex2 = elementVertices[Triangle.innerFaceNeighbourVertices[local][1]]
		areaVectorCoords = sum([w*vertex.getCoordinates() for w,vertex in zip([1,-0.5,-0.5],[elementCentroid, vertex1, vertex2])])
		return Point(*areaVectorCoords)