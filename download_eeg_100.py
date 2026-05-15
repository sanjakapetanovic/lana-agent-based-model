#!/usr/bin/env python3
"""
Download EEGBCI EEG data for 100 subjects.
Run 1 = eyes open, Run 2 = eyes closed.
"""
import mne
import os

output_dir = r"C:\LANA_EEG_100\eeg_data"
os.makedirs(output_dir, exist_ok=True)

N = 100
subjects = list(range(1, N + 1))

print(f"Downloading EEGBCI data for {N} subjects...")
print(f"Output: {output_dir}\n")

ok = 0
fail = 0
for subj in subjects:
    print(f"  Subject {subj:3d}/{N}...", end=" ")
    try:
        mne.datasets.eegbci.load_data(subj, [1], path=output_dir)
        mne.datasets.eegbci.load_data(subj, [2], path=output_dir)
        print("OK")
        ok += 1
    except Exception as e:
        print(f"ERROR: {e}")
        fail += 1

print(f"\nDone! {ok} subjects downloaded, {fail} failed.")
print(f"Files in: {output_dir}")
print(f"\nNext: copy LANA CSVs to C:\\LANA_EEG_100\\lana_data\\")
print(f"Then run: py lana_eeg_pipeline_v5.py")
