import numpy as np
import matplotlib.pyplot as plt
import pprint
from scipy.optimize import curve_fit
from math import isnan, isinf

from configuration import *

# Load the npz file
# npz_file = np.load(save_dir/'XEB_q4_5_seqs(77)_depth(7)_avgs(101)_random_gates(3).npz')
# npz_file = np.load(save_dir/'XEB_test.npz')
# Hero:
npz_file = np.load(save_dir/'XEB_q4_5_seqs(80)_depth(7)_avgs(100)_random_gates(3).npz')

# Create an empty dictionary to store variables
variables = {}

# Iterate through keys and store variables in the dictionary
for key in npz_file.files:
    variables[key] = npz_file[key]

# Close the npz file after loading the data
npz_file.close()

# # Example of accessing variables directly
g1 = variables['g1'] 
g2 = variables['g2'] 
state00 = variables['state00']
state01 = variables['state01']
state10 = variables['state10']
state11 = variables['state11']
seqs = variables['seqs']
depth = variables['depth']
avgs = variables['avgs']
random_gates = variables['random_gates']
I1 = variables['I1']
Q1 = variables['Q1']
I2 = variables['I2']
Q2 = variables['Q2']
state1 = variables['state1']
state2 = variables['state2']

# cross entropy
def cross_entropy(p, q, epsilon=1e-15):
    """
    Calculate cross entropy between two probability distributions.

    Parameters:
    - p: numpy array, the true probability distribution
    - q: numpy array, the predicted probability distribution
    - epsilon: small value to avoid taking the logarithm of zero

    Returns:
    - Cross entropy between p and q
    """
    q = np.maximum(q, epsilon)  # Avoid taking the logarithm of zero
    return -np.sum(p * np.log(q))

# Define the matrices
phix = np.pi/2
X90 = np.array([[np.cos(phix/2), -1J * np.sin(phix/2)], [-1J * np.sin(phix/2), np.cos(phix/2)]])
# print(X90)
phiy = np.pi/2
Y90 = np.array([[np.cos(phix/2), -np.sin(phix/2)], [+np.sin(phix/2), np.cos(phix/2)]])
# print(Y90)

W90 = 1/np.sqrt(3) * (X90 + Y90)
# print(W90)
CZ = np.array([[+1,0,0,0],[0,1,0,0],[0,0,+1,0],[0,0,0,-1]])
# CZ = np.array([[+1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,1]])

# def calculate_determinant(matrix):
#     if len(matrix) != 2 or len(matrix[0]) != 2 or len(matrix[1]) != 2:
#         raise ValueError("Input matrix must be a 2x2 matrix")
    
#     a, b = matrix[0]
#     c, d = matrix[1]
    
#     determinant = (a * d) - (b * c)
#     print(determinant)

# calculate_determinant(X90)
# calculate_determinant(Y90)
# calculate_determinant(W90)

idx=0
expected_mat = []
expected00_mat = []
expected01_mat = []
expected10_mat = []
expected11_mat = []
ce_vec = []
ce_mat = []

for i in range(seqs):
  # print(f"\nseq{i+1}:")
  expected_vec = []
  v00 = []; v01 = []; v10 = []; v11 = []
  ce_vec = []
  for j in range(depth):
    # print(f"depth = {j}")
    k=0
    psi = np.kron([1,0], [1,0])
    while k<j:
      if g1[idx]==0: g1_ = X90 
      elif g1[idx]==1: g1_ = Y90
      elif g1[idx]==2: g1_ = W90
      else: print('ERR')
      if g2[idx]==0: g2_ = X90 
      elif g2[idx]==1: g2_ = Y90
      elif g2[idx]==2: g2_ = W90
      else: print('ERR')
      # op_ = np.kron(g1_, g2_)
      op_ = np.kron(g2_, g1_)
      psi = np.dot(op_, psi)
      op_ = CZ
      psi = np.dot(op_, psi)
      k+=1; idx+=1
    v00.append(np.abs(psi[0])**2)
    v01.append(np.abs(psi[1])**2)
    v10.append(np.abs(psi[2])**2)
    v11.append(np.abs(psi[3])**2)
    incoherent = np.array([0.25, 0.25, 0.25, 0.25])
    expected = np.array([v00[-1], v10[-1], v01[-1], v11[-1]])
    measured = np.array([(state00[i][j])/avgs, (state01[i][j])/avgs, (state10[i][j])/avgs, (state11[i][j])/avgs])

    fxeb = ((cross_entropy(incoherent, expected)-cross_entropy(measured, expected))/
            (cross_entropy(incoherent, expected)-cross_entropy(expected, expected)))
    if isnan(fxeb): print(f"nan found in seq-{i+1}, depth{j+1}: {fxeb}, {cross_entropy(expected, expected)}")
    elif isinf(fxeb): print(f"inf found in seq-{i+1}, depth{j+1}: {fxeb}, {cross_entropy(expected, expected)}")

    ce_vec.append(fxeb)
  expected00_mat.append(v00)
  expected01_mat.append(v01)
  expected10_mat.append(v10)
  expected11_mat.append(v11)
  ce_mat.append(ce_vec)

