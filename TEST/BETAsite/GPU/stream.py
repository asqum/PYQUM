from numba import cuda, float32
import numpy as np
import math
import time

# leadtek 2020/10/29

# install python library
# install python3
# sudo -H pip3 install numba==0.50.1
# sudo -H pip3 install numpy

#----------------------------------------------------------
# cuda numba function
# TPB1, TPB2 -- parameter of cuda threads

TPB1=1
TPB2=1024

# Average against y
@cuda.jit
def dat_mean(a, c, nx, ny):
    x, y = cuda.grid(2)
    sa=cuda.shared.array(shape=(TPB1,TPB2), dtype=float32)

    tx=cuda.threadIdx.x
    ty=cuda.threadIdx.y

#    if x >= a.shape[0] or y >= a.shape[1]:
    if x < nx and y < ny:

        tmp=0.
        num=0
        for i in range(int(ny/TPB2)):
            sa[tx,ty]=a[x,ty+i*TPB2]
            cuda.syncthreads()

            for j in range(TPB2):
                tmp += sa[tx,j]
                num += 1
            cuda.syncthreads()

        c[x]=tmp/float(num)

#----------------------------------------------------------
# matrix = nx*ny
# nx -- amount of data
# ny -- array
# num_stream -- cuda stream amount

nx=1000 #40000
ny=20000
num_stream=10 #500

#----------------------------------------------------------
# create same dat
print("---- create sample input data ----")
dat_tmp = np.random.rand(ny)
dat_tmp = np.float32(dat_tmp)

# create pinned array for cuda
dat = cuda.pinned_array((nx,ny), dtype=np.float32)
# copy sample data
for i in range(nx):
    dat[i][:]=dat_tmp[:]

#----------------------------------------------------------
# process nx data_block(20000), divided into num_stream stream processes
segment_size = nx//num_stream
print(nx, "data block -->", num_stream, " stream")
print()

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
print("---- go output ----")
#out=out_d.copy_to_host()
print("all time", sti, "-- dt", total_dt, "sec")

print("-- input data of shape %s --" %str(dat.shape))
print(dat)
print("-- output data of shape %s --" %(out.shape))
print(out)
print("---- finish ----")
