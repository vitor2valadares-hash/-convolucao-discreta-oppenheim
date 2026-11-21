"""
Simulação dinâmica da Convolução Discreta (Exemplo 2.4 - Oppenheim & Willsky, 2ª Ed.).
Visualiza passo a passo o espelhamento, deslocamento e somatório de convolução y[n] = x[n] * h[n].
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

alpha = 1.5 
p = 13
n_eixo = np.arange(-2, p)
ticks_x = list(range(-2, p))

# m -> j
def x_func(m):
    return np.where((m >= 0) & (m <= 4), 1.0, 0.0)

def h_func(m):
    return np.where((m >= 0) & (m <= 6), alpha**m, 0.0)

j_eixo = np.arange(-10, 20)

y_completo = []

for n in n_eixo:
    v_soma = np.sum(x_func(j_eixo) * h_func(n - j_eixo))
    y_completo.append(v_soma)
max_y = max(y_completo)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

def update(frame):
    n_atual = n_eixo[frame]
    
    ax1.clear()
    ax2.clear()
    ax3.clear()
    
    # ------------------ Subplot 1: Sinal fixo x[j] ------------------
    valores_x = x_func(j_eixo)
    marker1, stem1, baseline1 = ax1.stem(j_eixo, valores_x, linefmt='b-', markerfmt='bo', label=r"$x[j]$")
    baseline1.set_visible(False)
    marker1.set_markersize(6)
    ax1.set_xlim(-5, p + 2)
    ax1.set_ylim(-0.1, 2)
    ax1.set_xticks(ticks_x)
    ax1.set_xticklabels([])
    ax1.grid(True)
    ax1.legend(loc="upper left")
    ax1.set_title(f"Processo de Convolução Discreta (Instante Atual: n = {n_atual})", fontsize=12)

    # ------------------ Subplot 2: Sinal invertido e deslocado h[n - j] ------------------
    valores_h_deslocado = h_func(n_atual - j_eixo)
    marker2, stem2, baseline2 = ax2.stem(j_eixo, valores_h_deslocado, linefmt='C1-', markerfmt='C1o', label=f"$h[{n_atual} - j]$")
    baseline2.set_visible(False)
    marker2.set_markersize(6)
    ax2.set_xlim(-5, p + 2)
    ax2.set_ylim(-0.9, h_func(6) * 1.2)
    ax2.set_xticks(ticks_x)
    ax2.set_xticklabels([])
    ax2.grid(True)
    ax2.legend(loc='upper left')

    # ------------------ Subplot 3: Resultado acumulado y[n] ------------------
    n_ate_agora = n_eixo[:frame+1]
    y_ate_agora = y_completo[:frame+1]
    
    if len(n_ate_agora) > 0:
        marker3, stem3, baseline3 = ax3.stem(n_ate_agora, y_ate_agora, linefmt='g-', markerfmt='go', label=r"$y[n]$")
        baseline3.set_visible(False)
        marker3.set_markersize(7)
        
    ax3.set_xlim(-5, p + 2)
    ax3.set_ylim(-max_y * 0.1, max_y * 1.4)
    ax3.set_xticks(ticks_x)
    ax3.grid(True)
    ax3.legend(loc='upper left')
    
    texto_formulas = (
        r"$y[n] = 0$, $n < 0$ ou $n > 10$" + "\n" + 
        r"$y[n] = \frac{1-\alpha^{n+1}}{1-\alpha}$, $0 \leq n \leq 4$" + "\n" + 
        r"$y[n] = \alpha^{n-4}(\frac{1-\alpha^5}{1-\alpha})$, $4 < n \leq 6$" + "\n" + 
        r"$y[n] = \frac{\alpha^{n-4} - \alpha^7}{1-\alpha}$, $ 6 < n \leq 10$"
    )
    ax3.text(0.80, 0.95, texto_formulas, transform=ax3.transAxes, fontsize=9,
             verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.7, edgecolor='gray'))

    plt.tight_layout()

ani = FuncAnimation(fig, update, frames=len(n_eixo), interval=1000, repeat=True)
ani.save(filename=r"convolucao.gif", writer="ffmpeg")
plt.show()
