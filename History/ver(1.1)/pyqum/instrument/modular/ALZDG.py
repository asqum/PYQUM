# Alazar Digitizer (ATS9371)
from __future__ import division
import ctypes
from numpy import array, zeros
import os
import signal
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'Library'))
import atsapi as ats

from pyqum.instrument.analyzer import curve

dRange = 0.4 # Dynamic Range of Digitizer (400mV)

# NPT: Multiple Records without Pre-Trigger Samples:
# Configures a board for acquisition
def ConfigureBoard_NPT(board, samplesPerSec=1000000000.0):
    # TODO: Select clock parameters as required to generate this
    # sample rate
    #
    # For example: if samplesPerSec is 100e6 (100 MS/s), then you can
    # either:
    #  - select clock source INTERNAL_CLOCK and sample rate
    #    SAMPLE_RATE_100MSPS
    #  - or select clock source FAST_EXTERNAL_CLOCK, sample rate
    #    SAMPLE_RATE_USER_DEF, and connect a 100MHz signal to the
    #    EXT CLK BNC connector
    
    board.setCaptureClock(ats.EXTERNAL_CLOCK_10MHz_REF, #ats.INTERNAL_CLOCK,
                          samplesPerSec, #ats.SAMPLE_RATE_1000MSPS,
                          ats.CLOCK_EDGE_RISING,
                          0)
    
    # TODO: Select channel A input parameters as required.
    board.inputControlEx(ats.CHANNEL_A,
                         ats.DC_COUPLING,
                         ats.INPUT_RANGE_PM_400_MV,
                         ats.IMPEDANCE_50_OHM)
    
    
    # TODO: Select channel B input parameters as required.
    board.inputControlEx(ats.CHANNEL_B,
                         ats.DC_COUPLING,
                         ats.INPUT_RANGE_PM_400_MV,
                         ats.IMPEDANCE_50_OHM)
    
    # TODO: Select trigger inputs and levels as required.
    board.setTriggerOperation(ats.TRIG_ENGINE_OP_J,
                              ats.TRIG_ENGINE_J,
                              ats.TRIG_EXTERNAL, #ats.TRIG_CHAN_A,
                              ats.TRIGGER_SLOPE_POSITIVE,
                              0,
                              ats.TRIG_ENGINE_K,
                              ats.TRIG_DISABLE,
                              ats.TRIGGER_SLOPE_POSITIVE,
                              0)

    # TODO: Select external trigger parameters as required.
    board.setExternalTrigger(ats.DC_COUPLING,
                             ats.ETR_TTL)

    # TODO: Set trigger delay as required.
    triggerDelay_sec = 888*1e-9
    triggerDelay_samples = int(triggerDelay_sec * samplesPerSec + 0.5)
    board.setTriggerDelay(triggerDelay_samples)

    # TODO: Set trigger timeout as required.
    #
    # NOTE: The board will wait for a for this amount of time for a
    # trigger event.  If a trigger event does not arrive, then the
    # board will automatically trigger. Set the trigger timeout value
    # to 0 to force the board to wait forever for a trigger event.
    #
    # IMPORTANT: The trigger timeout value should be set to zero after
    # appropriate trigger parameters have been determined, otherwise
    # the board may trigger if the timeout interval expires before a
    # hardware trigger event arrives.
    board.setTriggerTimeOut(0)

    # Configure AUX I/O connector as required
    board.configureAuxIO(ats.AUX_OUT_TRIGGER,
                         0)
    dt = 1 / samplesPerSec
    return dt
    

