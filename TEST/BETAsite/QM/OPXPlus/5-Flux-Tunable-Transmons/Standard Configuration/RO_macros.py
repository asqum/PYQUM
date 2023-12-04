"""
This file contains useful QUA macros meant to simplify and ease QUA programs.
All the macros below have been written and tested with the basic configuration. If you modify this configuration
(elements, operations, integration weights...) these macros will need to be modified accordingly.
"""

from qm.qua import *
from qualang_tools.addons.variables import assign_variables_to_element
from qualang_tools.results import fetching_tool, progress_counter
from qualang_tools.plot import interrupt_on_close
from configuration import *

import matplotlib.pyplot as plt
from scipy import signal
from scipy.optimize import curve_fit

##############
# QUA macros #
##############
def multiRO_declare( resonators:list ):
    """
    Macro to declare the necessary QUA variables

    :param resonators: name of the element for resonator
    :return: I, I_st, Q, Q_st
    """
    if type(resonators) is not list:
        resonators = [resonators]

    ro_channel_num = len(resonators)

    I = [declare(fixed) for _ in range(ro_channel_num)]
    Q = [declare(fixed) for _ in range(ro_channel_num)]
    I_st = [declare_stream() for _ in range(ro_channel_num)]
    Q_st = [declare_stream() for _ in range(ro_channel_num)]
    # Workaround to manually assign the results variables to the readout elements
    for idx, ele_name in enumerate(resonators):
        assign_variables_to_element( ele_name, I[idx], Q[idx])
    return I, I_st, Q, Q_st

def multiRO_measurement( iqdata_stream, resonators:list, sequential=False, amp_modify=1.0, weights=""):
    """
        RO pulse
    """
    (I, I_st, Q, Q_st) = iqdata_stream
    if type(resonators) is not list:
        resonators = [resonators] 
    ro_channel_num = len(resonators)

    for idx, res in enumerate(resonators):
        measure(
            "readout" * amp(amp_modify),
            f"{res}",
            None,
            dual_demod.full(weights + "cos", "out1", weights + "sin", "out2", I[idx]),
            dual_demod.full(weights + "minus_sin", "out1", weights + "cos", "out2", Q[idx]),
        )

        if I_st is not None:
            save(I[idx], I_st[idx])
        if Q_st is not None:
            save(Q[idx], Q_st[idx])

        if sequential and idx < ro_channel_num -1:
            align(f"{res}", f"{resonators[idx+1]}")



def multiRO_pre_save( iqdata_stream, resonators:list, buffer_shape:tuple, suffix:str='' ):
    """
    Save RO pulse signal on FPGA
    """
    (I, I_st, Q, Q_st) = iqdata_stream
    if type(resonators) is not list:
        resonators = [resonators]
        
    ro_channel_num = len(resonators)
    for idx_res, res in enumerate(resonators):
        I_st[idx_res].buffer(*buffer_shape).average().save(f"{res}_I{suffix}")
        Q_st[idx_res].buffer(*buffer_shape).average().save(f"{res}_Q{suffix}") 

def multiRO_pre_save_singleShot( iqdata_stream, resonators:list, suffix:str='' ):
    """
    Save RO pulse signal on FPGA
    """
    (I, I_st, Q, Q_st) = iqdata_stream
    if type(resonators) is not list:
        resonators = [resonators]
        
    ro_channel_num = len(resonators)
    for idx_res, res in enumerate(resonators):
        I_st[idx_res].save_all(f"{res}_I{suffix}")
        Q_st[idx_res].save_all(f"{res}_Q{suffix}")  



def state_tomo_singleRO_declare( resonators:list ):
    """
    Only NQ 
    :param resonators: name of the element for resonator
    :return: I, I_st, Q, Q_st
    """
    if type(resonators) is not list:
        resonators = [resonators]

    ro_channel_num = len(resonators)


    I = [declare(fixed) for _ in range(ro_channel_num)]
    Q = [declare(fixed) for _ in range(ro_channel_num)]
    I_st = [declare_stream() for _ in range(ro_channel_num)]
    Q_st = [declare_stream() for _ in range(ro_channel_num)]
    # Workaround to manually assign the results variables to the readout elements
    for idx, ele_name in enumerate(resonators):
        assign_variables_to_element( ele_name, I[idx], Q[idx])

    return I, I_st, Q, Q_st

