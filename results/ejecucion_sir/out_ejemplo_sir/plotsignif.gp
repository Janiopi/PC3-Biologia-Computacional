set term postscript color  10 
set output "signif.ps"
set yrange [0:0.3] 
set ytics 0.01 
set xrange [0:100] 
set xlabel 'Time(Units)' 
set title "PRCC Significance: S"
plot 'prcc.0001' u 1:10 t 'beta', 'prcc.0001' u 1:12 t 'gamma', 'prcc.0001' u 1:14 t 'N0', 0 t '' w l, 0.01 t '' w l 
set title "PRCC Significance: I"
plot 'prcc.0002' u 1:10 t 'beta', 'prcc.0002' u 1:12 t 'gamma', 'prcc.0002' u 1:14 t 'N0', 0 t '' w l, 0.01 t '' w l 
set title "PRCC Significance: R"
plot 'prcc.0003' u 1:10 t 'beta', 'prcc.0003' u 1:12 t 'gamma', 'prcc.0003' u 1:14 t 'N0', 0 t '' w l, 0.01 t '' w l 
exit
