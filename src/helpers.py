from math import ceil
import numpy as np
from scipy import stats
from statsmodels.stats.power import TTestIndPower

def n_for_two_sample_means(delta, sd, alpha=0.05, power=0.8):
    """A priori N per group for a two-sample t-test (two-sided)."""
    d = delta / sd
    n = TTestIndPower().solve_power(effect_size=d, alpha=alpha, power=power)
    return ceil(n)

def n_for_proportion_moe(p=0.5, moe=0.05, alpha=0.05, finite_pop=None):
    """Descriptive sizing by MOE; worst-case if p=0.5. Returns total n."""
    z = stats.norm.ppf(1 - alpha/2)
    n = (z**2 * p*(1-p)) / (moe**2)
    if finite_pop and finite_pop > 0:
        n = n / (1 + (n - 1)/finite_pop)
    return ceil(n)

def familywise_fp_prob(m, alpha=0.05):
    """P(≥1 false positive) for m independent tests."""
    return 1 - (1 - alpha)**m

def benjamini_hochberg(pvals, alpha=0.05):
    """Boolean mask of p-values significant under BH-FDR."""
    pvals = np.asarray(pvals)
    m = len(pvals)
    order = np.argsort(pvals)
    ranked = pvals[order]
    thresholds = alpha * (np.arange(1, m+1) / m)
    is_sig_sorted = ranked <= thresholds
    if not is_sig_sorted.any():
        return np.zeros_like(pvals, dtype=bool)
    k = np.where(is_sig_sorted)[0].max()
    sig_mask_sorted = np.zeros_like(pvals, dtype=bool)
    sig_mask_sorted[:k+1] = True
    sig_mask = np.zeros_like(pvals, dtype=bool)
    sig_mask[order] = sig_mask_sorted
    return sig_mask