# Create a pcolor plot
plt.subplot(521)
plt.pcolor(state00/avgs)
plt.clim(vmin=0, vmax=1)
ax = plt.gca()
ax.set_title('<00> Measured')
ax.set_xlabel('Circuit depth')
ax.set_ylabel('Sequences')
ax.set_xticks(np.arange(depth))
plt.colorbar()

# Create a pcolor plot
plt.subplot(523)
plt.pcolor(state01/avgs)
plt.clim(vmin=0, vmax=1)
ax = plt.gca()
ax.set_title('<01> Measured')
ax.set_xlabel('Circuit depth')
ax.set_ylabel('Sequences')
ax.set_xticks(np.arange(depth))
plt.colorbar()

# Create a pcolor plot
plt.subplot(525)
plt.pcolor(state10/avgs)
plt.clim(vmin=0, vmax=1)
ax = plt.gca()
ax.set_title('<10> Measured')
ax.set_xlabel('Circuit depth')
ax.set_ylabel('Sequences')
ax.set_xticks(np.arange(depth))
plt.colorbar()

# Create a pcolor plot
plt.subplot(527)
plt.pcolor(state11/avgs)
plt.clim(vmin=0, vmax=1)
ax = plt.gca()
ax.set_title('<11> Measured')
ax.set_xlabel('Circuit depth')
ax.set_ylabel('Sequences')
ax.set_xticks(np.arange(depth))
plt.colorbar()

# Create a pcolor plot
plt.subplot(522)
plt.pcolor(expected00_mat)
plt.clim(vmin=0, vmax=1)
ax = plt.gca()
ax.set_title('<00> Expected')
ax.set_xlabel('Circuit depth')
ax.set_ylabel('Sequences')
ax.set_xticks(np.arange(depth))
plt.colorbar()

# Create a pcolor plot
plt.subplot(524)
plt.pcolor(expected01_mat)
plt.clim(vmin=0, vmax=1)
ax = plt.gca()
ax.set_title('<01> Expected')
ax.set_xlabel('Circuit depth')
ax.set_ylabel('Sequences')
ax.set_xticks(np.arange(depth))
plt.colorbar()

# Create a pcolor plot
plt.subplot(526)
plt.pcolor(expected10_mat)
plt.clim(vmin=0, vmax=1)
ax = plt.gca()
ax.set_title('<10> Expected')
ax.set_xlabel('Circuit depth')
ax.set_ylabel('Sequences')
ax.set_xticks(np.arange(depth))
plt.colorbar()

# Create a pcolor plot
plt.subplot(528)
plt.pcolor(expected11_mat)
plt.clim(vmin=0, vmax=1)
ax = plt.gca()
ax.set_title('<11> Expected')
ax.set_xlabel('Circuit depth')
ax.set_ylabel('Sequences')
ax.set_xticks(np.arange(depth))
plt.colorbar()

# Create a pcolor plot
plt.subplot(529)
plt.pcolor(ce_mat)
ax = plt.gca()
ax.set_title('cross entropy')
ax.set_xlabel('Circuit depth')
ax.set_ylabel('Sequences')
ax.set_xticks(np.arange(depth))
plt.colorbar()

# Create a 
plt.subplot(5,2,10)
Fxeb = np.mean(ce_mat, axis=0)
print(Fxeb)

def exponential_decay(x, a, b, c):
    return a * np.exp(-b * x) + c

params, covariance = curve_fit(exponential_decay, np.arange(depth), Fxeb)
a_fit, b_fit, c_fit = params

x = exponential_decay(np.arange(depth), a_fit, b_fit, c_fit)

xeb_err_per_cycle = 1 - (x[2]-c_fit)/(x[1]-c_fit)


plt.scatter(np.arange(depth), Fxeb, label='Original Data')
plt.plot(np.arange(depth), exponential_decay(np.arange(depth), a_fit, b_fit, c_fit), label='err_per_cycle={:.2f}'.format(xeb_err_per_cycle), color='red')
plt.legend()
ax = plt.gca()
ax.set_title('XEB')
ax.set_ylabel('fidelity')
ax.set_xticks(np.arange(depth))
plt.show()