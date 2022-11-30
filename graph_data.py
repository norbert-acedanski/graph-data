import random
import matplotlib.pyplot as plt
from statistics import mean, stdev
import json
import os
import sys


class GraphData():
    def __init__(self, files_names_to_graph):
        self.gaussian_type, self.uniform_type = "GAUSS", "UNIFORM"
        self.random_types = [self.gaussian_type, self.uniform_type]
        self.files_names = files_names_to_graph
        self.data_names = [os.path.splitext(self.files_names[i])[0] for i in range(len(self.files_names))]
        self.data_list = []
        self.data_mean_values = []
        self.data_max_values = []
        self.data_min_values = []
        self.data_standard_deviations = []
        self.random_data = []
        self.plots = [None for i in range(len(self.files_names))]
        self.mean_vertical = None
        self.x_values = []

    def file_operations(self):
        for i in range(len(self.files_names)):
            f = open(self.files_names[i])
            self.data_list.append(json.load(f))
            f.close()

    def data_preparations(self):
        self.mean_vertical = round((self.max_value(self.data_list) + self.min_value(self.data_list))/2)
        for i in range(len(self.data_list)):
            self.x_values.append(list(range(1, len(self.data_list[i]) + 1)))
            self.data_mean_values.append(mean(self.data_list[i]))
            self.data_standard_deviations.append(stdev(self.data_list[i]))
            self.data_max_values.append([max(self.data_list[i]), self.data_list[i].index(max(self.data_list[i]))])
            self.data_min_values.append([min(self.data_list[i]), self.data_list[i].index(min(self.data_list[i]))])

    def max_value(self, input_list):
        return max([max(list) for list in input_list])

    def min_value(self, input_list):
        return min([min(list) for list in input_list])

    def prepare_histograms(self):
        fig = plt.figure("Histograms Figure")
        for i in range(len(self.data_list)):
            subplot_number = len(self.data_list)*100 + 10 + i + 1
            self.plots[i] = fig.add_subplot(subplot_number)
            self.plots[i].hist(self.data_list[i])
            self.plots[i].set_title(self.data_names[i] + " Histogram")

    def generate_random_measurement(self, random_type):
        if random_type == self.uniform_type:
            for i in range(len(self.data_list)):
                self.random_data.append(round(random.uniform(min(self.data_list[i]), max(self.data_list[i]))))
        elif random_type == self.gaussian_type:
            for i in range(len(self.data_list)):
                self.random_data.append(round(random.gauss(self.data_mean_values[i], self.data_standard_deviations[i])))

    def prepare_values_graph(self):
        plt.figure("All Data Figure")
        # Add values from files to plot
        for i in range(len(self.data_list)):
            plt.plot(self.x_values[i], self.data_list[i], label = self.data_names[i], marker="o")
            plt.text(len(self.data_list[i]) + 1, self.data_list[i][len(self.data_list[i]) - 1],
                     str(self.data_list[i][len(self.data_list[i]) - 1]))
        # Add mean line to plot
        for i in range(len(self.data_list)):
            plt.plot([0, len(self.data_list[i])], [self.data_mean_values[i], self.data_mean_values[i]],
                     label=self.data_names[i] + " mean value")
        # Add random values to plot
        for type in self.random_types:
            self.generate_random_measurement(type)
            string_to_print = "Random " + str(type.lower()) + " data: "
            for i in range(len(self.data_list)):
                string_to_print += self.data_names[i] + " - " + str(self.random_data[i]) + "; "
            print(string_to_print)
            for i in range(len(self.data_list)):
                plt.plot(len(self.data_list[i]) + 5, self.random_data[i],
                         label=f"Random {type.lower()} {self.data_names[i]}", linestyle='dashed',
                         marker="*", markersize=5)
                plt.text(len(self.data_list[i]) + 5, self.random_data[i], str(self.random_data[i]),
                         horizontalalignment='left')
            self.random_data.clear()
        # Add mean values text to plot
        string_to_print = "Mean values: "
        for i in range(len(self.data_list)):
            string_to_print += str(self.data_names[i]) + " - " + str(round(self.data_mean_values[i])) + "; "
        # Add standard deviations text to plot
        string_to_print += "Standard deviations: "
        for i in range(len(self.data_list)):
            string_to_print += str(self.data_names[i]) + " - " + str(round(self.data_standard_deviations[i], 2)) + "; "
        max_x_values_length = max([len(x_values) for x_values in self.x_values])
        plt.text(round(max_x_values_length/2), self.mean_vertical, string_to_print, horizontalalignment='center')
        # Add min, max values to the plot
        for i in range(len(self.data_list)):
            if self.data_max_values[i][0] != len(self.data_list[i]) - 1:
                plt.text(self.data_max_values[i][1] + 1, self.data_max_values[i][0],
                         f"Max - {self.data_max_values[i][0]}",
                         verticalalignment="bottom", horizontalalignment="center")
            if self.data_min_values[i][0] != len(self.data_list[i]) - 1:
                plt.text(self.data_min_values[i][1] + 1, self.data_min_values[i][0] - 2,
                         f"Min - {self.data_min_values[i][0]}",
                         verticalalignment="bottom", horizontalalignment="center")

    def plot_all(self):
        plt.xlabel("x - samples")
        string_to_print = "y - measurement ("
        for i in range(len(self.data_list)):
            if i != len(self.data_names) - 1:
                string_to_print += self.data_names[i] + ", "
            else:
                string_to_print += self.data_names[i] + ")"
        plt.ylabel(string_to_print)
        plt.title("Measurements")
        plt.legend(loc='center left', framealpha=0.5)
        plt.show()

    def run(self):
        self.file_operations()
        self.data_preparations()
        self.prepare_histograms()
        self.prepare_values_graph()
        self.plot_all()


def show_instruction():
    print("Program for graphing data read from selected files.")
    print("Files to read are selected by writing their extensions in the terminal "
          "(If multiple file extensions will be used, they should be written as a ... (no idea for now))")
    print("For now, data can't be load with corresponding x values - only the measurements.")
    print("Data will appear as histograms of the load data and a graph with a mean and standard deviation, "
          "one prediction (uniform and gauss) and min and max values for each data set.")
    print("y names of values are determined by names of the corresponding files.\n")


if __name__ == '__main__':
    show_instruction()
    number_of_files_with_given_extension = 0
    while number_of_files_with_given_extension == 0:
        file_extension = input('Specify extention of files to be included in the graph '
                               '(e.g.: txt, json - without "."): ').lower()
        files_names = [file for file in os.listdir() if file.endswith("." + file_extension)]
        number_of_files_with_given_extension = len(files_names)
        if number_of_files_with_given_extension == 0:
            print(f"No .{file_extension} files found in directory: '" + str(os.path.abspath(os.getcwd())) + "'.")
            print("Files found: '", end="")
            files_to_print = "', '".join(os.listdir())
            print(files_to_print + "'\nTry again.")
            sys.exit()
        else:
            print(str(number_of_files_with_given_extension) + ' files with "' + file_extension + '" extension found.')
    measurements_data_graph = GraphData(files_names)
    measurements_data_graph.run()
