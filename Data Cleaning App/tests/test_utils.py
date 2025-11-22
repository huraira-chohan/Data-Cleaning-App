from modules.utils import text_to_number


def test_simple_numbers():
    assert text_to_number('twenty') == 20
    assert text_to_number('twenty-two') == 22
    assert text_to_number('80') == 80
    assert text_to_number('eighty') == 80
    assert text_to_number(None) is None
    assert text_to_number('unknown') is None
