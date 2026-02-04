# app-mark_bad-raw

[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.XXX-blue.svg)](https://doi.org/10.25663/brainlife.app.XXX)

## Description

Marks bad channels and time segments in MNE raw MEG/EEG data using `raw.info['bads']` and `mne.Annotations`. Channels marked as bad are excluded from analysis, and annotations describe segments of data to be discarded (e.g., movement artifacts, signal dropout).

## Inputs

- **mne**: Path to MNE raw `.fif` file

## Outputs

- **out_dir/raw.fif**: Raw data with marked bad channels and annotations
- **product.json**: Summary of marked channels and annotations

## Configuration Parameters

- **mne** (string): Path to input MNE raw `.fif` file
- **bads** (string, optional): Comma-separated list of channel names to mark as bad (e.g., "MEG2423,MEG2422,EEG001"). Leave empty if no additional channels need to be marked.
- **reset_bads** (boolean, optional): If `true`, clears any bad channels already marked in the input file before marking new ones. If `false` (default), appends new bad channels to existing ones. Default: `false`
- **annotations** (string, optional): Multiline text describing time segments to annotate. Each line follows the format: "onset, duration, description[, channels]"
  - **onset**: Start time in seconds
  - **duration**: Duration in seconds
  - **description**: Label for the annotation
  - **channels** (optional): Specific channels affected by the annotation
  
  Example:
  ```
  2, 2, bad_segment
  5, 2, movement_artifact, MEG2121, MEG2122
  ```

## Usage

The app:
1. Loads the raw MNE data file
2. Optionally resets bad channels if `reset_bads` is enabled
3. Marks additional channels as bad if specified in config
4. Adds time-based annotations if specified in config
5. Saves the updated raw data with marked bad channels and annotations
6. Generates a product.json with detailed information

## Technical Details

- **Bad Channels**: Marked in `raw.info['bads']` and excluded from analysis in downstream apps
- **Annotations**: Stored in `raw.annotations` and can be used for segment-level quality control
- **Channel Validation**: Invalid channel names in both bads and annotations are validated against the input file
- **Preload**: Data is loaded and saved efficiently without full preload unless needed

## Authors
- [Maximilien Chaumon](https://github.com/dnacombo), Paris Brain Institute

## Citations

We kindly ask that you cite the following articles when publishing papers and code using this app:

**brainlife.io: A decentralized and open source cloud platform to support neuroscience research**. Hayashi, S., Caron, B. A., et al. & Pestilli, F. (2023). ArXiv. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10274934/

**MEG and EEG data analysis with MNE-Python**. Gramfort A, et al. & Hämäläinen MS. (2013). Frontiers in Neuroscience, 7(267):1–13. https://doi.org/10.3389/fnins.2013.00267

## Funding Acknowledgement

brainlife.io is publicly funded and for the sustainability of the project we kindly ask that you acknowledge the following funding sources:

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://grantome.com/grant/NIH/R01-EB030896-01)

#### MIT Copyright (c) 2026 brainlife.io The University of Texas at Austin and Indiana University