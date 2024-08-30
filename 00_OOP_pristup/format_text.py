import matplotlib.pyplot as plt
import os

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#=============================================================================================================

def format_ylabel(x):
    exceptions = ["c_0xp [m/s]", "c_4xp [m/s]", "c_2x [m/s]","c_6x [m/s]","c2x_us1 [-]","c6x_us2 [-]",
                  "s_0s [kJ*kg^-1*K^-1]","s_4s [kJ*kg^-1*K^-1]"]
    if x[:3] == "ro_" and "[kJ/kg]" in x:
        return "ρ [-]"

    if x in exceptions:
        if x[:2] == "s_":
            return "s [kJ/kg*K]"
        elif x[:2] == "c_":
            return "$\\mathregular{c_{x}}$ [m/s]"
        else:
            return "$\\mathregular{c_{x}}/\\mathregular{u_{s}}$ [-]"
        
    unit = " " + find_unit(x)

    x = x.split("_")
    if len(x) == 1:
        unit = ""

    if x[0] == "delta":
        x = math_greek(x[0])+x[1]
    else:
        x = math_greek(x[0])

    return x + unit

#=============================================================================================================
'''
def format_legend(x):
    if x == "c2x_us1 [-]":
        return "$\\mathregular{(c_{2x}/u_s)A}$"
    elif x == "c6x_us2 [-]":
        return "$\\mathregular{(c_{6x}/u_s)HP1}$"
    
    x = x.replace(" ","_")
    x = x.split("_")[:-1]
    i=0
    added_var = ""
    if x[0] == "delta":
        i = 1
        added_var = x[1]
    elif x[0] == "eps":
        if x[1][-1] == "1": 
            x[1] = x[1][:-1] + "A"
        elif x[1][-1] == "2":
            x[1] = x[1][:-1] + "HP1"

    elif x[0] == "eta":
        if x[1][0] == "1": 
            x[1] = "A" + x[1][1:]
        elif x[1][0] == "2":
            x[1] = "HP1" + x[1][1:]

    var = math_greek(x[0])
    subscript = edit_subscript(x[i+1:])

    output = "$\mathregular{" + var + added_var + "_{" + subscript + "}}$"
    return output

def edit_subscript(sub_list):
    output = ""
    dash_strings = ["tt", "ss","1tt","2tt","1ss","2ss", "Ass", "Att", "HP1ss", "HP1tt"]
    do_dash = True
    for sub in sub_list:
        output += sub
        
        if sub in dash_strings and do_dash :
            output += "/"
            do_dash = False

    return output
'''

#=============================================================================================================

def format_text(x,l_or_a):   
    text = "$"
    
    # if its a label
    if l_or_a == "l":
        x = x.replace(" ", "_")               
        x = x.split("_")
        x = x[0:-1]
        unit = ""

    # if its an axis
    elif l_or_a == "a":
        unit = " " + find_unit(x)
        x = x.split("_")
        x = [x[0]]
        return math_greek(x[0]) + unit

    else:
        print("CHYBA zadejte \"l\" nebo \"a\" ")
    
    text += math_greek(x[0])

    for i in x[1::]:
        text += "_{"
        text += i
        text += "}"

    text += "$"
    text += unit
    return text 


def find_unit(s):
    unit = s.split(" ")
    return unit[-1]


def math_greek(x):
    greek_alpha = ["eps", "phi", "ro", "eta","delta", "zeta", "tau"]
    math_greek_alpha = ["ε", "φ", "ρ", "η", "Δ", "ζ", "τ"]
    
    if x in greek_alpha:
        text = math_greek_alpha[greek_alpha.index(x)]
        
    else :
        text = x
    
    return text


