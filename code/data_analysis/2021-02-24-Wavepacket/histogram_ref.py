import pandas as pd
import matplotlib.pyplot as plt

time_tagger_file = "X:\\users\\jamesbate\\_Histogram_2021-02-24_15-27-22_.txt"
#time_tagger_file = "X:\\users\\jamesbate\\_Histogram-2_2021-02-24_15-26-34_.txt"


data = pd.read_csv(time_tagger_file, delimiter = "\t")
time = data['time(ps)']
counts = data['counts']


dt = time[1] - time[0]

print(dt)


plt.bar(time, counts, width = dt)
plt.show()