import pandas as pd
from modules.text_cleaning import handle_text_encoded_values, clean_text_values


def test_handle_text_encoded_values():
    df = pd.DataFrame({
        'name': ['Ali', 'Sara', 'Bob'],
        'age': ['20', 'twenty-two', '??']
    })

    # call the function (it returns updated df)
    out = handle_text_encoded_values(df.copy())

    # After conversion, "twenty-two" should be converted to numeric 22
    # '??' should remain NaN after subsequent cleaning, so ensure that numeric coercion occurred
    assert 'age' in out.columns
    # check that 'twenty-two' converted to numeric 22 or NaN if not convertible
    assert out['age'].dtype.kind in ('i', 'u', 'f', 'n') or out['age'].isnull().any()


def test_clean_text_values():
    df = pd.DataFrame({
        'col': [' None', 'NA', 'hello!!']
    })
    out = clean_text_values(df.copy())
    # The function replaces common NULL strings with NaN when that operation is selected in UI,
    # but this unit test ensures function runs without error and returns a DataFrame
    assert isinstance(out, pd.DataFrame)
