import matplotlib.pyplot as plt
import numpy as np


a = 0.6
b = 0.02
c = 0.5
d = 0.01
r = 0.3
k = 0.009

dt = 0.005
steps = 50000


x = 100
y = 5
z = 50

# Listen zur Speicherung der Werte
t_values = [0]
x_values = [x]
y_values = [y]
z_values = [z]


for step in range(steps):
    dx = (a * x - b * x * y + k * x * z) * dt
    dy = (-c * y + d * x * y) * dt
    dz = (r * z - k * x * z) * dt


    x = max(0, x + dx)
    y = max(0, y + dy)
    z = max(0, z + dz)


    t_values.append(t_values[-1] + dt)
    x_values.append(x)
    y_values.append(y)
    z_values.append(z)


x_mean = np.mean(x_values)
y_mean = np.mean(y_values)


fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlabel("Zeit")
ax.set_ylabel("Population / Menge")
ax.set_title("Lotka-Volterra Simulation (statisch)")


ax.plot(t_values, x_values, label="Beutetiere (x)", color='blue')
ax.plot(t_values, y_values, label="Räuber (y)", color='red')
ax.plot(t_values, z_values, label="Nahrung (z)", color='green')
ax.axhline(y=x_mean, color='blue', linestyle='--', label="Mittelwert x")
ax.axhline(y=y_mean, color='red', linestyle='--', label="Mittelwert y")


ax.text(0.02, 0.95, f"Mittlere x (Beutetiere): {x_mean:.2f}\nMittlere y (Räuber): {y_mean:.2f}",
        transform=ax.transAxes, fontsize=10, verticalalignment='center_baseline')

ax.legend()
plt.show()
