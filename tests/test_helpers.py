from src.helpers import familywise_fp_prob

def test_familywise_increases_with_m():
    assert familywise_fp_prob(20, 0.05) > familywise_fp_prob(1, 0.05)