def state_tomo_measurement( iqdata_stream, process, q_name, resonators, thermalization_time=200, sequential=False, amp_modify=1.0, weights=""):
    """
        Only for 1Q 
    """
    (I, I_st, Q, Q_st) = iqdata_stream
    if type(resonators) is not list:
        resonators = [resonators]

    if type(q_name) is list:
        q_name = q_name[0]    
    ro_channel_num = len(resonators)
    basis = declare(int)
    

    with for_each_(basis, [0, 1, 2]):
        wait(thermalization_time * u.us)

        process()
        align()
        with switch_(basis, unsafe=True):
            with case_(0):
                pass
            with case_(1):
                play("y90", q_name)
            with case_(2):
                play("-x90", q_name)
        # Measure resonator state after the sequence
        align()
        for idx, res in enumerate(resonators):
            measure(
                "readout" * amp(amp_modify),
                f"{res}",
                None,
                dual_demod.full(weights + "cos", "out1", weights + "sin", "out2", I[idx]),
                dual_demod.full(weights + "minus_sin", "out1", weights + "cos", "out2", Q[idx]),
            )

            if sequential and idx < ro_channel_num -1:
                align(f"{res}", f"{resonators[idx+1]}")

            save(I[idx], I_st[idx])
            save(Q[idx], Q_st[idx])



def tomo_pre_save_singleShot( iqdata_stream, q_name:list, resonators:list, suffix:str='' ):
    """
    Save RO pulse signal on FPGA
    """
    (I, I_st, Q, Q_st) = iqdata_stream
    if type(resonators) is not list:
        resonators = [resonators]
    if type(q_name) is not list:
        q_name = [q_name]
    q_dim = tuple( [3] *len(q_name) )
    ro_channel_num = len(resonators)
    for idx_res, res in enumerate(resonators):
        I_st[idx_res].buffer(*q_dim).save_all(f"{res}_I{suffix}")
        Q_st[idx_res].buffer(*q_dim).save_all(f"{res}_Q{suffix}")  




def state_tomo_NQ_measurement( QV, iqdata_stream, process, q_name, resonators, thermalization_time=200, sequential=False, amp_modify=1.0, weights="" ):
    """
       for NQ 
       q_name should have same length with resonators
    """
    (I, I_st, Q, Q_st) = iqdata_stream

    wait(thermalization_time)
    process()
    align()
    for q, basis in QV:
        with switch_(basis, unsafe=True):
            with case_(0):
                pass
            with case_(1):
                play("y90", f"{q}")
            with case_(2):
                play("-x90", f"{q}")
    # Measure resonator state after the sequence
    align()
    multiRO_measurement( iqdata_stream, resonators, weights=weights )
        # with else_(layer_idx==1):
        #     state_tomo_measurement( iqdata_stream, process, q_next, resonators, thermalization_time=200, sequential=False, amp_modify=1.0, weights="" )

def tomo_NQ_proj( iqdata_stream, process, q_name, resonators, thermalization_time=200, sequential=False, weights="", q_proj=[] )->list:

    q_current = q_name[-1]
    proj = declare(int)
    with for_each_(proj, [0, 1, 2]):
        q_proj_next = q_proj +[(q_current,proj)]
        if len(q_name) > 1:
            q_next = q_name[:-1]
            tomo_NQ_proj( iqdata_stream, process, q_next, resonators, thermalization_time=thermalization_time, sequential=sequential, weights=weights, q_proj=q_proj_next )
        else:
            state_tomo_NQ_measurement( q_proj_next, iqdata_stream, process, q_name, resonators, thermalization_time=thermalization_time, weights=weights )
