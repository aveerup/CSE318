rm plot_data.txt 2> /dev/null 
touch plot_data.txt
echo "criteria, max_depth, avg_accuracy, nodes" > plot_data.txt

g++ decision_tree_2.cpp -o dcsn.out

for i in {0..9}; do 
    ./dcsn.out IG $i
done

for i in {0..9}; do 
    ./dcsn.out IGR $i
done

for i in {0..9}; do 
    ./dcsn.out NWIG $i
done

./venv/bin/python3 generate_plot.py