#!bin/bash

module load nco

mkdir tmp

# REF
for y in $(seq 33 52); do
   ncra -v vmo gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.smag_control.003/ocn/hist/gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.smag_control.003.mom6.h.native.00${y}-??.nc tmp/00${y}.ocean_annual_rho2.vmo.nc
done
ncrcat tmp/????.ocean_annual_rho2.vmo.nc REF/0033-0052.ocean_annual_rho2.vmo.nc
rm tmp/*

# MBK
for y in $(seq 33 52); do
   ncra -v vmo gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.MEKE_GM.007/ocn/hist/gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.MEKE_GM.007.mom6.h.native.00${y}-??.nc tmp/00${y}.ocean_annual_rho2.vmo.nc
done
ncrcat tmp/????.ocean_annual_rho2.vmo.nc MBK/0033-0052.ocean_annual_rho2.vmo.nc
rm tmp/*

# LBK
for y in $(seq 33 52); do
   ncra -v vmo gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.leith_GM.028/ocn/hist/gmom.e23.GJRAv3.TL319_t025_hycom1_N75.tx1_4.leith_GM.028.mom6.h.native.00${y}-??.nc tmp/00${y}.ocean_annual_rho2.vmo.nc
done
ncrcat tmp/????.ocean_annual_rho2.vmo.nc LBK/0033-0052.ocean_annual_rho2.vmo.nc
rm tmp/*

rmdir tmp
