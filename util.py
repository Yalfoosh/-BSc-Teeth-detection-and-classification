from typing import List


def endswith_in(string: str,
                suffices: List[str],
                start: int or List[int] = None,
                end: int or List[int] = None):
    assert isinstance(string, str)

    if isinstance(start, int) and isinstance(end, int):
        new_start, new_end = (list(), list())

        for i in range(0, len(suffices)):
            new_start.append(start)
            new_end.append(end)
    elif not (isinstance(start, list) and isinstance(end, list)):
        start = end = None

    for i, suffix in enumerate(suffices):
        assert isinstance(suffix, str)

        if not string.endswith(suffix=suffix, start=start[i], end=end[i]):
            return False

    return True