def AcquireData_NPT(board):
    # No pre-trigger samples in NPT mode
    preTriggerSamples = 0

    # TODO: Select the number of samples per record.
    postTriggerSamples = 512 #2048

    # TODO: Select the number of records per DMA buffer.
    recordsPerBuffer = 100 #10 ##samples*records is limited by ~20% of Total On-Board 8G memory, and yet the best performance lies between 16-32MB!

    # TODO: Select the number of buffers per acquisition.
    buffersPerAcquisition = 128 #10
    
    # TODO: Select the active channels.
    channels = ats.CHANNEL_A | ats.CHANNEL_B
    channelCount = 0
    for c in ats.channels:
        channelCount += (c & channels == c)

    print("Channel count: %s" %channelCount)

    # TODO: Should data be saved to file?
    saveData = False
    dataFile = None
    if saveData:
        dataFile = open(os.path.join(os.path.dirname(__file__),
                                     "data.bin"), 'wb')

    # Compute the number of bytes per record and per buffer
    memorySize_samples, bitsPerSample = board.getChannelInfo()
    print("Memory size (On-Board 8G): %s samples \nBits per sample: %s" %(memorySize_samples.value, bitsPerSample.value))
    bytesPerSample = (bitsPerSample.value + 7) // 8
    samplesPerRecord = preTriggerSamples + postTriggerSamples
    bytesPerRecord = bytesPerSample * samplesPerRecord
    bytesPerBuffer = bytesPerRecord * recordsPerBuffer * channelCount

    # TODO: Select number of DMA buffers to allocate
    bufferCount = 64 # 4

    # Allocate DMA buffers

    sample_type = ctypes.c_uint8
    if bytesPerSample > 1:
        sample_type = ctypes.c_uint16

    buffers = []
    for i in range(bufferCount):
        buffers.append(ats.DMABuffer(board.handle, sample_type, bytesPerBuffer))
    
    # Set the record size
    board.setRecordSize(preTriggerSamples, postTriggerSamples)

    recordsPerAcquisition = recordsPerBuffer * buffersPerAcquisition

    # Configure the board to make an NPT AutoDMA acquisition
    board.beforeAsyncRead(channels,
                          -preTriggerSamples,
                          samplesPerRecord,
                          recordsPerBuffer,
                          recordsPerAcquisition,
                        #   ats.ADMA_EXTERNAL_STARTCAPTURE | ats.ADMA_NPT | ats.ADMA_FIFO_ONLY_STREAMING)
                          ats.ADMA_EXTERNAL_STARTCAPTURE | ats.ADMA_NPT)
    


    # Post DMA buffers to board
    for buffer in buffers:
        board.postAsyncBuffer(buffer.addr, buffer.size_bytes)

    start = time.time() # Keep track of when acquisition started
    try:
        board.startCapture() # Start the acquisition
        print("Capturing %d buffers. Press <enter> to abort" %
              buffersPerAcquisition)
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
        # Samples are arranged in the buffer as follows:
        # S0A, S0B, ..., S1A, S1B, ...
        # with SXY the sample number X of channel Y.
        #
        # A 12-bit sample code is stored in the most significant bits of
        # each 16-bit sample value.
        #
        # Sample codes are unsigned by default. As a result:
        # - 0x0000 represents a negative full scale input signal.
        # - 0x8000 represents a ~0V signal.
        # - 0xFFFF represents a positive full scale input signal.

        # Digital range in binary
        codeRange = 2 ** (float(bitsPerSample.value) - 1) - 0.5
        rangeconv = dRange/codeRange/16. # range and zero for each channel, combined with bit shifting
        # Digital offset in binary
        codeZero = 2 ** (float(bitsPerSample.value) - 1) - 0.5
        offset = 16.*codeZero

        # Preparing data basket:
        data_V = zeros([recordsPerBuffer*buffersPerAcquisition, postTriggerSamples, channelCount])

        # Collecting buffers:
        while (buffersCompleted < buffersPerAcquisition and not
               ats.enter_pressed()):
            # Wait for the buffer at the head of the list of available
            # buffers to be filled by the board.
            buffer = buffers[buffersCompleted % len(buffers)]
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
    print("Captured %d buffers (%f buffers per sec)" %
          (buffersCompleted, buffersPerSec))
    print("Captured %d records (%f records per sec)" %
          (recordsPerBuffer * buffersCompleted, recordsPerSec))
    print("Transferred %d bytes (%f bytes per sec)" %
          (bytesTransferred, bytesPerSec))

    return data_V


def test():
    board = ats.Board(systemId = 1, boardId = 1)
    dt = ConfigureBoard_NPT(board)
    DATA = AcquireData_NPT(board)
    Ch = 1
    y1, y2, y3 = DATA[7777,:,Ch-1], DATA[7877,:,Ch-1], DATA[7977,:,Ch-1]
    print("DATA: %s" %DATA)
    curve([dt*array(range(len(y1))),dt*array(range(len(y2))), dt*array(range(len(y3)))], [y1, y2, y3], "ATS-9371 NPT Multi-Records", "t(s)", "Signal(V)", style=["-k","-b","-r"])
    y1, y2 = DATA[1,:,0], DATA[1,:,1]
    curve([dt*array(range(len(y1)))]*2, [y1,y2], "ATS-9371 NPT 1/N Records", "t(s)", "Signal(V)")


