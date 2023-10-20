from matplotlib import pyplot as plt
import numpy as np
import plotly.graph_objects as go

T2 =5
# maximum single gate fidelity
def p_SQ(m, T2):
    return np.exp(-m*0.02*1.875/T2)
def F_SQ(m,T2):
    return (1-p_SQ(m,T2))/2 + p_SQ(m,T2)

m = np.linspace(0,100,101)
plt.xticks(np.linspace(0,100,11))
plt.title("Maximum gate fidelity when T2 = 5 us")
plt.xlabel("total m Clifford gates")
plt.ylabel("maximum fidelity F")
plt.grid()
plt.plot(m,F_SQ(m,T2))
plt.show()

def p_2Q(m, T2):
    return np.exp(-m*(0.02*8.25+0.025*1.5)/T2)
def F_2Q(m, T2):
    return (1-p_2Q(m,T2))/4 + p_2Q(m,T2)

m = np.linspace(0,20,21)
plt.xticks(np.linspace(0,20,11))
plt.title("Maximum gate fidelity when T2 = 5 us")
plt.xlabel("total m Clifford gates")
plt.ylabel("maximum fidelity F")
plt.grid()
plt.plot(m,F_2Q(m,T2))
plt.show()
# test