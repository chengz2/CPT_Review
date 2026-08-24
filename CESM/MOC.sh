module load nco

mkdir tmp

# REF
for y in $(seq 49 60); do
   ncra -v vmo,rho2_l gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.smag_control.003_daily/ocn/hist/gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.smag_control.003.mom6.h.rho2.00${y}-??.nc tmp/00${y}.ocean_annual_rho2.vmo.nc
done
ncrcat tmp/????.ocean_annual_rho2.vmo.nc REF/0049-0060.ocean_annual_rho2.vmo.nc
rm tmp/*

# MBK
for y in $(seq 49 60); do
   ncra -v vmo,rho2_l gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.MEKE_GM.007_daily/ocn/hist/gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.MEKE_GM.007.mom6.h.rho2.00${y}-??.nc tmp/00${y}.ocean_annual_rho2.vmo.nc
done
ncrcat tmp/????.ocean_annual_rho2.vmo.nc MBK/0049-0060.ocean_annual_rho2.vmo.nc
rm tmp/*

# LBK
for y in $(seq 49 60); do
   ncra -v vmo,rho2_l gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.leith_GM.028_daily/ocn/hist/gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.leith_GM.028.mom6.h.rho2.00${y}-??.nc tmp/00${y}.ocean_annual_rho2.vmo.nc
done
ncrcat tmp/????.ocean_annual_rho2.vmo.nc LBK/0049-0060.ocean_annual_rho2.vmo.nc
rm tmp/*

rmdir tmp
