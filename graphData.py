import random
import matplotlib.pyplot as plt
from statistics import mean, stdev
import json
import os
import sys

class GraphData():
    def __init__(self, filesNamesToGraph):
        self.gaussianType, self.uniformType = "GAUSS", "UNIFORM"
        self.randomTypes = [self.gaussianType, self.uniformType]
        self.filesNames = filesNamesToGraph
        self.dataNames = [os.path.splitext(self.filesNames[i])[0] for i in range(len(self.filesNames))]
        self.dataList = []
        self.dataMeanValues = []
        self.dataMaxValues = []
        self.dataMinValues = []
        self.dataStandardDeviations = []
        self.randomData = []
        self.plots = [None for i in range(len(self.filesNames))]
        self.meanVertical = None
        self.XValues = []

    def fileOperations(self):
        for i in range(len(self.filesNames)):
            f = open(self.filesNames[i])
            self.dataList.append(json.load(f))
            f.close

    def dataPreperations(self):
        self.meanVertical = round((self.maxValue(self.dataList) + self.minValue(self.dataList))/2)
        for i in range(len(self.dataList)):
            self.XValues.append(list(range(1, len(self.dataList[i]) + 1)))
            self.dataMeanValues.append(mean(self.dataList[i]))
            self.dataStandardDeviations.append(stdev(self.dataList[i]))
            self.dataMaxValues.append([max(self.dataList[i]), self.dataList[i].index(max(self.dataList[i]))])
            self.dataMinValues.append([min(self.dataList[i]), self.dataList[i].index(min(self.dataList[i]))])

    def maxValue(self, inputList):
        return max([max(list) for list in inputList])

    def minValue(self, inputList):
        return min([min(list) for list in inputList])

    def prepareHistograms(self):
        fig = plt.figure("Histograms Figure")
        for i in range(len(self.dataList)):
            subplotNumber = len(self.dataList)*100 + 10 + i + 1
            self.plots[i] = fig.add_subplot(subplotNumber)
            self.plots[i].hist(self.dataList[i])
            self.plots[i].set_title(self.dataNames[i] + " Histogram")

    def generateRandomMeasurement(self, randomType):
        if randomType == self.gaussianType:
            for i in range(len(self.dataList)):
                self.randomData.append(round(random.uniform(min(self.dataList[i]), max(self.dataList[i]))))
        elif randomType == self.uniformType:
            for i in range(len(self.dataList)):
                self.randomData.append(round(random.gauss(self.dataMeanValues[i], self.dataStandardDeviations[i])))

    def prepareValuesGraph(self):
        plt.figure("All Data Figure")
        # Add values from files to plot
        for i in range(len(self.dataList)):
            plt.plot(self.XValues[i], self.dataList[i], label = self.dataNames[i], marker="o")
            plt.text(len(self.dataList[i]) + 1, self.dataList[i][len(self.dataList[i]) - 1], str(self.dataList[i][len(self.dataList[i]) - 1]))
        # Add mean line to plot
        for i in range(len(self.dataList)):
            plt.plot([0, len(self.dataList[i])], [self.dataMeanValues[i], self.dataMeanValues[i]], label = self.dataNames[i] + " mean value")
        # Add random values to plot
        for type in self.randomTypes:
            self.generateRandomMeasurement(type)
            stringToPrint = "Random " + str(type.lower()) + " data: "
            for i in range(len(self.dataList)):
                stringToPrint += self.dataNames[i] + " - " + str(self.randomData[i]) + "; "
            print(stringToPrint)
            for i in range(len(self.dataList)):
                plt.plot(len(self.dataList[i]) + 5, self.randomData[i], label = "Random " + str(type.lower()) + " " + self.dataNames[i],   linestyle='dashed', marker= "*", markersize=5)
                plt.text(len(self.dataList[i]) + 5, self.randomData[i], str(self.randomData[i]), horizontalalignment='left')
            self.randomData.clear()
        # Add mean values text to plot
        stringToPrint = "Mean values: "
        for i in range(len(self.dataList)):
            stringToPrint += str(self.dataNames[i]) + " - " + str(round(self.dataMeanValues[i])) + "; "
        # Add standard deviations text to plot
        stringToPrint += "Standard deviations: "
        for i in range(len(self.dataList)):
            stringToPrint += str(self.dataNames[i]) + " - " + str(round(self.dataStandardDeviations[i], 2)) + "; "
        maxXValuesLength = max([len(xValues) for xValues in self.XValues])
        plt.text(round(maxXValuesLength/2), self.meanVertical, stringToPrint, horizontalalignment='center')
        # Add min, max values to the plot
        for i in range(len(self.dataList)):
            if self.dataMaxValues[i][0] != len(self.dataList[i]) - 1:
                plt.text(self.dataMaxValues[i][1] + 1, self.dataMaxValues[i][0], "Max - " + str(self.dataMaxValues[i][0]), verticalalignment="bottom", horizontalalignment="center")
            if self.dataMinValues[i][0] != len(self.dataList[i]) - 1:
                plt.text(self.dataMinValues[i][1] + 1, self.dataMinValues[i][0] - 2, "Min - " + str(self.dataMinValues[i][0]), verticalalignment="bottom", horizontalalignment="center")

    def plotAll(self):
        plt.xlabel("x - samples")
        stringToPrint = "y - measurement ("
        for i in range(len(self.dataList)):
            if i != len(self.dataNames) - 1:
                stringToPrint += self.dataNames[i] + ", "
            else:
                stringToPrint += self.dataNames[i] + ")"
        plt.ylabel(stringToPrint)
        plt.title("Measurements")
        plt.legend(loc='center left', framealpha=0.5)
        plt.show()

    def run(self):
        self.fileOperations()
        self.dataPreperations()
        self.prepareHistograms()
        self.prepareValuesGraph()
        self.plotAll()

def showInstruction():
    print("Program for graphing data read from selected files.")
    print("Files to read are selected by writing their extensions in the terminal (If multiple file extensions will be used, they should be written as a ... (no idea for now))")
    print("For now, data can't be load with corresponding x values - only the measurements.")
    print("Data will appear as histograms of the load data and a graph with a mean and standard deviation, one prediction (uniform and gauss) and min and max values for each data set.")
    print("y names of values are determined by names of the corresponding files.\n")

if __name__ == '__main__':
    showInstruction()
    amountOfFilesWithGivenExtention = 0
    while amountOfFilesWithGivenExtention == 0:
        fileExtention = input('Specify extention of files to be included in the graph (e.g.: txt, json - without "."): ').lower()
        fileExtention = "json"
        filesNames = [file for file in os.listdir() if file.endswith("." + fileExtention)]
        amountOfFilesWithGivenExtention = len(filesNames)
        if amountOfFilesWithGivenExtention == 0:
            print("No ." + fileExtention + " files found in directory: '" + str(os.path.abspath(os.getcwd())) + "'.")
            print("Files found: '", end = "")
            filesToPrint = "', '".join(os.listdir())
            print(filesToPrint + "'\nTry again.")
            sys.exit()
        else:
            print(str(amountOfFilesWithGivenExtention) + ' files with "' + fileExtention + '" extention found.')
    measurementsDataGraph = GraphData(filesNames)
    measurementsDataGraph.run()