def format_xlabel(x_label):

    if x_label == "rych_pomer_Akolo_stred_static_static [-]":
        return "$\\mathregular{(u_s/c_{is})A_{ss}}$ [-]"
    elif x_label == "rych_pomer_Akolo_pata_static_static [-]":
        return "$\\mathregular{(u_p/c_{is})A_{ss}}$ [-]"
    elif x_label == "rych_pomer_Akolo_stred_total_static [-]":
        return "$\\mathregular{(u_s/c_{is})A_{ts}}$ [-]"
    elif x_label == "rych_pomer_Akolo_pata_total_static [-]":
        return "$\\mathregular{(u_p/c_{is})A_{ts}}$ [-]"

    elif x_label == "rych_pomer_2stupen_stred_static_static [-]":
        return "$\\mathregular{(u_s/c_{is})HP1_{ss}}$ [-]"
    elif x_label == "rych_pomer_2stupen_pata_static_static [-]":
        return "$\\mathregular{(u_p/c_{is})HP1_{ss}}$ [-]"
    elif x_label == "rych_pomer_2stupen_stred_total_static [-]":
        return "$\\mathregular{(u_s/c_{is})HP1_{ts}}$ [-]"
    elif x_label == "rych_pomer_2stupen_pata_total_static [-]":
        return "$\\mathregular{(u_p/c_{is})HP1_{ts}}$ [-]"
    
    elif x_label == "Ma_2 [-]":
        return "$\\mathregular{Ma_{HP1}}$ [-]"
    elif x_label == "Ma_RL1 [-]":
        return "$\\mathregular{Ma_{RL1}}$ [-]"
    
    else:
        return format_ylabel(x_label)
    

def find_file_name_long(dir):
    file_name = os.path.basename(dir)
    return file_name



def find_file_name_short(dir):
    full_name = find_file_name_long(dir)
    short_name = full_name[9:31]
    return short_name


def find_graph_name(dir,x_name,y_name):
    pass




def format_for_graph_name(var):
    
    if var == "rych_pomer_Akolo [-]":
        return  "_Akolo" 
    
    elif var == "rych_pomer_Akolo_stred_static_static [-]":
        return "_Akolo_stred_ss"
    elif var == "rych_pomer_Akolo_pata_static_static [-]":
        return "_Akolo_pata_ss"
    elif var == "rych_pomer_Akolo_stred_total_static [-]":
        return "_Akolo_stred_ts"
    elif var == "rych_pomer_Akolo_pata_total_static [-]":
        return "_Akolo_pata_ts"

    elif var == "rych_pomer_2stupen_stred_static_static [-]":
        return "_2stup_stred_ss"
    elif var == "rych_pomer_2stupen_pata_static_static [-]":
        return "_2stup_pata_ss"
    elif var == "rych_pomer_2stupen_stred_total_static [-]":
        return "_2stup_stred_ts"
    elif var == "rych_pomer_2stupen_pata_total_static [-]":
        return "_2stup_pata_ts"
    
    else:
        jmeno = var.replace(" ","_").split("_")
        if len(jmeno) == 2:
            return "_" + jmeno[0]
        else:
            return "_" + jmeno[0] + "_" + jmeno[1]
    

def create_new_dir(parent_dir, name):
    path = os.path.join(parent_dir, name)
    os.makedirs(path)
    pass

# ==================================================================================================================

def format_legend(x):
    if x == "c2x_us1 [-]":
        return "$\\mathregular{(c_{2x}/u_s)A}$"
    elif x == "c6x_us2 [-]":
        return "$\\mathregular{(c_{6x}/u_s)HP1}$"
    
    x = x.replace(" ","_")
    x = x.split("_")[:-1]
    i=0
    added_var = ""
    if x[0] == "delta":
        i = 1
        added_var = x[1]

    elif x[0] in ["eps","h","Ma","Re","N", "ro"] and len(x) > 1 :
        if x[1][-1] == "1": 
            x[1] = x[1][:-1] + "A"
        elif x[1][-1] == "2":
            x[1] = x[1][:-1] + "HP1"

    elif x[0] == "G" and x[1][0] in ["r","o"]:
        if x[1][-1] == "1": 
            x[1] = x[1][:-1] + "A"
        elif x[1][-1] == "2":
            x[1] = x[1][:-1] + "HP1"

    elif x[0] == "eta":
        if x[1][0] == "1": 
            x[1] = "A" + x[1][1:]
        elif x[1][0] == "2":
            x[1] = "HP1" + x[1][1:]

    var = math_greek(x[0])
    subscript = edit_subscript(x[i+1:])

    output = "$\mathregular{" + var + added_var + "_{" + subscript + "}}$"
    return output

