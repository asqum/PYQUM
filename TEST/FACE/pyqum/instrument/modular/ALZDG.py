# Alazar Digitizer (ATS9371)
from __future__ import division
import ctypes
from numpy import array, zeros, ceil, empty
import os
import signal
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'Library'))
import atsapi as ats

from pyqum.instrument.analyzer import curve

def Initiate():
    board = ats.Board(systemId = 1, boardId = 1)
    return board

# NPT: Multiple Records without Pre-Trigger Samples:
# Configures a board for acquisition
def ConfigureBoard_NPT(board, samplesPerSec=1000000000.0, 
                        triggerDelay_sec = 888*1e-9):
    # CLOCK:
    # Configure clock parameters as required to generate this sample rate
    board.setCaptureClock(ats.EXTERNAL_CLOCK_10MHz_REF, #ats.INTERNAL_CLOCK,
                          samplesPerSec, #ats.SAMPLE_RATE_1000MSPS,
                          ats.CLOCK_EDGE_RISING,
                          0)
    # CHANNELS:
    # Configure channel A input parameters as required.
    board.inputControlEx(ats.CHANNEL_A, ats.DC_COUPLING, ats.INPUT_RANGE_PM_400_MV, ats.IMPEDANCE_50_OHM)
    # Configure channel B input parameters as required.
    board.inputControlEx(ats.CHANNEL_B, ats.DC_COUPLING, ats.INPUT_RANGE_PM_400_MV, ats.IMPEDANCE_50_OHM)
    # TRIGGER:
    # Configure trigger inputs and levels as required.
    board.setTriggerOperation(ats.TRIG_ENGINE_OP_J,
                              ats.TRIG_ENGINE_J,
                              ats.TRIG_EXTERNAL, #ats.TRIG_CHAN_A,
                              ats.TRIGGER_SLOPE_POSITIVE,
                              0,
                              ats.TRIG_ENGINE_K,
                              ats.TRIG_DISABLE,
                              ats.TRIGGER_SLOPE_POSITIVE,
                              0)
    # Configure external trigger parameters as required.
    board.setExternalTrigger(ats.DC_COUPLING, ats.ETR_TTL)
    # Set trigger delay as required.
    board.setTriggerDelay(int(triggerDelay_sec * samplesPerSec + 0.5))
    # Set trigger timeout as required.
    '''
    The board will wait for a for this amount of time for a
    trigger event.  If a trigger event does not arrive, then the
    board will automatically trigger. Set the trigger timeout value
    to 0 to force the board to wait forever for a trigger event.
    
    IMPORTANT: The trigger timeout value should be set to zero after
    appropriate trigger parameters have been determined, otherwise
    the board may trigger if the timeout interval expires before a
    hardware trigger event arrives.
    '''
    board.setTriggerTimeOut(0)
    # Configure AUX I/O connector as required
    board.configureAuxIO(ats.AUX_OUT_TRIGGER, 0)
    
    dt = 1 / samplesPerSec # in sec
    return dt
    

