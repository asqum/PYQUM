'''
Adopted from leadtek 2020/10/29
'''

from numba import cuda, float32
import numpy as np
import math
import time

#----------------------------------------------------------
# cuda numba function
# parameter of cuda threads
TPB1, TPB2 = 2, 512 # 1, 1024

# Average against y
@cuda.jit
def dat_mean(arr, cout, nx, ny):
    # Allocating grids:
    x, y = cuda.grid(2)
    sa = cuda.shared.array(shape=(TPB1,TPB2), dtype=float32)
    tx, ty = cuda.threadIdx.x, cuda.threadIdx.y # Thread block dimension

    if x < nx and y < ny:

        tmp, num = 0., 0
        block_count = int(ny/TPB2)
        for i in range(block_count):
            sa[tx,ty]=arr[x,ty+i*TPB2]
            cuda.syncthreads()

            parallel_block_sweep = TPB2
            # if ny%TPB2 and i==block_count-1: parallel_block_sweep = ny%TPB2 # cuda seems to stick strongly to block size
            for j in range(parallel_block_sweep):
                # tmp += math.sin(sa[tx,j])
                tmp += sa[tx,j]
                num += 1
                
            cuda.syncthreads()
        cout[x]=float(tmp)/int(num)

def cuda_streamean(dat_tmp, num_stream=1):
    #----------------------------------------------------------
    nx = np.array(dat_tmp).shape[0] # 40000 # x-axis dimension
    ny = np.array(dat_tmp).shape[1] // TPB2 * TPB2 # 20000 # y-axis dimension (force into multiples of TPB2)
    # num_stream=1 #500 # cuda stream amount

    #----------------------------------------------------------
    # create same dat
    print("---- create sample input data ----")
    
    # create pinned array for cuda
    dat = cuda.pinned_array((nx,ny), dtype=np.float32)
    # copy sample data
    # for i in range(nx): dat[i][:]=dat_tmp[:]
    dat = dat_tmp

    #----------------------------------------------------------
    # process nx data_block(20000), divided into num_stream stream processes
    segment_size = nx//num_stream
    print(nx, "data block -->", num_stream, " stream")

    # cuda setting
    thread=(TPB1,TPB2)
    block_x=int(math.ceil(segment_size/thread[0]))
    block_y=int(math.ceil(ny/thread[1]))
    block = (block_x,block_y)

    # stream outout array
    stream_out_d=cuda.device_array(segment_size)
    # output array
    out=np.empty(nx, dtype=np.float32)

    #----------------------------------------------------------
    print("---- go data mean function ----")

    # total_dt -- total spend time
    # dt -- spend time per stream
    # sti -- stream

    total_dt=0.
    for sti in range(0, num_stream):

        tStart = time.time()

        stream = cuda.stream()
        with stream.auto_synchronize():
            dat_i_d=cuda.to_device(dat[sti*segment_size:(sti+1)*segment_size][:], stream=stream)

            dat_mean[block, thread, stream](dat_i_d, stream_out_d, nx, ny)
            out[sti*segment_size:(sti+1)*segment_size]=stream_out_d.copy_to_host(stream=stream)

        tEnd = time.time()
        dt=tEnd - tStart
        total_dt += dt
        print("stream", sti, "-- dt", dt, "sec")

    #----------------------------------------------------------
    print("all time", sti, "-- dt", total_dt, "sec")

    return out


def test():
    nx, ny = 10, 200000
    dat_tmp = np.ones([nx, 1])*np.float32(np.linspace(1, ny, ny)) # np.random.rand(ny)
    # dat_tmp = np.ones([1, 1])*np.float32(np.linspace(1, ny, ny)) # np.random.rand(ny)
    out = cuda_streamean(dat_tmp)

    print("testing consistency:")
    print(">> input data of shape: %s" %str(dat_tmp.shape))
    print(dat_tmp)
    print(">> output data of shape: %s" %(out.shape))
    print(out)

test()

