
# Pathfinder: An SNN-Based Prefetcher

**Pathfinder** is a spiking neural network (SNN)–based prefetcher integrated with **ChampSim**.
It explores new SNN node designs within the **BindsNET** framework to achieve improved hardware efficiency with minimal performance trade-off.

---

## Compilation & Execution

To build **Pathfinder**, run:

```bash
./ml_prefetch_sim.py build
```

### Available Commands

The `ml_prefetch_sim.py` script supports the following options:

| Command    | Description                                         |
| ---------- | --------------------------------------------------- |
| `build`    | Builds base and prefetcher ChampSim binaries        |
| `run`      | Runs ChampSim on specified traces                   |
| `eval`     | Parses and computes metrics from simulation results |
| `train`    | Trains the SNN model                                |
| `generate` | Generates the prefetch file                         |

After building, use the provided script to run simulations:

```bash
./run_pathfinder_gap_spec.sh
```

This script:

1. Generates prefetch files for each trace using the `generate` option.
2. Runs the corresponding ChampSim binary with the generated prefetch file.

> **Note:** The `generate` step can take several hours per trace due to the BindsNET-based SNN simulation.

---

## Downloading Traces

Download GAP and SPEC traces using:

```bash
./download.sh
```

---

## Results

Simulation outputs and prefetcher performance results are stored in:

```
pathfinder_prefetches_gap_spec/
```

---

## BindsNET Integration

Pathfinder introduces new **SNN nodes** and **models** within the [BindsNET](https://github.com/BindsNET/bindsnet) framework.
These can be found in:

* `bindsnet.network.nodes`
* `bindsnet.models`

The modified models are:

* DiehlAndCook2015ModifiedExc - Modified the excitatory layer of the SNN with Integrate and Fire nodes instead of the classic LIF nodes (remove the leak).
* DiehlAndCook2015ModifiedInh - Modified the inhibitory layer of the SNN with linear decay instead of exponential decay.

Use these new models when constructing the SNN in:

* `pathfinder_pcpage_functions.py`
* `model.py`

The aim is to explore novel neuron and connection types that reduce hardware cost while preserving prediction accuracy.

---

## Repository Structure

```
├── ml_prefetch_sim.py              # Main interface for build, run, train, and generate options
├── run_pathfinder_gap_spec.sh      # Automates generation and execution for all traces
├── download.sh                     # Downloads GAP and SPEC traces
├── bindsnet/                       # The SNN simulation framework
├── pathfinder_pcpage_functions.py  # SNN construction and prefetch logic
├── model.py                        # Defines SNN architecture
└── pathfinder_prefetches_gap_spec/ # Stores simulation results
```
