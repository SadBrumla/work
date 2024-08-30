import matplotlib.pyplot as plt
import pandas as pd
from format_text import format_for_graph_name, find_file_name_short, find_file_name_long, format_xlabel, format_ylabel, format_legend
from graphgenerator import *

class Graph:
    '''
    Class graph is used to load data from excel file, generate graphs from certain data,
    interpolate data, set xlim and ylim, find xlabel and ylabel
    '''
    def __init__(self):
        self.df = pd.DataFrame
        self.__int_factor = int
        

    def define_figure(self):
        self.fig = Figure(figsize=(10, 7), dpi=110, layout='tight')
        return self.fig
    
    def initlize(self,df, factor = 0):
        self.df = df
        self.__int_factor = factor
        self.labels = list(df.keys())

    def plot_axes(self, fig):
        self.fig = fig
        self.ax = fig.add_subplot(111)

        df = self.df 
        self.ax.clear()

        labels = self.labels
        my_markers = " xo^*+psd"
        my_colors = ["","royalblue","darkviolet","red","limegreen","aqua","gold","hotpink","lightsalmon","black"]
        #my_colors = ["", "royalblue","red", "darkorchid", "navy", "aqua", "gold", "mediumpurple", "firebrick"]
        #my_colors = ["","#005eb8","#00AD83","#00a5d7","#f6511d","#ffb400", "#780116", "#1b998b","#a6e1fa"]
 
        for i in range(1,len(labels)):

            if df[labels[i]].isnull().values.any():
                print(f"SKIPPED (Empty column {labels[i]})")
                continue
            elif labels[0] in labels[i:]:
                print(f"SKIPPED (Ploting {labels[0]} against {labels[i]}")
                continue
            
            self.ax.scatter(x = df[labels[0]], y = df[labels[i]], label = format_legend(labels[i]), marker=my_markers[i], color = my_colors[i])
            [x_interpol, y_interpol] = interpolate(df[labels[0]],df[labels[i]],self.int_factor)
            try:
                self.ax.plot(x_interpol,y_interpol,'--',color=my_colors[i])
            except:
                continue
                


        # Set labels and legend
        #self.ax.legend(fontsize = 20)
        self.ax.legend(fontsize = 20)
        #self.ax.axis("tight")
        self.ax.set_xlabel(format_xlabel(labels[0]),fontsize = 20, fontweight = "bold")
        self.ax.set_ylabel(format_ylabel(labels[1]), fontsize = 20, fontweight = "bold")
        self.ax.tick_params(axis='both', which='major', labelsize=12)
        self.ax.grid(visible=True)

        #plt.show()
        
        return self.ax
    
    def find_name(self,dir):
        graph_name = find_file_name_short(dir)
        x_label = format_for_graph_name(self.labels[0])
        y_label = format_for_graph_name(self.labels[1])
        graph_name = graph_name + y_label + x_label
        return graph_name

    def find_name_multiple(self, dir):
        graph_name = find_file_name_long(dir)
        x_label = format_for_graph_name(self.labels[0])
        y_label = format_for_graph_name(self.labels[1])
        graph_name = "graf" + y_label + x_label
        return graph_name
    #===========================================================================================================================

    @property
    def int_factor(self):
        return self.__int_factor
    
    @int_factor.setter
    def int_factor(self, factor:int):
        self.__int_factor = factor


