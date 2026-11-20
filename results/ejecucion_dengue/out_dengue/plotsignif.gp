set term postscript color  10 
set output "signif.ps"
set yrange [0:0.3] 
set ytics 0.01 
set xrange [0:360] 
set xlabel 'Time(Units)' 
set title "PRCC Significance: ih"
plot 'prcc.0001' u 1:10 t 'b', 'prcc.0001' u 1:12 t 'beta_h', 'prcc.0001' u 1:14 t 'beta_v', 'prcc.0001' u 1:16 t 'sigma_h', 'prcc.0001' u 1:18 t 'gamma_h', 'prcc.0001' u 1:20 t 'sigma_v', 'prcc.0001' u 1:22 t 'mu_v', 'prcc.0001' u 1:24 t 'm', 'prcc.0001' u 1:26 t 'u', 0 t '' w l, 0.01 t '' w l 
set title "PRCC Significance: ivr"
plot 'prcc.0002' u 1:10 t 'b', 'prcc.0002' u 1:12 t 'beta_h', 'prcc.0002' u 1:14 t 'beta_v', 'prcc.0002' u 1:16 t 'sigma_h', 'prcc.0002' u 1:18 t 'gamma_h', 'prcc.0002' u 1:20 t 'sigma_v', 'prcc.0002' u 1:22 t 'mu_v', 'prcc.0002' u 1:24 t 'm', 'prcc.0002' u 1:26 t 'u', 0 t '' w l, 0.01 t '' w l 
set title "PRCC Significance: ch"
plot 'prcc.0003' u 1:10 t 'b', 'prcc.0003' u 1:12 t 'beta_h', 'prcc.0003' u 1:14 t 'beta_v', 'prcc.0003' u 1:16 t 'sigma_h', 'prcc.0003' u 1:18 t 'gamma_h', 'prcc.0003' u 1:20 t 'sigma_v', 'prcc.0003' u 1:22 t 'mu_v', 'prcc.0003' u 1:24 t 'm', 'prcc.0003' u 1:26 t 'u', 0 t '' w l, 0.01 t '' w l 
set title "PRCC Significance: R0"
plot 'prcc.0004' u 1:10 t 'b', 'prcc.0004' u 1:12 t 'beta_h', 'prcc.0004' u 1:14 t 'beta_v', 'prcc.0004' u 1:16 t 'sigma_h', 'prcc.0004' u 1:18 t 'gamma_h', 'prcc.0004' u 1:20 t 'sigma_v', 'prcc.0004' u 1:22 t 'mu_v', 'prcc.0004' u 1:24 t 'm', 'prcc.0004' u 1:26 t 'u', 0 t '' w l, 0.01 t '' w l 
exit
