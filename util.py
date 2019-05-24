from typing import List


def endswith_in(string: str,
                suffices: List[str],
                start: int or List[int] = None,
                end: int or List[int] = None):
    assert isinstance(string, str)

    new_start = start
    new_end = end

    if isinstance(start, int) and isinstance(end, int):
        new_start, new_end = (list(), list())

        for i in range(0, len(suffices)):
            new_start.append(start)
            new_end.append(end)
    elif not (isinstance(start, list) and isinstance(end, list)):
        new_start, new_end = (list(), list())

        for i in range(0, len(suffices)):
            new_start.append(None)
            new_end.append(None)

    start = new_start
    end = new_end

    for i, suffix in enumerate(suffices):
        assert isinstance(suffix, str)

        if string.endswith(suffix, start[i], end[i]):
            return True

    return False
