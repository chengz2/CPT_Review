
import numpy as np
import xarray as xr
from xgcm import Grid

# runs with different setup
runs=['REF','BS','BSV']

f='/ocean_daily.19980101-20021231.zos.nc'

for k in np.arange(1,3):
    
    ds = xr.open_dataset(runs[k] + f)

    nt=int(np.size(ds.time.values)/5.)
    e = ds.zos[:nt,:,:].resample(time="5D").mean(dim='time');
    ebar=e.mean('time')
    eprime=e-ebar
    ssh_v=(eprime**2).mean('time')

    np.savez(runs[k]+'_ssh_variance.npz',ssh_v=ssh_v)

    print(runs[k]+'_ssh_variance.npz created')


