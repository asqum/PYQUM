import numpy as np


file_path = r"C:\Users\ASQUM_2\Documents\GitHub\PYQUM\TEST\BETAsite\QM\OPXPlus\data"
file_name = "IQ_Blobs_q1_2_3_4_5"
data = np.load(file_path+"\\"+file_name+".npz", allow_pickle=True)

for k, v in data.items():
    print(k, v.shape)

# for k, v in data["arr_0"].item():
#     print(k, v.shape)