These files are intended to be used as demos.  
The learning objective is to show how the Quantum Control System (QCS) 
can be used to run real experiments on superconducting qubits.  
Each demo can be run by itself, 
but taken together they are designed to demonstrate a part of the customer workflow 
to characterize a new qubit chip.  
For this, the correct order to run the demos is:


1. Spectroscopy (find qubit frequencies)
2. Rabi (calibrate pi-pulse for the qubits)
3. Energy Relazation (find T1 time for qubits)
4. Ramsey and Spin Echo (find T2* and T2E times for qubits)

Module Configuration
    Verify that the configuration matches with two_qubit_system.yaml
        Slot 2 - M5201A downconverter
        Slot 3 - M5200A digitizer
        Slot 4 - M5300A AWG
        Slot 6 - M5300A AWG

Connections
    Connect the readout_signal AnalogChannel (awg1 channel 4) 
         to the readout_signal AcquisitionChannel on the downconverter (downconverter, channel 4)

    Connect the readout_signal downconverter to the digitizer
        (downconverter channel 4) to (digitizer channel 4)
    Connect qubit 1 AnalogChannel xy (awg1 channel 1)
         to the control_signal acquisition_channel 

Note, this bypasses the downconverter
        (awg1 channel 1) to (digitizer channel 1)