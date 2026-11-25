<h1 align="center">Mark bad data</h1>

<p align="center">
  Marks bad channels and bad time segments in raw MEG/EEG data with MNE-Python, from a channel list, a BIDS channels.tsv and annotation lines, and outputs the updated raw .fif with a PSD plot.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.743"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.743-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-see_LICENSE-lightgrey.svg" alt="License"></a>
</p>

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Marks bad channels and bad time segments in raw MEG/EEG data with MNE-Python, from a channel list, a BIDS channels.tsv and annotation lines, and outputs the updated raw .fif with a PSD plot.**

Adds channels to raw.info['bads'] from the bads parameter and from rows of a channels.tsv whose status is 'bad', and adds mne.Annotations for segments given as 'onset, duration, description[, channels]' lines. Use it to record manual quality-control decisions so downstream Apps exclude those channels and segments. reset_bads clears existing bad channels first.

| | |
|---|---|
| **Inputs** | `neuro/meeg/mne/raw` · `neuro/meg/fif-override` (optional) |
| **Outputs** | `neuro/meeg/mne/raw` |
| **Container** | `brainlifemeeg/mne:1.12.1` |
| **Resources** | 1 CPUs · 20 GB memory |
| **Run it** | [doi.org/10.25663/brainlife.app.743](https://doi.org/10.25663/brainlife.app.743) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `fif` | `neuro/meeg/mne/raw` | yes | Continuous MEG/EEG data in MNE raw .fif format. |
| `channels` | `neuro/meg/fif-override` | no | channels.tsv file (at least 2 columns: name and status). Channels with status "bad" will be rejected. |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir` | `neuro/meeg/mne/raw` | Raw data with added annotation with marked channel x time segments. |

<details>
<summary><b>Parameters</b> (3)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bads` | string |  | Comma-separated list of channels. |
| `annotations` | string |  | Bad data segments described by their start, duration, description, and optionally the channels they apply to (all channels if omitted). |
| `reset_bads` | boolean | `false` | Reset bad channels before adding new ones specified here. |

</details>

<!-- brainlife-app:end -->

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.743](https://doi.org/10.25663/brainlife.app.743), choose `neuro/meeg/mne/raw`, `neuro/meg/fif-override` from your project, set the parameters and press **Execute**. The results are saved to your project as `neuro/meeg/mne/raw`.

### Locally

You need [Singularity/Apptainer](https://apptainer.org/) (the App runs in `brainlifemeeg/mne:1.12.1`), [`jq`](https://jqlang.github.io/jq/).

1. Clone this repository.
2. Create `config.json` with the paths to your inputs and the parameters:

   ```json
   {
       "raw": "/path/to/fif/raw",
       "channels": "/path/to/channels/channels",
       "bads": "",
       "annotations": "",
       "reset_bads": false
   }
   ```

3. Run `./main`.

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

## Local Testing

```bash
# Edit config.json to point "raw" (and optionally "channels") at real data, then:
python main.py
```

## Technical Details

- **Bad Channels**: Marked in `raw.info['bads']` and excluded from analysis in downstream apps
- **Annotations**: Stored in `raw.annotations` and can be used for segment-level quality control
- **Channel Validation**: Invalid channel names in both `bads` and `annotations` are validated against the input file
- **Preload**: Data is loaded and saved efficiently without full preload unless needed

## Citing

If you use this App, please cite it, the software it builds on and brainlife.io:

- Mark bad data. brainlife.io App. [doi:10.25663/brainlife.app.743](https://doi.org/10.25663/brainlife.app.743)
- Gramfort A, et al. MEG and EEG data analysis with MNE-Python. Front Neurosci 7:267 (2013). [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

- [Maximilien Chaumon](https://github.com/dnacombo), Paris Brain Institute

## Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io, which runs this App, is publicly funded by Wellcome, the U.S. National Institutes of Health and the U.S. National Science Foundation; acknowledging that support helps keep it running.</sub>

## License

See [LICENSE](LICENSE).
