import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dir = r"U:\Ukoly\Eroze\data_posun_krivek\puvodni_data\\"
find_9k = pd.read_excel(dir + "Ak1TD_LK_9k.xlsx",header = None)
ref_9k = pd.read_excel(dir + "T671_9k.xlsx",header = None)
ref_12k = pd.read_excel(dir + "T671_12k.xlsx",header = None)


ref_poly_9k = np.polyfit(ref_9k[0],ref_9k[1],2)
ref_poly_12k = np.polyfit(ref_12k[0],ref_12k[1],2)
find_poly_9k = np.polyfit(find_9k[0],find_9k[1],2)




find_poly_12k = ref_poly_12k + find_poly_9k - ref_poly_9k

print(f"{ref_poly_12k} \n  + {find_poly_9k} \n {ref_poly_9k} \n ----------------------------- \n {find_poly_12k}")

find_12k = np.polyval(find_poly_12k, ref_12k[1])

test_ref_9k = np.polyval(ref_poly_9k, ref_9k[1])

result = pd.DataFrame({'vlhkost':ref_12k[0],'ubytek': find_12k})


plt.sc



plt.scatter(find_9k[0], find_9k[1])
plt.scatter(ref_9k[0], ref_9k[1])
plt.scatter(ref_12k[0], ref_12k[1])
plt.scatter(result.vlhkost, result.ubytek)
plt.scatter(test_ref_9k, ref_9k[1])
plt.show()

#print(df)