import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def find_names(dir):
    return os.listdir(dir)


def find_df(dir, name):
    j = 0
    df = pd.DataFrame()
    df = pd.read_excel(dir +"\\"+ name, header = None)
    name = name.removesuffix(".xlsx")
    df.columns = [name + "_wet", name + "_ero"]

    return df


def combine_dataframes(T_ref, T_new, XYZ_ref):
    df = pd.concat([T_ref, T_new, XYZ_ref], axis= 1)

    return df
    


# načtení všech dat máteriálů do listu all_materials
material_dir = r"U:\Ukoly\Eroze\automatizace\puvodni_soubory"
material_names = find_names(material_dir)
all_materials = []

for material_name in material_names:
    material_list = [None]*5
    xlsx_names = find_names(material_dir + "\\" + material_name)

    for xlxs_name in xlsx_names:
        if "9k" in xlxs_name:
            material_list[0] = find_df(material_dir + "\\" + material_name, xlxs_name)
        if "10k" in xlxs_name:
            material_list[1] = find_df(material_dir + "\\" + material_name, xlxs_name)
        if "11k" in xlxs_name:
            material_list[2] = find_df(material_dir + "\\" + material_name, xlxs_name)
        if "12k" in xlxs_name:
            material_list[3] = find_df(material_dir + "\\" + material_name, xlxs_name)
        if "14k" in xlxs_name:
            material_list[4] = find_df(material_dir + "\\" + material_name, xlxs_name)

    all_materials.append(material_list)




# oddělení materiálu T který použiji k odvození ubytku v jiných režimech
T_material = all_materials[4]


# vytvoření jednotlivých dataframes obsahujících vlhkost a erozi od T_ref, T_new, XYZ_ref
list_of_dfs = []
other_material_refs = []
for other_material in all_materials:
    
    for regime_num in range(len(other_material)-1,0,-1):
        if isinstance(other_material[regime_num], pd.DataFrame):
            
            break
    
    
    for T_regime in T_material:

        df = combine_dataframes(T_material[regime_num], T_regime, other_material[regime_num])
        #df = df.dropna(axis=0)

        list_of_dfs.append(df)
        


# hledání funkce pro prložení a vytvroření dat XYZ

for i in range(len(list_of_dfs)):
    columns = list(list_of_dfs[i].columns)
    T_ref_f = interp1d(list_of_dfs[i].iloc[:,1].dropna(), list_of_dfs[i].iloc[:,0].dropna(), 'linear',fill_value="extrapolate")
    T_new_f = interp1d(list_of_dfs[i].iloc[:,3].dropna(), list_of_dfs[i].iloc[:,2].dropna(), 'linear',fill_value="extrapolate")
    XYZ_ref_f = interp1d(list_of_dfs[i].iloc[:,5].dropna(), list_of_dfs[i].iloc[:,4].dropna(), 'linear',fill_value="extrapolate")

    max = list_of_dfs[i].iloc[:,[1,3,5]].max().min()
    min = list_of_dfs[i].iloc[:,[1,3,5]].min().max()


    name_stop = columns[4].index("_")
    name = columns[4][:name_stop] + columns[3][-8:-3]

    x = np.linspace(min,max,list_of_dfs[i].shape[0])
    
    list_of_dfs[i][name + "wet"] = T_new_f(x) + XYZ_ref_f(x) - T_ref_f(x)
    list_of_dfs[i][name + "ero"] = x



        



# vykreslení
for i in range(len(list_of_dfs)):
    if list_of_dfs[i].shape[1] == 6:
        continue
    plt.figure(i)
    plt.title(list_of_dfs[i].columns[6])
    plt.scatter(list_of_dfs[i].iloc[:,0],list_of_dfs[i].iloc[:,1])
    plt.scatter(list_of_dfs[i].iloc[:,2],list_of_dfs[i].iloc[:,3])
    plt.scatter(list_of_dfs[i].iloc[:,4],list_of_dfs[i].iloc[:,5])
    plt.plot(list_of_dfs[i].iloc[:,6],list_of_dfs[i].iloc[:,7] ,'ro--')
    plt.xlabel("wettness [?]")
    plt.ylabel("erosion [?]")
    plt.legend(["T_ref", "T_new", "XYZ_ref", "XYZ_new"])
    plt.savefig(r"vygenerovane_grafy\\ " + list_of_dfs[i].columns[6])
    plt.close(i)

    # uložit data   
    list_of_dfs[i].to_excel(r"vygenerovana_data\\ " + list_of_dfs[i].columns[6] + ".xlsx",index = False)


"""
for i in range(len(list_of_dfs)):
    plt.scatter(list_of_dfs[i].iloc[:,1],list_of_dfs[i].iloc[:,0])
    plt.scatter(list_of_dfs[i].iloc[:,3],list_of_dfs[i].iloc[:,2])
    plt.scatter(list_of_dfs[i].iloc[:,5],list_of_dfs[i].iloc[:,4])
    plt.plot(list_of_dfs[i]["new_e"],list_of_dfs[i]["new_w"] ,'ro--')
    plt.show()

"""


