import re

# Small utility to convert textual numbers to integers for tests and reuse
TEXT_TO_NUM = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
    'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
    'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13,
    'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
    'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'thirty': 30,
    'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70,
    'eighty': 80, 'ninety': 90, 'hundred': 100
}


def text_to_number(s: str):
    """Attempt to convert a small textual number to an int.
    Supports simple words and hyphenated forms like "twenty-two".
    Returns int or None if not convertible.
    """
    if s is None:
        return None
    s = str(s).strip().lower()
    if not s:
        return None
    # direct digit
    if re.fullmatch(r"[-+]?\d+", s):
        try:
            return int(s)
        except:
            return None

    # Clean punctuation and words like 'and'
    s_clean = re.sub(r"[,()]", "", s)
    s_clean = s_clean.replace(" and ", " ")
    s_clean = re.sub(r"[^a-z0-9\s-]", "", s_clean)

    # direct mapping
    if s_clean in TEXT_TO_NUM:
        return TEXT_TO_NUM[s_clean]

    # tokenise on spaces or hyphens and handle scale word 'hundred'
    parts = re.split(r"[-\s]+", s_clean)
    total = 0
    current = 0
    for p in parts:
        if not p:
            continue
        if p.isdigit():
            current += int(p)
            continue
        if p in TEXT_TO_NUM:
            val = TEXT_TO_NUM[p]
            if val == 100:
                # scale current by 100 (e.g., 'one hundred twenty')
                if current == 0:
                    current = 100
                else:
                    current = current * 100
            else:
                current += val
        else:
            return None
    total += current
    return total if total != 0 else None
