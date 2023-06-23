####################
# QUA START        #
####################

from qm.qua import *
from configuration import *
from qualang_tools.loops import from_array
from pyqum.instrument.toolbox import waveform

code = '''

# constant / from config:
n_avg = 4000000
t = 17000//4 #//100
fres_q1 = qubit_IF_q1
fres_q2 = qubit_IF_q2

# variables
dfq1 = np.linspace( -100e6, 490e6, 100, dtype=int) # qubit 1
dcq1 = np.linspace(-0.49, 0.49, 120) # flux 1
dfq2 = np.linspace(- 120e6, 160e6, 100, dtype=int) # qubit 2
dcq2 = np.linspace(-0.49, 0.49, 120) # flux 2 

# Equalization for comparison: fixed on f_q1
fres_q2 = fres_q1
dfq2 = dfq1

# QUA program
with program() as qua_program:
    
    I = [declare(fixed) for i in range(2)]
    Q = [declare(fixed) for i in range(2)] 
    I_st = [declare_stream() for i in range(2)]
    Q_st = [declare_stream() for i in range(2)]
    n = declare(int)
    n_st = declare_stream()
    df_q1 = declare(int)
    df_q2 = declare(int)
    dc_q1 = declare(fixed)
    dc_q2 = declare(fixed)

    with for_(n, 0, n < n_avg, n+1):
        
        save(n, n_st)
       
        with for_each_((df_q1,df_q2), (dfq1,dfq2)):

            update_frequency("q1_xy", df_q1 + fres_q1)
            update_frequency("q2_xy", df_q2 + fres_q2) 
            
            with for_(*from_array(dc_q2, dcq2)):

                # Flux sweeping 
                set_dc_offset("q1_z", "single", dc_q2)
                set_dc_offset("q2_z", "single", 0.173)
                set_dc_offset("qc_z", "single", -0.117)
                
                # Saturate qubit
                play("cw"*amp(0.07), "q1_xy", duration=t)
                play("cw"*amp(0.3), "q2_xy", duration=t)

                # align()
                
                # readout
                measure("readout"*amp(0.9), "rr1", None, dual_demod.full("cos", "out1", "minus_sin", "out2", I[0]),
                dual_demod.full("sin", "out1", "cos", "out2", Q[0]))
                measure("readout"*amp(0.9), "rr2", None, dual_demod.full("cos", "out1", "sin", "out2", I[1]),
                dual_demod.full("minus_sin", "out1", "cos", "out2", Q[1]))
                save(I[0], I_st[0])
                save(Q[0], Q_st[0])
                save(I[1], I_st[1])
                save(Q[1], Q_st[1])
                
                # DC waiting time will affect the edges of the curve:
                wait(1000)

    with stream_processing():

        n_st.save("n")

        # resonator 1
        I_st[0].buffer(len(dfq1), len(dcq1)).average().save("I1")
        Q_st[0].buffer(len(dfq1), len(dcq1)).average().save("Q1")
        
        # resonator 2
        I_st[1].buffer(len(dfq2), len(dcq2)).average().save("I2")
        Q_st[1].buffer(len(dfq2), len(dcq2)).average().save("Q2")
        
        # Oracle SCOPE:
        SCOPE = ["n", "I1", "Q1", "I2", "Q2"]

        '''


exec(code)