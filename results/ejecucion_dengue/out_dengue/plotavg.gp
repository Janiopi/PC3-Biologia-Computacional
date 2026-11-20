set term postscript color  10 
set output "stats.ps"
set xlabel 'Time(Units)' 
set title "Stats :ih"
plot 'prcc.0001' u 1:2:7:8 t 'Avg' w errorbars, 'prcc.0001' u 1:6 t 'Min' w l, 'prcc.0001' u 1:5 t 'Max' w l
set title "Stats :ivr"
plot 'prcc.0002' u 1:2:7:8 t 'Avg' w errorbars, 'prcc.0002' u 1:6 t 'Min' w l, 'prcc.0002' u 1:5 t 'Max' w l
set title "Stats :ch"
plot 'prcc.0003' u 1:2:7:8 t 'Avg' w errorbars, 'prcc.0003' u 1:6 t 'Min' w l, 'prcc.0003' u 1:5 t 'Max' w l
set title "Stats :R0"
plot 'prcc.0004' u 1:2:7:8 t 'Avg' w errorbars, 'prcc.0004' u 1:6 t 'Min' w l, 'prcc.0004' u 1:5 t 'Max' w l
exit
