# Power & Sample Size Playground

Interactive tools and helpers for **power analysis** and **survey sample size estimation** geared toward quantitative UX research.

## What's inside

- **Streamlit app** (`app.py`) — one-page interactive playground.
- **Jupyter notebook** (`notebooks/power_sample_playground.ipynb`) — widgets for a priori sizing, MOE, multiple testing visualization, and simulation-based power.
- **Helper functions** (`src/helpers.py`) — drop-in utilities for sizing and false-positive calculations.
- **Examples** (`examples/`) — quick scripts showing how to call helpers from Python.

## Quickstart

### 1) Clone and install
```bash
git clone https://github.com/your-username/power-sample-playground.git
cd power-sample-playground
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

### 2) Run the Streamlit app
```bash
streamlit run app.py
```

### 3) Use the Jupyter notebook
```bash
jupyter notebook notebooks/power_sample_playground.ipynb
```

---

## Contents

- `app.py` — Streamlit UI covering:
  - Two-sample t-test power (a priori sizing)
  - Proportion MOE-based sizing (with optional finite-population correction)
  - Multiple testing false-positive compounding
  - Simulation-based power for skewed outcomes

- `notebooks/power_sample_playground.ipynb` — same concepts with ipywidgets.

- `src/helpers.py` — programmatic API:
  - `n_for_two_sample_means(delta, sd, alpha=0.05, power=0.8)`
  - `n_for_proportion_moe(p=0.5, moe=0.05, alpha=0.05, finite_pop=None)`
  - `familywise_fp_prob(m, alpha=0.05)`
  - `benjamini_hochberg(pvals, alpha=0.05)`

- `examples/usage_two_sample.py` — quick demo of helper functions.

---

## Notes

- The simulation examples use a simple Gamma–Poisson mixture to approximate overdispersed, skewed counts, then apply Welch's t-test as a pragmatic check. For production-grade analysis, consider GLMs or mixed models and tailor the simulation to your metric and data-generating process.
- For clustered survey designs, extend simulation to include intra-class correlation (ICC) and mixed-effects models.
- If p (for proportions) is unknown, `p=0.5` is a conservative variance assumption.

## License

MIT — see `LICENSE`.

