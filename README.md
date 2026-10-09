# Mark Bad Channels and Segments in Raw MEG/EEG Data

[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.743-blue.svg)](https://doi.org/10.25663/brainlife.app.743)
[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)

## Description

Marks bad channels and time segments in MNE raw MEG/EEG data using `raw.info['bads']` and `mne.Annotations`. Channels marked as bad are excluded from analysis, and annotations describe segments of data to be discarded (e.g., movement artifacts, signal dropout).

The app generates:
- The raw data with updated `info['bads']` and annotations
- A power spectral density (PSD) plot (bad channels excluded)
- A `product.json` summarizing the marked channels and annotations

## Inputs

- **`raw`** (`neuro/meeg/mne/raw`): continuous raw MEG/EEG data to mark bad channels and segments in (required)
- **`channels`** (`neuro/meg/fif-override`, `channels.tsv` file): optional BIDS `channels.tsv` file; rows whose `status` column is `bad` are added to `raw.info['bads']` (optional)

## Outputs

- **`out_dir/raw.fif`** (`neuro/meeg/mne/raw`, tag `bads_marked`): raw data with marked bad channels and annotations
- **`out_figs/psd.png`**: power spectral density plot computed with bad channels excluded
- **`product.json`**: summary of marked channels and annotations, with the PSD plot embedded

## Configuration Parameters

| key | type | default | description |
|---|---|---|---|
| `bads` | string | `""` | Comma-separated list of channel names to mark as bad (e.g., `"MEG2423,MEG2422,EEG001"`). Names not present in the data are ignored. |
| `annotations` | string (multiline) | `""` | Bad data segments, one per line: `onset, duration, description[, channels]`. If `channels` is omitted the annotation applies to all channels. |
| `reset_bads` | boolean | `false` | If `true`, clears any bad channels already marked in the input file before adding the new ones from `bads`/`channels`. |

Example `annotations` value:
```
2, 2, bad_segment
5, 2, movement_artifact, MEG2121, MEG2122
```

## Usage

### Running on Brainlife.io

1. Select your raw MEG/EEG dataset as the `raw` input.
2. Optionally provide a `channels.tsv` file as the `channels` input to mark channels whose `status` column is `bad`.
3. Optionally set `bads`, `annotations`, and/or `reset_bads` in the configuration form.
4. Submit the process.

### Local Testing

```bash
# Edit config.json to point "raw" (and optionally "channels") at real data, then:
python main.py
```

## Technical Details

- **Bad Channels**: Marked in `raw.info['bads']` and excluded from analysis in downstream apps
- **Annotations**: Stored in `raw.annotations` and can be used for segment-level quality control
- **Channel Validation**: Invalid channel names in both `bads` and `annotations` are validated against the input file
- **Preload**: Data is loaded and saved efficiently without full preload unless needed

## Authors

- [Maximilien Chaumon](https://github.com/dnacombo), Paris Brain Institute

## Citations

We kindly ask that you cite the following articles when publishing papers and code using this app:

Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2

Gramfort A, et al. & Hämäläinen MS. MEG and EEG data analysis with MNE-Python. Frontiers in Neuroscience, 7(267):1–13 (2013). https://doi.org/10.3389/fnins.2013.00267

## Funding Acknowledgement

brainlife.io is publicly funded and for the sustainability of the project we kindly ask that you acknowledge the following funding sources:

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://grantome.com/grant/NIH/R01-EB030896-01)

## License

Copyright (c) 2026 MEEG Brainlife team. Licensed under AGPL-3.0, see [license.txt](license.txt).
