
import numpy as np
import xarray as xr
from xgcm import Grid

# runs with different setup
runs = ['REF','MBK','LBK']
cases = ['gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.smag_control.003',
         'gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.MEKE_GM.007',
         'gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.leith_GM.028']

# GFDL uses data from 1998 to 2002, corresponding to years 0041 to 0045 in CESM runs
for k in range(0,3):

    ds = xr.open_mfdataset(cases[k]+"/ocn/hist/"+cases[k]+".mom6.h.sfc.004[1-5]-??.nc",
         combine="by_coords", chunks={"time": 30})

    e = ds.SSH.resample(time="5D").mean(dim="time")   # 5-day means, full record, lazy
    ebar = e.mean("time")
    eprime = e - ebar
    ssh_v = (eprime**2).mean("time")

    ssh_v = ssh_v.compute()   # only now does actual computation happen

    np.savez(runs[k]+'_ssh_variance.npz',ssh_v=ssh_v)

    print(runs[k]+'_ssh_variance.npz created')

