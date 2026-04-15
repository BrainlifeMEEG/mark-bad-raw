"""
Mark bad channels and segments in MNE raw data.

This app marks bad channels and time segments in raw MEG/EEG data using
MNE's raw.info['bads'] and mne.Annotations mechanisms. Channels marked as
bad are excluded from analysis, and annotations describe segments of data
to be discarded (e.g., movement artifacts, signal dropout).

Inputs:
    - config.json:
      - mne: Path to MNE raw .fif file
      - bads: channels.tsv file of channels to mark as bad (optional)
      - annotations: Optional multiline annotations in format:
        "onset, duration, description[, channels]"

Outputs:
    - out_dir/raw.fif: Raw data with marked bad channels and annotations
    - product.json: Summary of marked channels and annotations
"""

# Copyright (c) 2026 brainlife.io
#
# This app marks bad segments and channels "by hand" in a MNE/raw file
#
# Author: Maximilien Chaumon (https://github.com/dnacombo)

import sys
import os
import re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

# Standard imports
import numpy as np
import mne
import pandas as pd
import matplotlib.pyplot as plt

# Import shared utilities
from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    add_image_to_product,
    add_raw_info_to_product
)

# Set up matplotlib for headless execution
setup_matplotlib_backend()

# Ensure output directories exist
ensure_output_dirs('out_dir', 'out_figs')

# Load configuration
config = load_config()

# == LOAD DATA ==
data_file = config['raw']
raw = mne.io.read_raw_fif(data_file, verbose=False)

# == MARK BAD CHANNELS ==
# Reset bad channels if requested
reset_bads = config.get('reset_bads', False)
if reset_bads:
    raw.info['bads'] = []

if config['bads']:
    # Parse comma-separated channel names
    bads = config['bads'].split(',')
    # Trim leading and trailing spaces
    bads = [b.strip() for b in bads]
    # Remove empty strings
    bads = [b for b in bads if b != '']
    # Filter to only channels that exist in the raw file
    bads = [ch for ch in bads if ch in raw.ch_names]
    if bads:
        raw.info['bads'].extend(bads)
        raw.info['bads'] = list(set(raw.info['bads']))  # Remove duplicates

if config['channels']:
    # read channels.tsv
    channels_tsv = config['channels']
    channels_df = pd.read_csv(channels_tsv, sep='\t')
    for _, row in channels_df.iterrows():
        if row.get('status', '').lower() == 'bad' and row['name'] in raw.ch_names:
            raw.info['bads'].append(row['name'])
    raw.info['bads'] = list(set(raw.info['bads']))  # Remove duplicates

# == ADD ANNOTATIONS ==
nuan = config.get("annotations")
if nuan:
    nuan = nuan.split("\n")
    nuan = [re.split("[,;-]", n) for n in nuan]
    # Remove trailing spaces from each element of nuan
    for n in nuan:
        for i in range(len(n)):
            n[i] = n[i].strip()

    onset = list()
    duration = list()
    description = list()
    ch_names = list()
    for a in nuan:
        if len(a) < 3:  # Skip lines with insufficient data
            continue
        onset.append(a.pop(0))
        duration.append(a.pop(0))
        description.append(a.pop(0))
        ch_names.append(a)
        # Validate that channels exist in raw data
        not_there = [elem for elem in ch_names[-1] if elem not in raw.ch_names]
        if ch_names[-1] != [] and len(not_there) > 0:
            raise Exception(f"Channels {not_there} mentioned in annotations not present in the data.")

    annot = mne.Annotations(
        onset=onset,
        duration=duration,
        description=description,
        ch_names=ch_names
    )
    print(annot)
    raw.set_annotations(annot)

# == SAVE DATA ==
raw.save(os.path.join('out_dir', 'raw.fif'), overwrite=True)

# == CREATE PSD PLOT ==
fig = raw.compute_psd().plot(exclude='bads', show=False)
fig.savefig(os.path.join('out_figs', 'psd.png'), dpi=100, bbox_inches='tight')
plt.close(fig)

# == CREATE PRODUCT JSON ==
product_items = []

# Add raw info
add_raw_info_to_product(product_items, raw)

# Add marked bad channels summary
if raw.info['bads']:
    bads_msg = f"Marked bad channels: {', '.join(raw.info['bads'])}"
    add_info_to_product(product_items, bads_msg, msg_type='success')

# Add annotations summary
if raw.annotations:
    n_annotations = len(raw.annotations)
    annot_msg = f"Added {n_annotations} annotation(s)"
    add_info_to_product(product_items, annot_msg, msg_type='success')

# Add PSD plot if it exists
psd_image_path = os.path.join('out_figs', 'psd.png')
if os.path.exists(psd_image_path):
    add_image_to_product(product_items, name='Power Spectral Density (PSD)', filepath=psd_image_path)

create_product_json(product_items)
