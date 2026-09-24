SELECT *, shipper_fsc-carrier_fsc AS spread,
 (shipper_fsc-carrier_fsc)*load_miles*1000 AS dollars_per_1000_loads
FROM model.dt_surcharge_clocks
