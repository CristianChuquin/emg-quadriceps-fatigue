# EMG-Based Detection and Classification of Quadriceps Muscular Fatigue

Integrative Project · Biomechanics of Gait · Universidad Yachay Tech · October 2026

Authors: Carolina Córdoba, Estefanía Paucar, Cristian Chuquín
Tutor: Kevin Landázuri, MSc.

This repository contains the code, processed feature tables and figures behind the report. It classifies windows of surface EMG from the rectus femoris into three fatigue levels (low, medium, high) with a Random Forest, compared against a majority-class baseline and a logistic regression on RMS and MDF.

## Repository map

| Folder or file | Content | Output |
|---|---|---|
| `modelo.ipynb` | Full pipeline: baselines, dataset variants, Random Forest, evaluation, inference on a new signal | Results tables and figures of Sections 6–7 |
| `Modificacion_dataset/` | Feature tables per window: clean, bilateral, smoothed and interpolated versions | Input to `modelo.ipynb` |
| `graficas/` | Confusion matrix, per-subject F1, feature importance, triplet comparison | Figures of Section 7 |
| `graficas_todos_los_sujetos/` | Feature trajectories for every participant, recording and leg (`sujetoN_RM_lado.png`) | Per-participant trajectories |
| `prueba/` | Example of a new signal and its extracted features | Inference on a signal the model has not seen |
| `signal_quality/` | Signal-quality and exclusion scripts, per-recording quality table | Sections 2.3–2.4 and Figure 1 |

## How to run

1. Install the dependencies: `pip install -r requirements.txt`.
2. Open `modelo.ipynb` and run the cells in order. The notebook reads the CSV files by name, so place the files of `Modificacion_dataset/` and `prueba/` in the working directory (or adjust the paths).
3. The trained model (`modelo_fatiga_rf.pkl`, about 300 MB) is not committed because it exceeds GitHub's file size limit. The notebook regenerates it in the Random Forest section.
4. The `signal_quality/` scripts expect the raw dataset at `emg/raw/<participant>/` and are run from the repository root.

## Data

- The raw EMG dataset is not committed. It was distributed by the course instructor.
- No participant names are stored in this repository: the notebook labels participants `sujeto1`–`sujeto15`, and the quality scripts use S01–S15 (alphabetical order of the dataset folders).
- Sampling rate: 1000 Hz.
