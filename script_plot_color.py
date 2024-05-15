
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('_mpl-gallery-nogrid')

# make data:
# np.random.seed(1)
# x = np.random.uniform(-3, 3, 256)
# y = np.random.uniform(-3, 3, 256)
# z = (1 - x/2 + x**5 + y**3) * np.exp(-x**2 - y**2)
# levels = np.linspace(z.min(), z.max(), 7)

# my data:
df = pd.read_csv("data/train.csv")
df.dropna(subset=["longitude", "latitude", "unitPrice"], inplace=True)
x = df["longitude"].values
x = x - x.min()
y = df["latitude"].values
y = y - y.min()
z = df["unitPrice"].values
z = z - z.min()
levels = np.linspace(z.min(), z.max(), 7)
print(len(x))

# plot:
fig, ax = plt.subplots()

ax.plot(x, y, 'o', markersize=1, color='grey')
ax.tricontourf(x, y, z, levels=levels)

ax.set(xlim=(x.min(), x.max()), ylim=(y.min(), y.max()))
plt.xlabel("longitude", fontsize=15)
plt.ylabel("latitude", fontsize=15)

plt.show()
