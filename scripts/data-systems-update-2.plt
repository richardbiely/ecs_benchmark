# Scale font and line width (dpi) by changing the size! It will always display stretched.
set terminal png size 1024,800 enhanced font "Arial,14"
set output 'systems-update-result-2.png'

# Key means label...
set key inside bottom right
set xlabel 'Entities'
set ylabel 'Time per Operation (ns/op)'
set title 'ECS Benchmark'

set logscale x 2
set logscale y 10
set format x "2^{%L}"
set format y "10^{%L}"

## the labels are in Alphabetical order
plot  "data-systems-update-2.dat" using 1:2 title 'Anax' with lines lw 3, \
    "data-systems-update-2.dat" using 1:3 title 'EnTT' with lines lw 3, \
    "data-systems-update-2.dat" using 1:4 title 'Artemis' with lines lw 3, \
	"data-systems-update-2.dat" using 1:5 title 'EntityX1' with lines lw 3, \
	"data-systems-update-2.dat" using 1:6 title 'EntityX2' with lines lw 3

