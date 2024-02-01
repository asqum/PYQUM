import numpy as np
import matplotlib.pyplot as plt
tomo_raw_data = np.load(r'testing/5Q_GHZ_5_4_3.npz', allow_pickle=True)# ["arr_0"].item()
# tomo_data =
for k, v in tomo_raw_data.items():
    print(k, v.shape)
# threshold = [2.007e-04, -5.748e-06, 1.421e-04]
threshold = [-5.748e-06, 2.007e-04, 1.421e-04]

q_names = ["rr5","rr4","rr3"]
q_order = [5,4,3]


tomo_data = {}

for q_o, q_name in zip(q_order, q_names):
    print(q_o, q_name, tomo_raw_data[q_name].shape)
    tomo_data[q_name] = np.moveaxis(tomo_raw_data[q_name],1,-1)[q_o*2-2:q_o*2]


bit_string = np.zeros(tomo_data[q_names[0]].shape[1:],dtype=int)

total_count = tomo_data[q_names[0]].shape[-1]
# plt.plot( r1_data[0][0][0],r1_data[1][0][0],'o')
# plt.show()
# plt.plot( r2_data[2][0][0],r2_data[3][0][0],'o')
# plt.show()

print( bit_string.shape )
for q_i, label in enumerate(q_names):
    q_address = len(q_names)-q_i-1
    print( label, 2**q_address, tomo_data[label].shape, threshold[q_address] )
    # ar_data = np.moveaxis(tomo_data[label],1,-1)
    bit_string += (tomo_data[label][0] > threshold[q_i]).astype(int)*(2**q_address)
    print(bit_string.shape)

probability_tomo = np.zeros(tomo_data[q_names[0]].shape[1:-1]+(2**len(q_names),))
print(probability_tomo.shape)
for i in range(3):
    ii = i-1
    if ii<0:
        ii=2
    for j in range(3):
        jj = j-1
        if jj<0:
            jj=2
        for k in range(3):
            kk = k-1
            if kk<0:
                kk=2
        # count_arr = np.unique(bit_string[i][j],return_counts=True)
            count_arr = np.bincount(bit_string[i][j][k])
            # print(count_arr, total_count, np.sum(count_arr))
            probability_tomo[ii][jj][kk] = count_arr/float(total_count)
print(probability_tomo.shape)


from scipy.io import savemat
savemat('3Q_tomo.mat',{"data":probability_tomo})


# print(type(DM_gg_view.A))
from qutip.visualization import matrix_histogram_complex
matrix_histogram_complex( probability_tomo )
# # fig, ax = plt.subplots(2,1)
# # # ax[0].imshow(reDM_gg_view)
# # # ax[1].imshow(imDM_gg_view)
# # c = ax[0].pcolormesh(reDM_gg_view, cmap='RdBu', vmin=-1, vmax=1)
# # ax[0].set_title('Re')
# # fig.colorbar(c, ax=ax[0])
# # c = ax[1].pcolormesh(imDM_gg_view, cmap='RdBu', vmin=-1, vmax=1)
# # ax[1].set_title('Im')
# # fig.colorbar(c, ax=ax[1])
# # fig.show()
# plt.show()