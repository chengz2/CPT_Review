
import numpy as np
import xarray as xr
from xgcm import Grid


# runs with different setup
runs=['REF','BS','BSV']

fu='/ocean_daily.19980101-20021231.uo.nc'
fv='/ocean_daily.19980101-20021231.vo.nc'

for k in np.arange(1,3):
    
    ds = xr.open_dataset('ocean_annual_z.static.nc')
    dsu = xr.open_dataset(runs[k] + fu)
    dsv = xr.open_dataset(runs[k] + fv)

    nt=int(np.size(dsu.time.values)/5)
    nzl=np.size(dsu.z_l.values)
    xh = ds.xh.values
    yh = ds.yh.values
    nxh=np.size(xh)
    nyh=np.size(yh)

    # compute regridded velocity components for decomposing KE:

    # This tells the grid where xh, xq, yh, and yq are defined.
    grid= Grid(ds, coords={'X': {'center': 'xh', 'right': 'xq'}, 
                       'Y': {'center': 'yh', 'right': 'yq'}});

    u = dsu.uo[:nt,:,:,:].resample(time="5D").mean(dim='time');  
    u = grid.interp(u,axis='X')#.fillna(0.);
    ubar=u.mean('time')
 
    v  = dsv.vo[:nt,:,:,:].resample(time="5D").mean(dim='time');  
    v = grid.interp(v,axis='Y')#.fillna(0.);
    vbar=v.mean('time')

    uprime=u-ubar
    vprime=v-vbar

    dz = dsu.z_i[1:].values-dsu.z_i[:-1].values
    del u, dsu
    del v, dsv

    h = np.tile(np.transpose(np.array(dz,ndmin=3)),(1,nyh,nxh))
    h = np.where(np.isnan(ubar), np.nan, h)
    H = np.nansum(h,axis=0)

    # The mean BT and BC KE values:
    ubar_BT=np.nansum(ubar*h,axis=0)/H
    ubar_BC=ubar-ubar_BT

    vbar_BT=np.nansum(vbar*h,axis=0)/H
    vbar_BC=vbar-vbar_BT

    KE_mean_BT=0.5*(vbar_BT**2+ubar_BT**2) #dim y,x
    KE_mean_BC=np.nansum(0.5*(vbar_BC**2+ubar_BC**2)*h,axis=0)/H #dim y,x

    del ubar_BT
    del ubar_BC
    del vbar_BT
    del vbar_BC

    # Eddy BT and BC KE parts:
    uprime_BT=np.zeros([int(nt/5),nzl,nyh,nxh])
    uprime_BC=np.zeros([int(nt/5),nzl,nyh,nxh])
    vprime_BT=np.zeros([int(nt/5),nzl,nyh,nxh])
    vprime_BC=np.zeros([int(nt/5),nzl,nyh,nxh])

    for i in np.arange(0,int(nt/5)):
        uprime_BT[i,:,:,:]=np.nansum(uprime[i,:,:,:]*h,axis=0)/H
        vprime_BT[i,:,:,:]=np.nansum(vprime[i,:,:,:]*h,axis=0)/H

    uprime_BC=uprime-uprime_BT
    vprime_BC=vprime-vprime_BT

    KE_eddy_BT=np.mean((0.5*(vprime_BT[:,0,:,:]**2+uprime_BT[:,0,:,:]**2)),axis=0)
    KE_eddy_BC=np.mean(np.nansum((0.5*(vprime_BC**2+uprime_BC**2)*h),axis=1),axis=0)/H

    del uprime_BT
    del uprime_BC
    del vprime_BT
    del vprime_BC

    #Total kinetic energy:

    KE_BT_tot=KE_eddy_BT+KE_mean_BT
    KE_BC_tot=KE_eddy_BC+KE_mean_BC
    KE_tot=KE_BT_tot+KE_BC_tot

    fraction_BT=KE_BT_tot/KE_tot
    fraction_BT_eddy=KE_eddy_BT/KE_tot
    fraction_BC=KE_BC_tot/KE_tot #when you divide zero/zero it's a nan
    fraction_BC_eddy=KE_eddy_BC/KE_tot

    np.savez(runs[k]+'_BTBC_KE_fractions.npz',
         fraction_BT=fraction_BT,fraction_BT_eddy=fraction_BT_eddy,
         fraction_BC=fraction_BC,fraction_BC_eddy=fraction_BC_eddy,
         KE_eddy_BT=KE_eddy_BT,KE_mean_BT=KE_mean_BT,
         KE_eddy_BC=KE_eddy_BC,KE_mean_BC=KE_mean_BC)

    print(runs[k]+'_BTBC_KE_fractions.npz created')
