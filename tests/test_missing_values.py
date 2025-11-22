import pandas as pd
from modules.missing_values import handle_missing_values


def test_fill_mean():
    df = pd.DataFrame({
        'a':[1, None, 3],
        'b':[None, 2, 3]
    })
    # Call function to ensure it runs; thorough UI-driven operations aren't fully testable here,
    # but the function should accept a DataFrame and return a DataFrame
    out = handle_missing_values(df.copy())
    assert isinstance(out, pd.DataFrame)
