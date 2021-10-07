from numpy.linalg import inv
from numpy import array, dot

leakage_factor = 3
Z_match = array([[leakage_factor, -1], [-1, leakage_factor]])
Z1_sole = 0.0024
Z2_sole = 0.0415
Z1_apply, Z2_apply = leakage_factor * dot(inv(Z_match), array([Z1_sole, Z2_sole]))
print("Z1_apply: %s\nZ2_apply: %s" %(Z1_apply, Z2_apply))
