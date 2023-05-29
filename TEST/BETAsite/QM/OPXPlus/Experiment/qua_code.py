####################
# QUA START        #
####################

from qm.qua import *
from configuration import *
from qualang_tools.loops import from_array
from pyqum.instrument.toolbox import waveform

num_pts = 100
t = 17000//4 #//100
fres_q1 = qubit_IF_q1
fres_q2 = qubit_IF_q2
# dfs1 = np.linspace(- 450e6, + 200e6, num_pts) # qubit 1
dfs1 = np.linspace( -100e6, 490e6, num_pts) # qubit 1
ddf1 = dfs1[1] - dfs1[0]
dcs1 = np.linspace(-0.49, 0.49, num_pts) # flux 1
ddc1 = dcs1[1] - dcs1[0]
# dfs2 = np.linspace(- 450e6, + 100e6, num_pts) # qubit 2
dfs2 = np.linspace(- 120e6, 160e6, num_pts) # qubit 2
ddf2 = dfs2[1] - dfs2[0]
dcs2 = np.linspace(-0.49, 0.49, num_pts) # flux 2 
ddc2 = dcs2[1] - dcs2[0]
n_avg = 4000000

# Equalization for comparison: fixed on f_q1
fres_q2 = fres_q1
dfs2 = dfs1
ddf2 = ddf1

# QUA program
with program() as multi_qubit_spec_vs_flux:
    
    I = [declare(fixed) for i in range(2)]
    Q = [declare(fixed) for i in range(2)] 
    I_st = [declare_stream() for i in range(2)]
    Q_st = [declare_stream() for i in range(2)]
    n = declare(int)
    n_st = declare_stream()
    f_q1 = declare(int)
    f_q2 = declare(int)
    dc1 = declare(fixed)
    dc2 = declare(fixed)
    i = declare(int)
    j = declare(int)

    with for_(n, 0, n < n_avg, n+1):
        
        save(n, n_st)
        
        assign(f_q1, dfs1[0] + fres_q1)
        assign(f_q2, dfs2[0] + fres_q2)

        with for_(i, 0, i<num_pts, i+1):

            update_frequency("q1_xy", f_q1)
            update_frequency("q2_xy", f_q2)  

            # assign(dc1, dcs1[0])
            assign(dc2, dcs2[0])

            with for_(j, 0, j<num_pts, j+1):

                # Flux sweeping 
                set_dc_offset("q1_z", "single", dc2)
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

                # assign(dc1, dc1 + ddc1)
                assign(dc2, dc2 + ddc2)
                
                # DC waiting time will affect the edges of the curve:
                wait(1000)

            assign(f_q1, f_q1 + ddf1)
            assign(f_q2, f_q2 + ddf2)

    with stream_processing():

        n_st.save("n")

        # resonator 1
        I_st[0].buffer(num_pts, num_pts).average().save("I1")
        Q_st[0].buffer(num_pts, num_pts).average().save("Q1")
        
        # resonator 2
        I_st[1].buffer(num_pts, num_pts).average().save("I2")
        Q_st[1].buffer(num_pts, num_pts).average().save("Q2")
        
        # Oracle SCOPE:
        SCOPE = ["n", "I1", "Q1", "I2", "Q2"]











        