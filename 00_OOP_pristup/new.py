import os 

zdrojove_data_dir = "S:/Rozvoj/01_Experimental_Research/Ranš/T1MW_grafy/Zdrojove_data_T1MW"
nastaveni_vykresleni_dir = "S:/Rozvoj/01_Experimental_Research/Ranš/T1MW_grafy/Nastaveni_vykresleni_T1MW"
vygenerovane_grafy_dir = "S:/Rozvoj/01_Experimental_Research/Ranš/T1MW_grafy/Vygenerovane_grafy_T1MW"


seznam_skupin_mereni = os.listdir(zdrojove_data_dir)
seznam_skupin_mereni = [skupina.replace(".xlsx","") for skupina in seznam_skupin_mereni]

for skupina in seznam_skupin_mereni:
    
    path0 = os.path.join(nastaveni_vykresleni_dir,skupina)
    if not os.path.isdir(path0):
          os.makedirs(path0)

    path1 = os.path.join(vygenerovane_grafy_dir,skupina)
    if not os.path.isdir(path1):
        os.makedirs(path1)
