import re
import os
import pandas as pd

data = []

for filename in os.listdir('.'):
    if filename.endswith('.txt'):
        # Extract trace name and mode from filename
        match = re.match(r'(.+?)\.trace\.(?:gz|xz)-(.+?)\.txt$', filename)
        if match:
            trace_name = match.group(1)
            mode = match.group(2)
        else:
            trace_name = 'Unknown'
            mode = 'Unknown'

        with open(filename, 'r') as file:
            content = file.read()

            ipc_match = re.search(r'Finished CPU 0 instructions: \d+ cycles: \d+ cumulative IPC: ([\d\.eE+-]+)', content)
            ipc = float(ipc_match.group(1)) if ipc_match else None

            # Extract LLC PREFETCH USEFUL
            useful_match = re.search(r'LLC PREFETCH\s+REQUESTED:.*?USEFUL:\s+(\d+)', content)
            useful = int(useful_match.group(1)) if useful_match else 0

            # Extract LLC PREFETCH ISSUED
            issued_match = re.search(r'LLC PREFETCH\s+REQUESTED:.*?ISSUED:\s+(\d+)', content)
            issued = int(issued_match.group(1)) if issued_match else 0

            # Extract LLC LOAD ACCESS
            load_access_match = re.search(r'LLC LOAD\s+ACCESS:\s+(\d+)', content)
            load_access = int(load_access_match.group(1)) if load_access_match else 0

            accuracy = useful / issued if issued != 0 else 0
            coverage = useful / load_access if load_access != 0 else 0

            data.append({
                'Trace': trace_name,
                'Mode': mode,
                'IPC': ipc,
                'Accuracy': accuracy,
                'Coverage': coverage
            })

df = pd.DataFrame(data)

df_sorted = df.sort_values(by='Trace')

df_sorted.to_csv('simulation_metrics.csv', index=False, float_format='%.3f')
