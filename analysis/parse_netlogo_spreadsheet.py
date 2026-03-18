"""
Universal parser for NetLogo BehaviorSpace spreadsheet CSV files.
Returns a list of dicts, one per run, with params and metrics.
"""
import csv, io

def parse_spreadsheet(path):
    """Parse a NetLogo BehaviorSpace spreadsheet CSV.
    Returns: (exp_name, list_of_run_dicts)
    Each run_dict has param names and metric names as keys.
    """
    with open(path, 'r') as f:
        content = f.read()
    
    lines = [l for l in content.strip().split('\n') if l.strip()]
    
    # Line 3 = experiment name
    exp_name = next(csv.reader(io.StringIO(lines[2])))[0]
    
    # Parse all rows into a structured format
    param_rows = {}
    header_row = None
    data_row = None
    run_number_row = None
    total_steps_row = None
    
    for i, line in enumerate(lines):
        row = next(csv.reader(io.StringIO(line)))
        if row[0] == '[run number]':
            run_number_row = row
        elif row[0] == '[total steps]':
            total_steps_row = row
        elif row[0] == '[final value]':
            header_row = row
            if i + 1 < len(lines):
                data_row = next(csv.reader(io.StringIO(lines[i + 1])))
        elif row[0] not in ('', 'min-pxcor', 'max-pxcor', 'min-pycor', 'max-pycor') \
             and not row[0].startswith('"BehaviorSpace') \
             and not row[0].startswith('"LANA') \
             and not row[0].startswith('"0') \
             and i > 4:
            # This is a parameter row
            param_rows[row[0]] = row[1:]
    
    if header_row is None or data_row is None:
        return exp_name, []
    
    # Determine metrics per run by finding [step] positions in header
    step_positions = [j for j in range(len(header_row)) if header_row[j] == '[step]']
    
    if len(step_positions) < 2:
        cols_per_run = len(header_row) - step_positions[0] if step_positions else len(header_row) - 1
    else:
        cols_per_run = step_positions[1] - step_positions[0]
    
    # Metric names (between first [step] and next [step])
    first_step = step_positions[0] if step_positions else 1
    metric_names = []
    for j in range(first_step + 1, first_step + cols_per_run):
        if j < len(header_row) and header_row[j] != '[step]':
            metric_names.append(header_row[j])
    
    # Parse runs
    runs = []
    run_idx = 0
    col = first_step
    
    while col + cols_per_run <= len(data_row) + 1:
        run_dict = {}
        
        # Add parameters
        for pname, pvals in param_rows.items():
            pcol = run_idx * cols_per_run
            if pcol < len(pvals) and pvals[pcol]:
                try:
                    run_dict[pname] = float(pvals[pcol])
                except:
                    run_dict[pname] = pvals[pcol]
        
        # Add metrics
        for m_idx, mname in enumerate(metric_names):
            dcol = col + 1 + m_idx
            if dcol < len(data_row) and data_row[dcol]:
                try:
                    run_dict[mname] = float(data_row[dcol])
                except:
                    run_dict[mname] = data_row[dcol]
        
        runs.append(run_dict)
        col += cols_per_run
        run_idx += 1
    
    return exp_name, runs

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python parse_netlogo_spreadsheet.py <csv_file>")
        print("Example: python parse_netlogo_spreadsheet.py data/E1-baseline.csv")
        sys.exit(1)
    name, runs = parse_spreadsheet(sys.argv[1])
    print(f"Experiment: {name}, Runs: {len(runs)}")
    if runs:
        print(f"First run keys: {list(runs[0].keys())}")
        print(f"First run: {runs[0]}")
