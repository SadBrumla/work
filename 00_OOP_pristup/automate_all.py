import os 

zdrojove_data_dir = "S:/Rozvoj/01_Experimental_Research/Ranš/T1MW_grafy/Zdrojove_data_new"
nastaveni_vykresleni_dir = "S:/Rozvoj/01_Experimental_Research/Ranš/T1MW_grafy/Nastaveni_vykresleni_new"
vygenerovane_grafy_dir = "S:/Rozvoj/01_Experimental_Research/Ranš/T1MW_grafy/Vygenerovane_grafy_new"


seznam_skupin_mereni = os.listdir(zdrojove_data_dir)
seznam_skupin_mereni = [skupina.replace(".xlsx","") for skupina in seznam_skupin_mereni]