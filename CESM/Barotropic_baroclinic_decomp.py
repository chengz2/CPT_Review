import dask
import numpy as np
import xarray as xr
import gc
from xgcm import Grid
from xarray.coders import CFDatetimeCoder

dask.config.set(scheduler='threads', num_workers=8)

# runs with different setup
runs = ['REF', 'MBK', 'LBK']
cases = ['gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.smag_control.003',
         'gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.MEKE_GM.007',
         'gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.leith_GM.028']

ds = xr.open_dataset('ocean_annual_z.static.nc').squeeze('time', drop=True)

xh = ds.xh.values
yh = ds.yh.values
nxh = np.size(xh)
nyh = np.size(yh)

# This tells the grid where xh, xq, yh, and yq are defined.
grid = Grid(ds, coords={'X': {'center': 'xh', 'right': 'xq'},
                        'Y': {'center': 'yh', 'right': 'yq'}},
            periodic=['X'], autoparse_metadata=False)

for k in range(0, 3):

    dsuv = xr.open_mfdataset(cases[k]+"_daily/ocn/hist/"+cases[k]+".mom6.h.daily.004[3-7]-??.nc",
                             combine="by_coords", decode_timedelta=True,
                             decode_times=CFDatetimeCoder(use_cftime=True))

    # compute regridded velocity components for decomposing KE
    u = dsuv.uo.chunk({"time": 10})
    u = u.resample(time="5D").mean(dim='time')
    u = grid.interp(u, axis='X')
    ubar = u.mean('time')

    v = dsuv.vo.chunk({"time": 10})
    v = v.resample(time="5D").mean(dim='time')
    v = grid.interp(v, axis='Y')
    vbar = v.mean('time')

    uprime = u - ubar
    vprime = v - vbar

    # Compute layer thickness and total depth
    dz = dsuv.z_i[1:].values - dsuv.z_i[:-1].values
    dz = xr.DataArray(dz, dims=['z_l'])

    h = dz.where(~np.isnan(ubar)).persist()
    H = h.sum(dim='z_l', skipna=True).persist()

    # Mean BT and BC kinetic energy
    ubar_BT = (ubar * dz).sum(dim='z_l', skipna=True) / H
    vbar_BT = (vbar * dz).sum(dim='z_l', skipna=True) / H

    ubar_BC = ubar - ubar_BT
    vbar_BC = vbar - vbar_BT

    KE_mean_BT = 0.5 * (vbar_BT**2 + ubar_BT**2)
    KE_mean_BC = (0.5 * (vbar_BC**2 + ubar_BC**2) * h).sum(dim='z_l', skipna=True) / H

    # Eddy BT and BC kinetic energy
    uprime_BT = (uprime * h).sum(dim='z_l', skipna=True) / H
    vprime_BT = (vprime * h).sum(dim='z_l', skipna=True) / H

    uprime_BC = uprime - uprime_BT
    vprime_BC = vprime - vprime_BT

    KE_eddy_BT = (0.5 * (vprime_BT**2 + uprime_BT**2)).mean(dim='time')
    KE_eddy_BC = (0.5 * (vprime_BC**2 + uprime_BC**2)
                  * h).sum(dim='z_l', skipna=True).mean(dim='time') / H

    # Total kinetic energy
    KE_BT_tot = KE_eddy_BT + KE_mean_BT
    KE_BC_tot = KE_eddy_BC + KE_mean_BC

    KE_tot = KE_BT_tot + KE_BC_tot

    fraction_BT = KE_BT_tot / KE_tot
    fraction_BC = KE_BC_tot / KE_tot

    fraction_BT_eddy = KE_eddy_BT / KE_tot
    fraction_BC_eddy = KE_eddy_BC / KE_tot

    # Calculation
    (KE_mean_BT, KE_mean_BC, KE_eddy_BT, KE_eddy_BC,
     fraction_BT, fraction_BT_eddy, fraction_BC, fraction_BC_eddy) = dask.compute(
        KE_mean_BT, KE_mean_BC, KE_eddy_BT, KE_eddy_BC,
        fraction_BT, fraction_BT_eddy, fraction_BC, fraction_BC_eddy
    )

    # Save data
    np.savez(runs[k]+'_BTBC_KE_fractions.npz',
             fraction_BT=fraction_BT, fraction_BT_eddy=fraction_BT_eddy,
             fraction_BC=fraction_BC, fraction_BC_eddy=fraction_BC_eddy,
             KE_eddy_BT=KE_eddy_BT, KE_mean_BT=KE_mean_BT,
             KE_eddy_BC=KE_eddy_BC, KE_mean_BC=KE_mean_BC)

    gc.collect()

    print(runs[k]+'_BTBC_KE_fractions.npz created')
