import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


dir = r"U:\Ukoly\Eroze\data_posun_krivek\puvodni_data"

ref_9k = pd.read_excel(dir + "\\T671\\T671_9k.xlsx",header = None)
ref_12k = pd.read_excel(dir + "\\T671\\T671_12k.xlsx",header = None)
find_9k = pd.read_excel(dir + "\Ak1TD\Ak1TD_9k.xlsx",header = None)
find_12k = pd.DataFrame({0: ref_12k[0], 1: ref_12k[0]})

plt.scatter(find_9k[1],find_9k[0])
plt.scatter(ref_12k[1],ref_12k[0])
plt.scatter(ref_9k[1],ref_9k[0])


ref_9k_f = interp1d(ref_9k[0], ref_9k[1], 'cubic',fill_value="extrapolate")
ref_12k_f = interp1d(ref_12k[0], ref_12k[1], 'cubic',fill_value="extrapolate")
find_9k_f = interp1d(find_9k[0], find_9k[1], 'cubic',fill_value="extrapolate")

print(find_9k_f)

x = ref_12k[0]
y = ref_12k_f(x) + find_9k_f(x) - ref_9k_f(x)

plt.plot(y,x,'o--')
plt.show()

p_ref_9k = np.polyfit(ref_9k[0], ref_9k[1],6)
p_ref_12k = np.polyfit(ref_12k[0], ref_12k[1],6)
p_find_9k = np.polyfit(find_9k[0], find_9k[1],6)
p_find_12k = p_ref_12k + p_find_9k - p_ref_9k

func = np.poly1d(p_find_12k) 
find_12k[1] = func(ref_12k[0])
plt.scatter(find_12k[1], find_12k[0])




f = np.poly1d(p_ref_9k)
test = f(ref_9k[1])
plt.scatter(ref_9k[1],test)
plt.show()

print("done")