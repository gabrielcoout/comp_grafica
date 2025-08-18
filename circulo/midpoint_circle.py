import matplotlib.pyplot as plt
import numpy as np
from numpy import cos, sin, pi
import time

grid_lim = 500
R = 250

def circle_trig(R): 
    pontos = [] 
    for theta in np.linspace(0, 2*np.pi, 4*R*int(pi)):
        x = int(round(R * cos(theta))) 
        y = int(round(R * sin(theta))) 
        pontos.append((x, y)) 
    x = [p[0] for p in pontos] 
    y = [p[1] for p in pontos] 
    return x, y

def circle_incr(R):
    x = 0
    y = R
    d = 1 - R
    deltaE  = 3
    deltaSE = -2*R+5
    pontos = []
    pontos.append((x, y))
    while y>x:
        if d < 0:
            d += deltaE
            deltaE += 2
            deltaSE += 2
        else:
            d += deltaSE
            deltaE += 2
            deltaSE += 4
            y -= 1
        x += 1
        pontos.append((x, y))
    return pontos



start_time = time.time()
points = circle_trig(0, 0, R)
elapsed_time = time.time() - start_time
print(f"Tempo de execução para R={R}: {elapsed_time:.6f} s")
print(f"Número de pontos únicos: {len(points[0])}")

# Plotagem
fig, ax = plt.subplots(1,2,figsize=(12,5))

# Círculo teórico
circle = plt.Circle((0, 0), R, fill=False, color='red', label='Círculo teórico')
ax[0].add_patch(circle)

# Pontos do círculo discretizado
ax[0].set_title(f"Reta ($x_1$={0},$y_1$={0}) ($x_2$={R}, $y_2$={0})")
ax[0].plot(points[0], points[1], '.', label='Pontos discretos')

ax[0].set_xlim(0, grid_lim)
ax[0].set_ylim(0, grid_lim)
# ax[0].set_xticks(np.arange(0, grid_lim+1, 1))
# ax[0].set_yticks(np.arange(0, grid_lim+1, 1))
# ax[0].grid()
ax[0].legend()
ax[0].text(
                grid_lim*3//4,
                grid_lim*3//4,
                f"{elapsed_time:.10f} s",
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'),
                ha='center',
                va='center'
            )
plt.show()
