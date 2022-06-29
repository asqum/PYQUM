from numpy.linalg import inv
from numpy import array, dot

leakage_factor = 3.7

# 1. Use inverse matrix:
Z_match = array([[leakage_factor, -1], [-1, leakage_factor]])
Z1_sole = 0.0475
Z2_sole = -0.037 #-0.035
Z1_apply, Z2_apply = leakage_factor * dot(inv(Z_match), array([Z1_sole, Z2_sole]))
print("Z1_apply: %s\nZ2_apply: %s" %(Z1_apply, Z2_apply))

# 2. Equivalent to the method above: 
# By maintaining one of the Z effectively as its own "sole-value":
Z1_apply = 1 / (1 - 1 / leakage_factor**2) * (Z1_sole + Z2_sole / leakage_factor)
print("By anchoring on Z2_sole at %s, we need Z1_apply = %s" %(Z2_sole, Z1_apply))
Z2_apply = 1 / (1 - 1 / leakage_factor**2) * (Z2_sole + Z1_sole / leakage_factor)
print("By anchoring on Z1_sole at %s, we need Z2_apply = %s" %(Z1_sole, Z2_apply))
