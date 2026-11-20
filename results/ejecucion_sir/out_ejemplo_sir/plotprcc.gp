set term postscript color  10 
set output "prccvals.ps"
set ytics 0.2 
set yrange [-1:1] 
set xrange [0:100] 
set xlabel 'Time(Units)' 
set title "PRCC : S"
plot 'prcc.0001' u 1:9 t 'beta', 'prcc.0001' u 1:11 t 'gamma', 'prcc.0001' u 1:13 t 'N0', 0 t '' w l 
set title "PRCC : I"
plot 'prcc.0002' u 1:9 t 'beta', 'prcc.0002' u 1:11 t 'gamma', 'prcc.0002' u 1:13 t 'N0', 0 t '' w l 
set title "PRCC : R"
plot 'prcc.0003' u 1:9 t 'beta', 'prcc.0003' u 1:11 t 'gamma', 'prcc.0003' u 1:13 t 'N0', 0 t '' w l 
exit
