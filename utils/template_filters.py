import re


def term_label(term):
    match = re.match(r"[a-zA-Z]*(\d+)/B(\d+)", term)
    if not match:
        return term

    year = int(match.group(1))
    block = match.group(2)
    full_year = 2000 + year if year < 100 else year
    return f"{full_year} · Block {block}"
