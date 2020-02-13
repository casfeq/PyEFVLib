import numpy as np
from libs.geometry.MSHReader import MSHReader
from libs.geometry.Grid import Grid
from libs.simulation.ProblemData2D import ProblemData2D
from libs.simulation.Timer import Timer
from libs.simulation.CgnsSaver import CgnsSaver
import pandas as pd

class HeatTransfer2D:
	def __init__(self):
		self.settings()
		self.run()
		self.finalize()

	def settings(self):
		self.problemData = ProblemData2D('heat_transfer_2d')
		
		reader = MSHReader(self.problemData.paths["Grid"])
		self.grid = Grid(reader.getData())
		self.problemData.setGrid(self.grid)

		self.timer = Timer(self.problemData.timeStep)				# Contains dictionary with initial times for different labels: start("assembly"); stop("assembly")
		self.cgnsSaver = CgnsSaver(self.timer, self.grid, self.problemData.paths["Output"], self.problemData.libraryPath)

		self.calculateInnerFacesGlobalDerivatives()
		self.numericalTemperature = np.zeros(self.grid.vertices.size)
		self.oldTemperature = np.repeat(self.problemData.initialValue, self.grid.vertices.size)

		self.matrix = np.zeros([self.grid.vertices.size, self.grid.vertices.size])
		self.difference = 0.0
		self.iteration = 0
		self.converged = False

	def run(self):
		while not self.converged and self.iteration < self.problemData.maxNumberOfIterations:
			self.addToLinearSystem()
			self.solveLinearSystem()
			self.print()

			self.timer.incrementTime()
			self.cgnsSaver.save(self.numericalTemperature, self.timer.getCurrentTime())
			self.converged = self.checkConvergence()

			self.iteration += 1   

	def calculateInnerFacesGlobalDerivatives(self):
		for element in self.grid.elements:
			for innerFace in element.innerFaces:
				derivatives = innerFace.element.shape.innerFaceShapeFunctionDerivatives[innerFace.local]
				innerFace.globalDerivatives = np.matmul(np.linalg.inv(element.getJacobian(derivatives)) , np.transpose(derivatives))

	def addToLinearSystem(self):
		self.timer.start("assemble")
		self.independent = np.zeros(self.grid.vertices.size)

		# Internal Heat Generation
		for region in self.grid.regions:
			heatGeneration = self.problemData.propertyData[region.handle]["InternalHeatGeneration"]
			for element in region.elements:
				for vertex in element.vertices:
					self.independent[vertex.handle] = vertex.volume * heatGeneration

		# TransientTermAdder and DiffusiveFluxAdder
		for region in self.grid.regions:
			density = self.problemData.propertyData[region.handle]["Density"]
			heatCapacity = self.problemData.propertyData[region.handle]["HeatCapacity"]
			conductivity = self.problemData.propertyData[region.handle]["Conductivity"]
			accumulation = density * heatCapacity / self.	timer.timeStep

			for element in region.elements:
				localMatrixFlux = computeLocalMatrix(element, conductivity,self.iteration==0)
				local = 0
				for vertex in element.vertices:
					index = vertex.handle
					self.independent[index] += element.subelementVolumes[local] * accumulation * self.oldTemperature[vertex.handle]
					if self.iteration == 0:
						self.matrix[index][index] += element.subelementVolumes[local] * accumulation
						qLocalIndex = 0
						for q in element.vertices:
							self.matrix[index][q.handle] += localMatrixFlux[local][qLocalIndex]
							qLocalIndex += 1
					local += 1

		# NeumannBoundaryAdder
		for bCondition in self.problemData.neumannBoundaries:
			for facet in bCondition.boundary.facets:
				for outerFace in facet.outerFaces:
					self.independent[outerFace.vertex.handle] += -1.0 * bCondition.getValue(outerFace.handle) * np.linalg.norm(outerFace.area.getCoordinates())


		# DirichletBoundaryAdder
		for bCondition in self.problemData.dirichletBoundaries:
			for vertex in bCondition.boundary.vertices:
				self.independent[vertex.handle] = bCondition.getValue(vertex.handle)

		if self.iteration == 0:
			numberOfVertices = sum([boundary.boundary.vertices.size for boundary in self.problemData.dirichletBoundaries])
			rows = np.zeros(numberOfVertices)
			for bCondition in self.problemData.dirichletBoundaries:
				for vertex in bCondition.boundary.vertices:
					self.matrix[vertex.handle] = np.zeros(self.grid.vertices.size)
					self.matrix[vertex.handle][vertex.handle] = 1.0

		self.timer.stop("assemble")

	def solveLinearSystem(self):
		self.timer.start("solve")
		self.numericalTemperature = np.linalg.solve(self.matrix, self.independent)
		self.timer.stop("solve")

	def checkConvergence(self):
		# Here oldTemperature becomes numerical (or right after this func is called)
		converged = False
		self.difference = max([abs(temp-oldTemp) for temp, oldTemp in zip(self.numericalTemperature, self.oldTemperature)])
		self.oldTemperature = self.numericalTemperature
		if self.timer.getCurrentTime() > self.problemData.finalTime:
			converged = True
		elif self.iteration > 0:
			converged = self.difference < self.problemData.tolerance

		return converged

	def startInfo(self):
		for key,path in zip( ["input", "output", "grids"] , [self.problemData.libraryPath+"/benchmark/heat_transfer_2d/" , self.problemData.paths["Output"], self.problemData.paths["Grid"]] ):
			print(f"\t\033[1;35m{key}\033[0m\n\t\t{path}\n")

		print(f"\t\033[1;35msolid\033[0m")
		for region in self.grid.regions:
			print(f"\t\t\033[36m{region.name}\033[0m")#//in blue
			for _property in self.problemData.propertyData[region.handle].keys():
				print(f"\t\t\t{_property}   : {self.problemData.propertyData[region.handle][_property]}")#//16 digits | scientific

			print("")
		print("")

	def print(self):
		if self.iteration == 0:
			self.startInfo()
			print("{:>9}\t{:>14}\t{:>14}\t{:>14}".format("Iteration", "CurrentTime", "TimeStep", "Difference"))
		else:
			print("{:>9}\t{:>14e}\t{:>14e}\t{:>14e}".format(self.iteration, self.timer.getCurrentTime(), self.timer.timeStep, self.difference))

	def finalize(self):
		self.cgnsSaver.finalize()
		print("")
		total = 0.0
		for timeLabel in self.timer.timeLabels.keys():
			total += self.timer.timeLabels[timeLabel]["elapsedTime"]
			print("\t{:<12}:{:>12.5f}s".format(timeLabel, self.timer.timeLabels[timeLabel]["elapsedTime"]))
		print("\t{:<12}:{:>12.5f}s".format("total", total))

		print("\n\t\033[1;35mresult:\033[0m", self.problemData.paths["Output"]+"Results.cgns", '\n')

def computeLocalMatrix(element, permeability,b=False):
	numberOfVertices = element.vertices.size
	localMatrix = np.zeros([numberOfVertices, numberOfVertices])
	for innerFace in element.innerFaces:
		derivatives = innerFace.globalDerivatives
		if len(derivatives) == 2: derivatives = np.vstack([derivatives, np.zeros(derivatives[0].size)])
		diffusiveFlux = permeability * np.matmul( np.transpose(derivatives[:-1]) , innerFace.area.getCoordinates()[:-1] )

		backwardVertexLocalHandle = element.shape.innerFaceNeighbourVertices[innerFace.local][0]
		forwardVertexLocalHandle = element.shape.innerFaceNeighbourVertices[innerFace.local][1]

		for i in range(numberOfVertices):
			coefficient = -1.0 * diffusiveFlux[i]
			localMatrix[backwardVertexLocalHandle][i] += coefficient
			localMatrix[forwardVertexLocalHandle][i] -= coefficient
	return localMatrix
