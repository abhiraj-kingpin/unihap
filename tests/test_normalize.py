from unihap.layers.l7_normalize.normalizer import AttributeNormalizer


def test_normalize_fractions():
    norm = AttributeNormalizer()
    assert norm.normalize_string("1/2 inch pipe") == "0.5 in pipe"
    assert norm.normalize_string("3/4 gpm flow") == "0.75 GPM flow"
    assert norm.normalize_string('1-1/4" fitting') == "1.25 in fitting"


def test_normalize_uom():
    norm = AttributeNormalizer()
    assert norm.normalize_string("10 gpm") == "10 GPM"
    assert norm.normalize_string("60 psi") == "60 PSI"
    assert norm.normalize_string("5 lbs") == "5 lb"
