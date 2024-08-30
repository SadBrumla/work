# funkce
import pandas as pd
import os

def load_settings(dir):
    settings=[]
    with open(dir,encoding="unicode_escape") as file:
        for line in file.readlines():
            settings.append(line.strip())
    settings = modify_settings(settings)
    return settings


def modify_settings(settings):
    settings_new = []
    for line in settings:
        graph_setting = line.split(",")
        settings_new.append(graph_setting)
    return settings_new


def load_excel_keys(dir):
    df1 = pd.read_excel(dir, sheet_name="Vstupní data",header=1)
    df2 = pd.read_excel(dir, sheet_name="Výsledky",header=2)
    try:
        df2.rename(columns={'[[ ID ]]': 'ID [-]'}, inplace=True)
    except:
        print("couldnt rename ID column")
    
    df = pd.merge(df1,df2, on="ID [-]", how="inner")
    df_keys = list(df.keys())
    for i in range(len(df_keys)):
        if df_keys[i][-2:] == "_x":
            df_keys[i] = df_keys[i][:-2]
    return df_keys


def map_keys_to_cols(keys):
    col_names = []
    for i in range(0,len(keys)):
        if i//26 == 0:
            first_letter = ""
        else:
            first_letter = chr(i//26 -1 + 65)
        col_name = first_letter + chr(i%26 + 65)
        col_names.append(col_name)
    return col_names


def create_collumn_settings(vars, cols, settings_var_names):
    settings_col_names = []
    first = False
    for var_names in settings_var_names:


        col_list = []
        for var in var_names:
            if first:
                col_list.append(var)
                first = False
                continue

            if isinstance(var_names,list):
                try:
                    i = vars.index(var)
                    col_list.append(cols[i])
                except:
                    continue
            else:
                col_list = var_names

        first = True

        settings_col_names.append(col_list)   
    return settings_col_names


def save_col_settings(col_settings, dir):
    with open(dir, mode="w") as file:
        file.write("xdata\n")
        file.write(col_settings[0][0])
        file.write("\n")
        file.write("ydata\n")
        for graph_vars in col_settings[1::]:
            for var in graph_vars:
                file.write(var)
                file.write(" ")
            file.write(",")
        file.write("\ninterpolation:\n")
        file.write("2")
        pass



def write_var_names_settings(keys):
    with open(file="S:/Rozvoj/01_Experimental_Research/Ranš/T1MW_grafy/Nastaveni_vykresleni/Sablona/00_vsechny_veliciny.txt", mode="w") as file:
        for key in keys:
            try:
                file.write(key)
                file.write(",\n")
            except:
                print(f"variable failed: {key}")

def create_var_names_settings():
    dir = "S:/Rozvoj/01_Experimental_Research/Ranš/T1MW_grafy/Zdrojove_data/4V-2.6bar-260C-2.20bar_u-cis_Akolo_bez_premosteni_1-89.xlsx"
    keys = load_excel_keys(dir)
    write_var_names_settings(keys)
    pass

#====================================================================================================================================
# TESTS

def test_map_keys_to_cols():
    dir = "S:/Rozvoj/01_Experimental_Research/Ranš/T1MW_grafy/Zdrojove_data/4V-2.6bar-260C-2.20bar_u-cis_Akolo_bez_premosteni_1-89.xlsx"
    keys = load_excel_keys(dir)
    df_map = map_keys_to_cols(keys)

    print(df_map)

def create_col_setting(excel_dir,var_settings_dir, col_settings_dir):
    excel_vars = load_excel_keys(excel_dir)
    settings = load_settings(var_settings_dir)
    col_names = map_keys_to_cols(excel_vars)
    col_settings = create_collumn_settings(excel_vars,col_names,settings)
    save_col_settings(col_settings, col_settings_dir) 
    
    pass



#==============================================================================================================================================

def create_all_settings(dir,datasets,x_cols_set):
    
    for i in range(len(datasets)):
        excel_dir = dir + "/Zdrojove_data_T1MW/" + datasets[i] +".xlsx"
        
        x_cols = x_cols_set[i].split(",")
        for x_col in x_cols:
            var_settings_dir = dir + "/Nastaveni_vykresleni_T1MW/Sablona/" + x_col + ".txt"
            col_settings_dir = dir + "/Nastaveni_vykresleni_T1MW/" + datasets[i] + "/" + x_col + ".txt"
            create_col_setting(excel_dir,var_settings_dir,col_settings_dir)

    print("all done")
        




#===============================================================================================================================================
#settings    
dir = "S:/Rozvoj/01_Experimental_Research/Ranš/T1MW_grafy"


datasets = [
            "2V_3.0bar_260C_2.15bar_u-cis_Akolo_bez_premosteni_3-59",
            "2V_3.4bar_260C_1.53bar_na_1.20bar_MaRLA-kolo-1_bez_premosteni_104-139",
            "3V_2.9bar_260C_2.20bar_na_2.37bar_min_spad_bez_premosteni_473,474,526,527",
            "3V_2.9bar_260C_2.20bar_na_2.37bar_min_spad_s_premostenim_473,474,526,527",
            "3V_2.9bar_260C_2.27bar_u-cis_bez_premosteni_540-588",
            "3V_2.9bar_260C_2.27bar_u-cis_s_premostenim_540-588",
            "3V-2.4bar-260C-1.40bar-u-cis_bez_premosteni_200-302",
            "3V-2.4bar-260C-1.40bar-u-cis_s_premostenim_200-302",
            "3V-2.4bar-260C-2.20_na_1.04bar_bez_premosteni_475_510",
            "3V-2.4bar-260C-2.20_na_1.04bar_s_premostenim_475_510",
            "3V-2.66bar-260C-1.90bar-223C-2500--4300_312-359_bez_premosteni",
            "4V-2.6bar-260C-2.20bar_u-cis_Akolo_bez_premosteni_1-89"
            ]

x_cols = ["GH,GL", "FC,EZ", "FC,EZ","FC,EZ", "GH,GL","GH,GL","GH,GL","GH,GL", "FC,EZ,GH,GL", "FC,EZ,GH,GL","FC,EZ,GH,GL", "GH,GL"]

dict_cols_to_vars = {"GH":"rych_pomer_Akolo_stred_static_static [-]",
                     "GL":"rych_pomer_2stupen_stred_static_static [-]",
                     "FC":"Ma_RL1 [-]",
                     "EZ":"Ma_2 [-]"}

datasets = os.listdir("S:\Rozvoj\\01_Experimental_Research\Ranš\T1MW_grafy\\Nastaveni_vykresleni_T1MW")[:-1]

x_cols = ["GH,GL","FC,EZ",
          "GH,GL","GH,GL","GH,GL","FC,EZ","FC,EZ","FC,EZ",
          "GH,GL"]

create_all_settings(dir,datasets,x_cols)
