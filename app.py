import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from math import ceil
from scipy import stats
from statsmodels.stats.power import TTestIndPower

st.set_page_config(page_title="Power & Sample Size Playground", layout="centered")
st.title("Power & Sample Size Playground")

st.markdown("""
Interactively size your study for:
- Two-sample **t-test** (means)
- **Proportion** estimation by margin of error
- **Multiple testing** false-positive compounding
- **Simulation** power for skewed outcomes
""")

st.header("1) Two-sample t-test (means)")
col1, col2 = st.columns(2)
with col1:
    delta = st.slider("Δ (expected mean difference)", 0.05, 1.0, 0.50, 0.05)
    sd = st.slider("σ (SD)", 0.4, 2.0, 1.2, 0.05)
with col2:
    alpha = st.slider("α (significance level)", 0.001, 0.10, 0.05, 0.001)
    target_power = st.slider("Power (1-β)", 0.50, 0.99, 0.80, 0.01)

d = delta / sd
analysis = TTestIndPower()
n_per_group = analysis.solve_power(effect_size=d, alpha=alpha, power=target_power, alternative='two-sided')
st.success(f"Cohen's d = {d:.3f} → Required N per group ≈ **{ceil(n_per_group)}** (total ≈ {2*ceil(n_per_group)})")

st.divider()
st.header("2) Proportion (MOE-based sizing)")
col3, col4 = st.columns(2)
with col3:
    p = st.slider("Expected proportion (p)", 0.05, 0.95, 0.50, 0.01)
    moe = st.slider("MOE (±)", 0.005, 0.15, 0.05, 0.005)
with col4:
    alpha2 = st.slider("α (for CI)", 0.001, 0.10, 0.05, 0.001, key="alpha2")
    finite_pop = st.number_input("Finite population size (0 = infinite)", min_value=0, value=0, step=1000)

z = stats.norm.ppf(1 - alpha2/2)
var = p*(1-p)
n = (z**2 * var) / (moe**2)
if finite_pop and finite_pop > 0:
    n = n / (1 + (n - 1)/finite_pop)  # finite population correction

st.info(f"Required n ≈ **{ceil(n)}** {'(with FPC)' if finite_pop else ''}")

st.divider()
st.header("3) Multiple testing: P(≥1 false positive)")
alpha3 = st.slider("α per test", 0.001, 0.10, 0.05, 0.001, key="alpha3")
max_m = st.slider("Max number of tests", 5, 200, 50, 5)
m = np.arange(1, max_m+1)
prob = 1 - (1 - alpha3)**m

fig, ax = plt.subplots(figsize=(6,4))
ax.plot(m, prob)
ax.set_xlabel("# tests (m)")
ax.set_ylabel("P(≥1 false positive)")
ax.set_title(f"Familywise error vs. m (α={alpha3:.3f})")
ax.grid(True)
st.pyplot(fig)

st.caption("Tip: Consider Holm–Bonferroni for FWER or Benjamini–Hochberg for FDR in large-scale testing.")

st.divider()
st.header("4) Simulation power for skewed outcomes (Welch t-test)")
col5, col6, col7 = st.columns(3)
with col5:
    mu1 = st.slider("μA (mean A)", 1.0, 20.0, 8.0, 0.5)
with col6:
    mu2 = st.slider("μB (mean B)", 1.0, 20.0, 10.0, 0.5)
with col7:
    sd_approx = st.slider("SD approx", 1.0, 12.0, 6.0, 0.5)

n_sim = st.slider("N per group", 20, 1000, 200, 20)
reps = st.slider("Sim reps", 500, 10000, 3000, 500)
alpha4 = st.slider("α", 0.001, 0.10, 0.05, 0.001, key="alpha4")

rng = np.random.default_rng(42)
k = (mu1**2) / max(sd_approx**2 - mu1, 1e-6)  # crude NB-like dispersion
successes = 0
for _ in range(reps):
    rate_a = rng.gamma(shape=max(k,1e-3), scale=mu1/max(k,1e-3), size=n_sim)
    rate_b = rng.gamma(shape=max(k,1e-3), scale=mu2/max(k,1e-3), size=n_sim)
    a = rng.poisson(rate_a)
    b = rng.poisson(rate_b)
    p = stats.ttest_ind(a, b, equal_var=False).pvalue
    successes += (p < alpha4)

power_est = successes / reps
st.success(f"Estimated power ≈ **{power_est:.2f}** (reps={reps}, N per group={n_sim})")
