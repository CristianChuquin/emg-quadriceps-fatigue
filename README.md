# EMG-Based Detection and Classification of Quadriceps Muscular Fatigue

Integrative Project · Biomechanics of Gait · Universidad Yachay Tech · October 2026

Authors: Carolina Córdoba, Estefanía Paucar, Cristian Chuquín
Tutor: Kevin Landázuri, MSc.

This repository contains the code, processed feature tables and figures behind the report. It classifies windows of surface EMG from the rectus femoris into three fatigue levels (low, medium, high) with a Random Forest, compared against a majority-class baseline and a logistic regression on RMS and MDF.

## Repository map

| Folder or file | Content | Output |
|---|---|---|
| `pipeline_completo.ipynb` | **Main notebook, end to end**: raw sEMG → band-pass 20–450 Hz + 60 Hz notch → 250 ms windows → RMS, MAV, WL, MDF, MNF → bilateral dataset → audit → z-score / GroupKFold tests by real subject → baselines (leave-one-subject-out) → exclusions, smoothing and interpolation → Random Forest → per-subject F1, feature importance → saved model → inference on a new signal | All tables and figures of Sections 3–7 (GroupKFold by real subject: Table 11) |
| `modelo.ipynb` | Model-only notebook that starts from the processed feature tables. Exports `resultados_modelo_fatiga.csv` | Table 8, class distribution |
| `resultados_modelo_fatiga.csv` | True label and Random Forest prediction for each of the 17,860 test windows | Accuracy 0.755, macro-F1 0.755 (Table 8) |
| `data/raw/` | Where the raw dataset goes (not committed; see its README) | Input |
| `data/test/` | Where the instructor's test signals go for the inference step (not committed) | Input |
| `Modificacion_dataset/` | Feature tables per window: clean, bilateral, smoothed and interpolated versions | Input to `modelo.ipynb` |
| `graficas/` | Confusion matrix, per-subject F1, feature importance, triplet comparison, class distribution | Figures of Section 7 |
| `graficas_todos_los_sujetos/` | Feature trajectories for every participant, recording and leg (`sujetoN_RM_lado.png`) | Per-participant trajectories |
| `prueba/` | Example of a new signal and its extracted features | Inference on a signal the model has not seen |
| `signal_quality/` | Signal-quality and exclusion scripts, per-recording quality table | Sections 2.3–2.4 and Figure 1 |

## How to run (clean environment)

```bash
git clone https://github.com/CristianChuquin/emg-quadriceps-fatigue.git
cd emg-quadriceps-fatigue
pip install -r requirements.txt
# put the raw dataset in data/raw/sujeto1 ... data/raw/sujeto15 (see data/raw/README.md)
# put the test signals in data/test/ (see data/test/README.md)
jupyter nbconvert --to notebook --execute pipeline_completo.ipynb --output pipeline_completo.ipynb
```

- Every path in `pipeline_completo.ipynb` is relative to the repository. The notebook creates `data/processed/`, `graficas/` and `resultados/` itself.
- In Google Colab, the first cell mounts Drive and links `data/raw` to the `EMG - RAW data` folder automatically.
- The trained model (`modelo_fatiga_rf.pkl`, about 300 MB) is not committed because it exceeds GitHub's file size limit; the notebook writes it to `resultados/`.
- The `signal_quality/` scripts expect the raw dataset at `emg/raw/<participant>/` and are run from the repository root.

## Data

- The raw EMG dataset is not committed. It was distributed by the course instructor.
- No participant names are stored in this repository: participants are labelled `sujeto1`–`sujeto15`, and the quality scripts use S01–S15 (alphabetical order of the dataset folders).
- Sampling rate: 1000 Hz. Columns of each raw CSV: `Relative_Time_s`, `ADC_Value`, `Voltage_mV`.