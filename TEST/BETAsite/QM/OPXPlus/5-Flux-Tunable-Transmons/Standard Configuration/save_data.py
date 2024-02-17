from datetime import datetime
import sys
import numpy as np

def save_npz( save_dir, file_name, output_data, suffix_time:bool=True ):
    save_path = f"{save_dir}/{file_name}"
    print(f"save file: {save_path}")
    save_time = ""
    if suffix_time:
        save_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
        save_time = "_"+save_time
    save_path = save_path+save_time+".npz" 
    np.savez(save_path, **output_data)


import xarray as xr

def save_xr( save_dir, file_name, output_data:xr.Dataset, suffix_time:bool=True ):
    save_path = f"{save_dir}/{file_name}"
    print(f"save file: {save_path}")
    save_time = ""
    if suffix_time:
        save_time = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
        save_time = "_"+save_time
    save_path = save_path+save_time+".nc" 
    output_data.to_netcdf(save_path)
