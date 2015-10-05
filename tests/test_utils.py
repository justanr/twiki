from twiki.utils import encode_term


def test_encode_term_with_no_space():
    assert encode_term('nospace') == 'nospace'


def test_encode_term_with_space():
    assert encode_term('has space') == 'has+space'


def test_encode_term_with_surrounding_space():
    assert encode_term('  has space  ') == 'has+space'


def test_encode_term_with_existing_plus():
    assert encode_term('has+plus') == 'has%2Bplus'
