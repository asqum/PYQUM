# Alazar Digitizer (ATS9371)
from __future__ import division
import ctypes
import numpy as np
import os
import signal
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../..', 'Library'))
import atsapi as ats

samplesPerSec = None

# Configures a board for acquisition
def ConfigureBoard(board):
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
    global samplesPerSec
    samplesPerSec = 1000000000.0
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
                              150,
                              ats.TRIG_ENGINE_K,
                              ats.TRIG_DISABLE,
                              ats.TRIGGER_SLOPE_POSITIVE,
                              128)

    # TODO: Select external trigger parameters as required.
    board.setExternalTrigger(ats.DC_COUPLING,
                             ats.ETR_TTL)

    # TODO: Set trigger delay as required.
    triggerDelay_sec = 0
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
    

def AcquireData(board):
    # TODO: Select the total acquisition length in seconds
    acquisitionLength_sec = 1 #1

    # TODO: Select the number of samples in each DMA buffer
    samplesPerBuffer = 1024000 #1024000
    
    # TODO: Select the active channels.
    channels = ats.CHANNEL_A
    channelCount = 0
    for c in ats.channels:
        channelCount += (c & channels == c)

    # TODO: Should data be saved to file?
    saveData = False
    dataFile = None
    if saveData:
        dataFile = open(os.path.join(os.path.dirname(__file__),
                                     "data.bin"), 'wb')

    # Compute the number of bytes per record and per buffer
    memorySize_samples, bitsPerSample = board.getChannelInfo()
    print("Memory size: %s samples" %memorySize_samples)
    bytesPerSample = (bitsPerSample.value + 7) // 8
    bytesPerBuffer = bytesPerSample * samplesPerBuffer * channelCount
    # Calculate the number of buffers in the acquisition
    samplesPerAcquisition = int(samplesPerSec * acquisitionLength_sec + 0.5)
    buffersPerAcquisition = ((samplesPerAcquisition + samplesPerBuffer - 1) //
                             samplesPerBuffer)

    # TODO: Select number of DMA buffers to allocate
    bufferCount = 4

    # Allocate DMA buffers

    sample_type = ctypes.c_uint8
    if bytesPerSample > 1:
        sample_type = ctypes.c_uint16

    buffers = []
    for i in range(bufferCount):
        buffers.append(ats.DMABuffer(board.handle, sample_type, bytesPerBuffer))
    
    board.beforeAsyncRead(channels,
                          0,                 # Must be 0
                          samplesPerBuffer,
                          1,                 # Must be 1
                          0x7FFFFFFF,        # Ignored
                          ats.ADMA_EXTERNAL_STARTCAPTURE | ats.ADMA_CONTINUOUS_MODE | ats.ADMA_FIFO_ONLY_STREAMING)
    


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
        while (buffersCompleted < buffersPerAcquisition and not
               ats.enter_pressed()):
            # Wait for the buffer at the head of the list of available
            # buffers to be filled by the board.
            buffer = buffers[buffersCompleted % len(buffers)]
            board.waitAsyncBufferComplete(buffer.addr, timeout_ms=5000)
            buffersCompleted += 1
            bytesTransferred += buffer.size_bytes

            # TODO: Process sample data in this buffer. Data is available
            # as a NumPy array at buffer.buffer

            # NOTE:
            #
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
            # Optionaly save data to file
            if dataFile:
                buffer.buffer.tofile(dataFile)

            # Add the buffer to the end of the list of available buffers.
            board.postAsyncBuffer(buffer.addr, buffer.size_bytes)
    finally:
        board.abortAsyncRead()
    # Compute the total transfer time, and display performance information.
    transferTime_sec = time.time() - start
    print("Capture completed in %f sec" % transferTime_sec)
    buffersPerSec = 0
    bytesPerSec = 0
    if transferTime_sec > 0:
        buffersPerSec = buffersCompleted / transferTime_sec
        bytesPerSec = bytesTransferred / transferTime_sec
    print("Captured %d buffers (%f buffers per sec)" %
          (buffersCompleted, buffersPerSec))
    print("Transferred %d bytes (%f bytes per sec)" %
          (bytesTransferred, bytesPerSec))

if __name__ == "__main__":
    board = ats.Board(systemId = 1, boardId = 1)
    ConfigureBoard(board)
    AcquireData(board)