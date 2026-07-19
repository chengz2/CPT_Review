#!bin/bash

module load nco

mkdir tmp

# REF
for y in $(seq 33 52); do
   ncra -v mlotst gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.smag_control.003/ocn/hist/gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.smag_control.003.mom6.h.sfc.00${y}-??.nc tmp/00${y}.ocean_monthly.mlotst.nc
done
ncrcat tmp/????.ocean_monthly.mlotst.nc REF/0033-0052.ocean_monthly_mean.MLD.nc
rm tmp/*

# MBK
for y in $(seq 33 52); do
   ncra -v mlotst gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.MEKE_GM.007/ocn/hist/gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.MEKE_GM.007.mom6.h.sfc.00${y}-??.nc tmp/00${y}.ocean_monthly.mlotst.nc
done
ncrcat tmp/????.ocean_monthly.mlotst.nc MBK/0033-0052.ocean_monthly_mean.MLD.nc
rm tmp/*

# LBK
for y in $(seq 33 52); do
   ncra -v mlotst gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.leith_GM.028/ocn/hist/gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.leith_GM.028.mom6.h.sfc.00${y}-??.nc tmp/00${y}.ocean_monthly.mlotst.nc
done
ncrcat tmp/????.ocean_monthly.mlotst.nc LBK/0033-0052.ocean_monthly_mean.MLD.nc
rm tmp/*

rmdir tmp
