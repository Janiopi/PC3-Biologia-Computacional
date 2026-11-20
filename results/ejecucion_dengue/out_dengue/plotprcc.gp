set term postscript color  10 
set output "prccvals.ps"
set ytics 0.2 
set yrange [-1:1] 
set xrange [0:360] 
set xlabel 'Time(Units)' 
set title "PRCC : ih"
plot 'prcc.0001' u 1:9 t 'b', 'prcc.0001' u 1:11 t 'beta_h', 'prcc.0001' u 1:13 t 'beta_v', 'prcc.0001' u 1:15 t 'sigma_h', 'prcc.0001' u 1:17 t 'gamma_h', 'prcc.0001' u 1:19 t 'sigma_v', 'prcc.0001' u 1:21 t 'mu_v', 'prcc.0001' u 1:23 t 'm', 'prcc.0001' u 1:25 t 'u', 0 t '' w l 
set title "PRCC : ivr"
plot 'prcc.0002' u 1:9 t 'b', 'prcc.0002' u 1:11 t 'beta_h', 'prcc.0002' u 1:13 t 'beta_v', 'prcc.0002' u 1:15 t 'sigma_h', 'prcc.0002' u 1:17 t 'gamma_h', 'prcc.0002' u 1:19 t 'sigma_v', 'prcc.0002' u 1:21 t 'mu_v', 'prcc.0002' u 1:23 t 'm', 'prcc.0002' u 1:25 t 'u', 0 t '' w l 
set title "PRCC : ch"
plot 'prcc.0003' u 1:9 t 'b', 'prcc.0003' u 1:11 t 'beta_h', 'prcc.0003' u 1:13 t 'beta_v', 'prcc.0003' u 1:15 t 'sigma_h', 'prcc.0003' u 1:17 t 'gamma_h', 'prcc.0003' u 1:19 t 'sigma_v', 'prcc.0003' u 1:21 t 'mu_v', 'prcc.0003' u 1:23 t 'm', 'prcc.0003' u 1:25 t 'u', 0 t '' w l 
set title "PRCC : R0"
plot 'prcc.0004' u 1:9 t 'b', 'prcc.0004' u 1:11 t 'beta_h', 'prcc.0004' u 1:13 t 'beta_v', 'prcc.0004' u 1:15 t 'sigma_h', 'prcc.0004' u 1:17 t 'gamma_h', 'prcc.0004' u 1:19 t 'sigma_v', 'prcc.0004' u 1:21 t 'mu_v', 'prcc.0004' u 1:23 t 'm', 'prcc.0004' u 1:25 t 'u', 0 t '' w l 
exit
