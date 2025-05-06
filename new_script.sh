 #!/bin/bash

mkdir -p pathfinder_prefetches_gap_spec
mkdir -p generate_log

# Only run pathfinder for 605.mcf-s1
xz="./gap_spec_traces/473.astar-s1.txt.xz"
file_variable="473.astar-s1"

# Generate prefetch file
./ml_prefetch_sim.py generate "$xz" "./pathfinder_prefetches_gap_spec/integrate_fire${file_variable}.txt" --model temp  > generate_log/integrate_fire${file_variable}.log 2>&1

# Run simulation
./ml_prefetch_sim.py run "./gap_spec_traces/${file_variable}.trace.gz" --prefetch "./pathfinder_prefetches_gap_spec/integrate_fire${file_variable}.txt" --num-instructions 61219343 --results-dir "./results_IF" 
