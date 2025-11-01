from src.helpers import n_for_two_sample_means, n_for_proportion_moe, familywise_fp_prob

print("Two-sample means (Δ=0.5, σ=1.2, α=0.05, power=0.8): N/group =", n_for_two_sample_means(0.5, 1.2))
print("Proportion MOE (p=0.5, MOE=±0.03, α=0.05): N =", n_for_proportion_moe(0.5, 0.03))
print("FWER for m=20, α=0.05:", round(familywise_fp_prob(20, 0.05), 4))
