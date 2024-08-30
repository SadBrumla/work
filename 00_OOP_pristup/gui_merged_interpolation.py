import os
import tkinter as tk
import pandas as pd
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graphgenerator import *
from format_text import *
from graph import Graph

class GraphGeneratorApp:

    def __init__(self, master):
        '''
        defininton of variables after initialion of the app
        '''
        # master refers to the window itself
        self.master = master
        self.master.title("Graph Generator")

        #==========================================================================================================================

        # define values that will be used to store user data

        self.directory_df = "S:\Rozvoj\\01_Experimental_Research\Ranš\T1MW_grafy\Zdrojove_data\\2V_3.0bar_260C_2.15bar_u-cis_Akolo_bez_premosteni_3-59.xlsx"
        self.file_name = self.directory_df.split("\\")
        self.file_name = self.file_name[-1]
        self.df = pd.DataFrame()
        self.df_graph = pd.DataFrame()
        self.data_x = tk.StringVar(value = "kq")
        self.data_y = tk.StringVar(value = "mq mp")
        self.message = tk.StringVar()
        self.directory_save = tk.StringVar()
        self.interpol_factor = tk.StringVar(master)
        self.interpol_factor.set(value="0 - Choose interpolation settings:")
        self.main_dir = "S:\Rozvoj\\01_Experimental_Research\Ranš\T1MW_grafy"
        #self.directory_settings = tk.StringVar()

        #==========================================================================================================================
        # DEFINE FIGURE
        self.graph = Graph()
        self.fig = self.graph.define_figure()

        #==========================================================================================================================
        # CREATE TKinter THINGS (labels, entries, buttons and scroll menus)

        # label with the file name 
        fn_text = self.file_name
        self.l_fn = tk.Label(master, text= fn_text)
        
        
        # entry for x values
        self.l_x1 = tk.Label(master, text="X Data: ")
        self.e_x1 = tk.Entry(master, textvariable=self.data_x)
        #self.l_x2 = tk.Label(master, text="Vlože KL nebo KM (KL=A kolo, KM=2.stupen)")

        # entry for y values
        self.l_y1 = tk.Label(master, text="Y Data: ")
        self.e_y1 = tk.Entry(master, textvariable=self.data_y)
        #self.l_y2 = tk.Label(master, text="Vložte indexy sloupců pro zobrazení oddělené čárkou (např. N,O,P,Q)")

        # buttons
        self.b_generate =   tk.Button(master, text="Generate Graph",            command=self.plot_graph)
        self.b_save =       tk.Button(master, text="Save Graph",                command=self.ask_save_graph)
        self.b_load =       tk.Button(master, text="Load data",                 command=self.ask_load_excel)
        self.b_multiple =   tk.Button(master, text="Generate multiple graphs",  command=self.generate_multiple)
        self.b_all =        tk.Button(master, text="Generate all graphs",  command=self.generate_all_graphs)
        
        # "Interpolation" option menu
        interpolation_menu_opt = ["0 - No interpolation",   
                                  "1 - Linear interpolation",
                                  "2 - 2nd polynomial interpolation",
                                  "3 - 3rd polynomial interpolation",
                                  "4 - 4th polynomial interpolation"]
        self.om_interpolation = tk.OptionMenu(master, self.interpol_factor, *interpolation_menu_opt)

        # message 
        self.messagebox = tk.Label(master, bg="grey", textvariable = self.message, justify="left",anchor="w")

        # Canvas
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self.master) 

        #==========================================================================================================================

        # Place things into master

        # load directory
        self.l_fn.grid(row = 0, column=0, columnspan= 2, pady=10, padx = 10, sticky="w")
        self.b_load.grid(row = 1, column=0, columnspan= 2, pady=10, padx = 10, sticky="we")
        
        # entry for x values
        self.l_x1.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.e_x1.grid(row=2, column=1, padx=10, pady=5, sticky="we")
        #self.l_x2.grid(row=2, column=0, padx=10, pady=5, sticky="we", columnspan= 2)

        # entry for y values
        self.l_y1.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.e_y1.grid(row=3, column=1, padx=10, pady=5, sticky="we")
        #self.l_y2.grid(row=4, column=0, padx=10, pady=5, sticky="we", columnspan= 2)

        # option menu
        self.om_interpolation.grid(row=5, column=0, columnspan= 2, padx=10, pady=5, sticky="we")

        # buttons
        self.b_generate.grid(row=6, column=0, columnspan= 2, pady=10, padx = 10, sticky="we")
        self.b_save.grid    (row=7, column=0, columnspan= 2, pady=10,  padx = 10, sticky="we")
        self.b_multiple.grid(row=8, column=0, columnspan= 2, pady=10,  padx = 10, sticky="we")
        self.b_all.grid     (row=9, column=0, columnspan= 2, pady=10,  padx = 10, sticky="we")
        # message
        self.messagebox.grid(row = 19, column=0, columnspan= 2, pady=10,  padx = 10, sticky="we")


        # canvas
        self.plot_canvas.get_tk_widget().grid(row=0, column=2, rowspan=20)

        self.load_excel()

        #end of __init__
        #==========================================================================================================================


    #==========================================================================================================================
    # BUTTON FUNCTIONS (they are called when buttons are pressed)
    def ask_load_excel(self):
        self.directory_df = filedialog.askopenfilename(initialdir="S:\Rozvoj\\01_Experimental_Research\Ranš\T1MW_grafy\Zdrojove_data")
        self.load_excel()

    def load_excel(self):
        self.file_name = find_file_name_long(self.directory_df)
        fn_text = self.file_name
        self.l_fn.config(text = fn_text)
        df1 = pd.read_excel(self.directory_df, sheet_name="Vstupní data",header=1)
        df2 = pd.read_excel(self.directory_df, sheet_name="Výsledky",header = 2)
        self.df = pd.merge(df1,df2, on="ID [-]", how="inner")
        self.df.columns = self.df.columns.str.strip("_x")
        self.message.set(value="Excel file loaded")

    #---------------------------------------------------------------------------------------------------------------
        
    def plot_graph(self):

        self.fig.clear()

        x_string = self.e_x1.get().upper()
        y_string = self.e_y1.get().upper().replace(" ",",")
        int_factor = self.get_interpol_factor()

        self.df_graph = find_sub_df(self.df, x_string, y_string)

        self.graph.initlize(self.df_graph, int_factor)
        self.ax = self.graph.plot_axes(fig = self.fig)
        self.graph_name = self.graph.find_name(self.directory_df)

        self.plot_canvas.draw()

        self.message.set(value="Graph ploted")


    #---------------------------------------------------------------------------------------------------------------
    def ask_save_graph(self):
        file = filedialog.asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")),
                                            defaultextension='.png', title="Save graph as",
                                            initialfile=self.graph_name)
        self.fig.savefig(file)


    def ask_safe_graph(self):
        self.directory_save = filedialog.askdirectory()
        if self.directory_save:
            self.save_graph()

    def save_graph(self):
        i = 0
        counter = ""
        file_path = f"{self.directory_save}/{self.graph_name}.png"
        while os.path.isfile(file_path):
            file_path = f"{self.directory_save}/{self.graph_name}_{i}.png"
            i += 1
            counter = "_" + str(i)
        file_path = f"{self.directory_save}/{self.graph_name}{counter}.png"
        self.fig.savefig(file_path)

        self.message.set(value="Graph saved")

        pass
        
    #-----------------------------------------------------------------------------------------------------------------------
    # GENERATE MULTIPLE GRAPHS

    def generate_multiple(self):

        self.fig.clear()

        settings = self.load_settings()

        data_x = settings[0]
        list_data_y = settings[1].split(",")
        # interpol factor je na první pozici v list_data_y
        self.ask_directory()

        for data_y in list_data_y:
            try:
                int_factor = int(data_y[0])
            except:
                int_factor = 0 
                print(f"skipped int_factor for {data_y}\n using int_factor = 0")
            data_y = data_y[1:]
            data_y = data_y.strip()
            self.fig.clear()
            self.df_graph = find_sub_df(self.df, data_x, data_y)
            self.graph.initlize(self.df_graph, int(int_factor))
            self.ax = self.graph.plot_axes(fig = self.fig)
            self.graph_name = self.graph.find_name_multiple(self.directory_df)
            self.save_graph()



    def ask_directory(self, type = "Save"):
        if type == "Save":
            self.directory_save = filedialog.askdirectory(title="Select save direcory", 
                                                            initialdir="S:\Rozvoj\\01_Experimental_Research\Ranš\T1MW_grafy\Vygenerovane_grafy")

        elif type == "Load":
            self.directory_load = filedialog.askdirectory(title="Select load direcory", 
                                                            initialdir="S:\Rozvoj\\01_Experimental_Research\Ranš\T1MW_grafy")

    def load_settings(self):
        file_name = filedialog.askopenfilename(title="Select settings file", filetypes= (('text files', '*.txt'),("All Files", "*.*")),
                                               initialdir="S:\Rozvoj\\01_Experimental_Research\Ranš\T1MW_grafy\\Nastaveni_vykresleni")
        with open(file_name) as f:
            lines = f.read().splitlines()


        settings = lines[1::2]
        return settings


    #==========================================================================================================================
    # GENERATE ALL GRAPHS
    
    def generate_all_graphs(self):

        NAME_OF_XLSX_FOLDER = "Zdrojove_data_T1MW"
        NAME_OF_SETTINGS_FOLDER = "Nastaveni_vykresleni_T1MW"
        NAME_OF_GRAPH_FOLDER = "Vygenerovane_grafy_T1MW"
        
        # ask a directory that contains only excel files
        self.ask_directory(type = "Load")
        
        # read all files in this directory
        self.read_xlsx_names()

        checkboxes = self.choose_xlsx_names()
        self.get_selected_options(checkboxes)


        # loop loading excels 
        for xlsx_name in self.xlsx_names:
            
            # define the working folders
            self.directory_xlsx =       os.path.join(self.main_dir, NAME_OF_XLSX_FOLDER, xlsx_name + ".xlsx")
            self.directory_settings =   os.path.join(self.main_dir, NAME_OF_SETTINGS_FOLDER, xlsx_name)
            self.directory_graphs =     os.path.join(self.main_dir, NAME_OF_GRAPH_FOLDER, xlsx_name)

            self.load_xlsx()

            # find settings for specific excel (eg. EZ, F)
            setting_names = self.read_txt_names()

            # settings for this excel (for example list of rows ploted against FC)
            settings = []

            for setting_name in setting_names:
                setting_list = (self.read_settings(self.directory_settings,setting_name+".txt"))
                settings.append([setting_list[0],setting_list[1].split(",")])

            
            for i in range(len(settings)):
                data_x = settings[i][0]

                self.generate_graph_folder(setting_names[i])

                for data_y in settings[i][1]:
                    try:
                        int_factor = int(data_y[0])
                    except:
                        int_factor = 0 
                        print(f"skipped int_factor for {data_y}\n using int_factor = 0")
                    data_y = data_y[1:]
                    data_y = data_y.strip()

                    self.fig.clear()
                    self.df_graph = find_sub_df(self.df, data_x, data_y)
                    self.graph.initlize(self.df_graph, int(int_factor))
                    self.ax = self.graph.plot_axes(fig = self.fig)
                    self.graph_name = self.graph.find_name_multiple(self.directory_df)
                    self.save_graph_all()


    def choose_xlsx_names(self):

        popup = tk.Toplevel()
        popup.title("Select files")
        checkboxes = []
        okVar = tk.IntVar()
        
        for xlsx_name in self.xlsx_names:
            var = tk.IntVar(value=1)
            checkbox = tk.Checkbutton(popup, text=xlsx_name, variable=var)
            checkbox.pack()
            checkboxes.append((xlsx_name, var))
        

        ok_button = tk.Button(popup, text="OK", command=lambda: okVar.set(1))
        ok_button.pack()

        popup.wait_variable(okVar)
        popup.destroy()

        return checkboxes

    
    def get_selected_options(self, checkboxes):

        self.xlsx_names = [option for option, var in checkboxes if var.get() == 1]
        print("Selected options:", self.xlsx_names)


        


    def generate_graph_folder(self,data_x):
        self.directory_graphs_exact = f"{self.directory_graphs}/{data_x}"
        if not os.path.exists(self.directory_graphs_exact):
            os.makedirs(self.directory_graphs_exact)
        



    def save_graph_all(self):
        i = 0
        counter = ""
        file_path = f"{self.directory_graphs_exact}/{self.graph_name}.png"
        while os.path.isfile(file_path):
            file_path = f"{self.directory_graphs_exact}/{self.graph_name}_{i}.png"
            i += 1
            counter = "_" + str(i)
        file_path = f"{self.directory_graphs_exact}/{self.graph_name}{counter}.png"
        self.fig.savefig(file_path)

        self.message.set(value="Graph saved")        

    # find all .txt files listed in path directory (retturs list of ["EZ","FC","GH","GL"])
    def read_txt_names(self):
        setting_names = os.listdir(self.directory_settings)
        setting_names = [name.replace(".txt","") for name in setting_names]
        return setting_names

            

    # open .txt file (eg.: EZ.txt) file and read 2nd 4th and 6th line, return them as a list of three strings
    def read_settings(self,path,setting_name):
            setting_dir = os.path.join(path,setting_name) 
            with open(setting_dir) as f:
                lines = f.read().splitlines()
            setting = lines[1:4:2]
            return setting

       


    def read_xlsx_names(self):
        self.xlsx_names = os.listdir(self.directory_load)
        self.xlsx_names = [name.replace(".xlsx","") for name in self.xlsx_names]

    
    def load_xlsx(self):
        df1 = pd.read_excel(self.directory_xlsx, sheet_name="Vstupní data",header=1)
        df2 = pd.read_excel(self.directory_xlsx, sheet_name="Výsledky",header = 2)
        self.df = pd.merge(df1,df2, on="ID [-]", how="inner")
        self.df.columns = self.df.columns.str.strip("_x")




    #==========================================================================================================================
    # OTHER FUNCTIONS

    def get_interpol_factor(self):
        int_factor = int(self.interpol_factor.get()[0])
        return int_factor


#==================================================================================================================================


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphGeneratorApp(root)
    root.mainloop()