import os

def run():
    sablony = ["EZ","FC","GH", "GL"]
    jmena_velicin = ["Ma_2 [-]","Ma_RL1 [-]","rych_pomer_Akolo_stred_static_static [-]","rych_pomer_2stupen_stred_static_static [-]"]

    with open("S:\Rozvoj\\01_Experimental_Research\Ranš\T1MW_grafy\\Nastaveni_vykresleni_T1MW\Sablona\\sablona_T1MW.txt") as file:
        lines = file.readlines()


    for i in range(4):
        with open(f"S:\Rozvoj\\01_Experimental_Research\Ranš\T1MW_grafy\\Nastaveni_vykresleni_T1MW\Sablona\\{sablony[i]}.txt", mode="w") as write_file:
            lines[0] = jmena_velicin[i] + "\n"
            for line in lines:
                write_file.write(line)

    print("all done")
    return

def run_special():
    sablony = ["EZ","FC","GH", "GL"]
    jmena_velicin = ["Ma_2 [-]","Ma_RL1 [-]","rych_pomer_Akolo_stred_static_static [-]","rych_pomer_2stupen_stred_static_static [-]"]

    with open("S:\Rozvoj\\01_Experimental_Research\Ranš\T1MW_grafy\\Nastaveni_vykresleni\Sablona\\00_sablona_A_uprava_5_3_2024_interpolace.txt") as file:
        lines = file.readlines()


    for i in range(4):
        with open(f"S:\Rozvoj\\01_Experimental_Research\Ranš\T1MW_grafy\\Nastaveni_vykresleni\Sablona\\{sablony[i]}.txt", mode="w") as write_file:
            lines[0] = jmena_velicin[i] + "\n"
            for line in lines:
                write_file.write(line)

    print("all done")
    return

run()