def AcquireData_NPT(board, dt, recordtime, recordsum, OPT_DMA_Buffer_Size=16):
    '''
    board: given by {Initiate}
    dt: given by {ConfigureBoard}
    recordtime (s): The duration of pulse response of interest
    recordsum: Total sum of records to be acquired for fedility test or fast averaging
    OPT_DMA_Buffer_Size (MB): Optimal Buffer size for DMA transfer between CPU and the board PER Channel
    '''
    # CONSTANTS:
    preTriggerSamples = 0 # No pre-trigger samples in NPT mode
    dRange = 0.4 # Dynamic Range of Digitizer (400mV)
    boardmemory_samples, bitsPerSample = board.getChannelInfo() # Get board's spec of memory and sample size 
    # A 12-bit sample code is stored in the most significant bits of each 16-bit sample value.
    codeRange = 2 ** (float(bitsPerSample.value) - 1) - 0.5 # Digital range in binary
    rangeconv = dRange/codeRange/16. # range and zero for each channel, combined with bit shifting
    codeZero = 2 ** (float(bitsPerSample.value) - 1) - 0.5
    offset = 16.*codeZero # Digital offset in binary
    MEM_SIZE = int(128 * 1024*1024*1024) # RAM MEMORY SIZE (<160GB)
    bytesPerBuffer_MAX = min(OPT_DMA_Buffer_Size *1024*1024, boardmemory_samples.value/2) # 16MB / channel # Note: DMA buffer is limited by ~20% of Total On-Board 8G memory, and yet the best performance lies between 16-32MB!

    # CHANNELS:
    # Configure the active channels.
    channels = ats.CHANNEL_A | ats.CHANNEL_B
    channelCount = 0
    for c in ats.channels: channelCount += (c & channels == c)
    # print("Channel count: %s" %channelCount)

    # SAMPLES:
    # Configure the number of samples/bytes per record.
    postTriggerSamples = recordtime / dt
    postTriggerSamples = int(ceil(postTriggerSamples / 128.)*128) # force it into multiples of 128
    bytesPerSample = (bitsPerSample.value + 7) // 8
    samplesPerRecord = preTriggerSamples + postTriggerSamples
    bytesPerRecord = bytesPerSample * samplesPerRecord
    # Optimize records/buffer:
    recordsPerBuffer_MAX = bytesPerBuffer_MAX // bytesPerRecord 
    recordsPerBuffer = min(recordsum, recordsPerBuffer_MAX) # the number of records per DMA buffer. 
    recordsPerBuffer = int(4096 * ceil(bytesPerRecord*recordsPerBuffer/4096.)) // bytesPerRecord # force buffer byte-size to be integer of 256 * 16 = 4096, due to 32-bit architecture?
    # Optimize buffer/acquisition:
    maxBufferCount = 2*(int(MEM_SIZE//(2*(bytesPerRecord*recordsPerBuffer)))) # force buffer count to be EVEN number, seems faster for allocating
    buffersPerAcquisition = min(recordsum // recordsPerBuffer, maxBufferCount)
    # Configure number of DMA buffers to allocate
    bufferCount = min(maxBufferCount, buffersPerAcquisition, 1024) # limit rotating buffer to 1024

    # DATA:
    # Allocate DMA buffers
    bytesPerBuffer = bytesPerRecord * recordsPerBuffer * channelCount
    # print("Buffer size: %sMB" %(bytesPerBuffer/1e6))

    if bytesPerSample > 1: sample_type = ctypes.c_uint16
    else: sample_type = ctypes.c_uint8

    buffers = empty(bufferCount, dtype=object)
    for i in range(bufferCount):
        buffers[i] = ats.DMABuffer(board.handle, sample_type, bytesPerBuffer)
    
    # Tell the board about the record size
    board.setRecordSize(preTriggerSamples, postTriggerSamples)
    
    # Configure the board to make an NPT AutoDMA acquisition
    recordsPerAcquisition = recordsPerBuffer * buffersPerAcquisition
    board.beforeAsyncRead(channels, -preTriggerSamples, samplesPerRecord, recordsPerBuffer, recordsPerAcquisition,
                        #   ats.ADMA_EXTERNAL_STARTCAPTURE | ats.ADMA_NPT | ats.ADMA_FIFO_ONLY_STREAMING)
                          ats.ADMA_EXTERNAL_STARTCAPTURE | ats.ADMA_NPT)

    # Post DMA buffers to board
    print("Allocating %sMB for every buffer" %(buffers[0].size_bytes/1024/1024))
    for buffer in buffers:
        board.postAsyncBuffer(buffer.addr, buffer.size_bytes)

    start = time.time() # Keep track of when acquisition started
    try:
        # Start Dual-port autoDMA capture:
        board.startCapture()
        print("Capturing %d buffers. Press <enter> to abort" %buffersPerAcquisition)
        buffersCompleted = 0
        bytesTransferred = 0
        
        # NOTE:
        # While you are processing this buffer, the board is already
        # filling the next available buffer(s).
        #
        # You MUST finish processing this buffer and post it back to the
        # board before the board fills all of its available DMA buffers
        # and on-board memory.
        #
        # Samples are arranged in the buffer as follows: S0A, S0B, ..., S1A, S1B, ... with SXY the sample number X of channel Y.
        # Preparing data basket:
        data_V = zeros([recordsPerBuffer*buffersPerAcquisition, postTriggerSamples, channelCount])

        # Collecting buffers:
        while (buffersCompleted < buffersPerAcquisition and not ats.enter_pressed()):
            buffer = buffers[buffersCompleted % len(buffers)] # rotating buffers to be filled by the board.
            # print("Current buffer #%s: %s" %(buffersCompleted % len(buffers), buffer.buffer[:8]))
            board.waitAsyncBufferComplete(buffer.addr, timeout_ms=100000) # transfer ats-DMA buffer to CPU buffer (RAM)
            buffersCompleted += 1
            bytesTransferred += buffer.size_bytes

            # TODO: Process sample data in this buffer. Data is available
            # as a NumPy array at buffer.buffer
            data_binary = buffer.buffer.reshape(recordsPerBuffer, postTriggerSamples, channelCount)
            data_binary = rangeconv * (data_binary - offset)
            # print("Buffer of shape %s: %s" %(data_binary.shape, data_binary))
            data_V[(buffersCompleted - 1) * recordsPerBuffer :  (buffersCompleted) * recordsPerBuffer, :, :] = data_binary
            # print("Data of shape %s: %s" %(data_V.shape, data_V))

            # Add the buffer to the end of the list of available buffers.
            board.postAsyncBuffer(buffer.addr, buffer.size_bytes)
    finally:
        board.abortAsyncRead()
    # Compute the total transfer time, and display performance information.
    transferTime_sec = time.time() - start
    print("Capture completed in %f sec" % transferTime_sec)
    buffersPerSec = 0
    bytesPerSec = 0
    recordsPerSec = 0
    if transferTime_sec > 0:
        buffersPerSec = buffersCompleted / transferTime_sec
        bytesPerSec = bytesTransferred / transferTime_sec
        recordsPerSec = recordsPerBuffer * buffersCompleted / transferTime_sec
    # print("Captured %d buffers (%f buffers per sec)" %(buffersCompleted, buffersPerSec))
    # print("Captured %d records (%f records per sec)" %(recordsPerBuffer * buffersCompleted, recordsPerSec))
    # print("Transferred %d bytes (%f bytes per sec)" %(bytesTransferred, bytesPerSec))

    return data_V, transferTime_sec, recordsPerBuffer, buffersPerAcquisition


def test():
    board = Initiate()
    dt = ConfigureBoard_NPT(board)
    
    N = 8
    for i in range(N):
        DMA_transfer_size = 2**(N-i)
        print("\nMaximum DMA Buffer PER Channel: %sMB" %DMA_transfer_size)
        ACQ = AcquireData_NPT(board, dt, 1e-6, 1024000, DMA_transfer_size)

    DATA = ACQ[0] 
    recordsPerBuffer = ACQ[2]
    buffersPerAcquisition = ACQ[3]
    middlerec = recordsPerBuffer*buffersPerAcquisition//2
    Ch = 1
    y1, y2, y3 = DATA[middlerec,:,Ch-1], DATA[middlerec+recordsPerBuffer,:,Ch-1], DATA[middlerec+2*recordsPerBuffer,:,Ch-1]
    # print("DATA: %s" %DATA)
    curve([dt*array(range(len(y1))),dt*array(range(len(y2))), dt*array(range(len(y3)))], [y1, y2, y3], "ATS-9371 NPT Multi-Records", "t(s)", "Signal(V)", style=["-k","-b","-r"])
    y1, y2 = DATA[1,:,0], DATA[1,:,1]
    curve([dt*array(range(len(y1)))]*2, [y1,y2], "ATS-9371 NPT 1/N Records", "t(s)", "Signal(V)")


