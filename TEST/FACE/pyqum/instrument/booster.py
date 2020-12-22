# Aim to accelerate post processing of data
# PENDING: MAKE A CLASS TO ORGANIZE SUBROUTINES

from numba import cuda, float32
import numpy as np
import math
import time
import sys

TPB1=16
TPB2=64

@cuda.jit
def test_mean(a, c, nx, ny):
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
#        c[x]=tmp

#-------------------------------------------------

nx=33
ny=200000
num_stream=1

# create same dat
dat_tmp = np.random.rand(ny)
dat_tmp = np.float32(dat_tmp)

dat = cuda.pinned_array((nx,ny), dtype=np.float32)
for i in range(nx):
    dat[i][:]=dat_tmp[:]


#dat_d=cuda.to_device(dat)
#out_d=cuda.device_array(nx)

segment_size = nx//num_stream
print(segment_size)

stream_list = list()
for sti in range(0, num_stream):
    stream = cuda.stream()
    stream_list.append(stream)

thread=(TPB1,TPB2)
#block_x=int(math.ceil(dat.shape[0]/thread[0]))
#block_y=int(math.ceil(dat.shape[1]/thread[1]))
#block = (block_x,block_y)
block_x=int(math.ceil(segment_size/thread[0]))
block_y=int(math.ceil(ny/thread[1]))
block = (block_x,block_y)

stream_out_d=cuda.device_array(segment_size)
out=np.empty(nx, dtype=np.float32)
#print(block_x, block_y)
#sys.exit()

print("go function")
tStart = time.time()
for sti in range(0, num_stream):
    dat_i_d=cuda.to_device(dat[sti*segment_size:(sti+1)*segment_size][:], stream=stream_list[sti])

    test_mean[block, thread, stream_list[sti]](dat_i_d, stream_out_d, nx, ny)
    out[sti*segment_size:(sti+1)*segment_size]=stream_out_d.copy_to_host(stream=stream_list[sti])
    cuda.synchronize()

print("go output")
#out=out_d.copy_to_host()
tEnd = time.time()
dt=tEnd - tStart
print("dt", dt, "sec")

print(dat)
print(out)