def edit_subscript(sub_list):
    output = ""
    dash_strings = ["tt", "ss","1tt","2tt","1ss","2ss", "Ass", "Att","HP1tt","HP1ss"]
    do_dash = True
    for sub in sub_list:
        output += sub
        
        if sub in dash_strings and do_dash :
            output += "/"
            do_dash = False

    return output

#===================================================================================================================
# UPDATE NA ÚPRAVU TEXTU

def format_legend_new(text):
    # vstup:    neupravená veličina např. h_issRL2 [kJ/kg], eps_pRL2 [-]
    # výstup:   upravená veličina ve formátu math regular, kde platí
    #               1) neobsahuje jednotku                  h_issRL2 [kJ/kg]    -> h_issRL2
    #               2) obsahuje korektní subscript          h_issRL2 [kJ/kg]    -> 
    #               3) převádí na řeckou abecedu            eps_pRL2 [-]        -> ε_pRL2
    #               4) převádí indexy 1 a 2 na A a HP1      eps_pRL2 [-]        -> ε_pRL HP1
    #               5) řeší problematiku c/u
    #               6) řeší problematiku delta  
    #
    # 1) a 2) platí pro všechny 
    # 3) platí pro ty kde první hodnota (při rozdělení .split("_")) náleží do seznamu vyjímek
    # 4) 
    # 5) platí pouze pro vyjímky c2x_us1 [-],c6x_us2 [-]

    # odstranění jednotky
    text = remove_unit(text)

    text = text.split("_")



    pass








def remove_unit(text):
    try:
        return text.split(" [")[0]
    except:
        print(f"ERROR: unable to remove unit \n returning: {text}")
        return text


def replace_greek(letter):
    greek_spelled = ["eps", "phi", "ro", "eta","delta", "zeta", "tau"]
    if letter in greek_spelled:
        greek_symbols = ["ε", "φ", "ρ", "η", "Δ", "ζ", "τ"]
        letter = greek_symbols[greek_spelled.index(letter)]
    return letter


def solve_greek(text):
    text = text.split("_")
    if text[0] == "delta":
        variable =  replace_greek(text[0]) + text[1]
    else:
        variable = math_greek(text[0])

    






#text = "delta_p_iss1 [kJ/kg]"
#text = remove_unit(text)
#print(solve_greek(text))

































# ======================================================================================================
#TESTING

'''
print(find_file_name("C:\Projects\VS_code\DOOSAN\20231122_4V-2.60bar-260C-2.2bar_1-89_bez_premosteni_puvodni_plus_domereni.xlsx"))
print(find_graph_name("C:\Projects\VS_code\DOOSAN\20231122_4V-2.60bar-260C-2.2bar_1-89_bez_premosteni_puvodni_plus_domereni.xlsx","Akolo","t_6"))


import random   
def y():
    yy = [0]*5
    for i in range (5):
        yy[i]=random.randint(10,20)
    return yy

    
x = [1,2,3,4,5]

typy_promenych = ["t_0ls_tt_tt [°C]","delta_p_uc [bar]","p_1sp [bar]","p_kkp1Al [bar]", "n_2 [ot/min]",
                  "G_pc [kg/hod]","eps_pOL2 [-]","h_isOL1 [kJ/kg]","zeta_k [-]"]

for funkce in typy_promenych:
    plt.scatter(x,y(),label = format_legend(funkce))

#plt.scatter(x,y,label = "$\\mathregular{ρ_{2tt/tt}}$")
plt.ylabel(format_ylabel("ro_2_tt [kJ/kg]"))
plt.legend()
plt.show()

'''