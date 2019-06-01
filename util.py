from typing import Iterable, Dict, List, Tuple


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


def intersection_over_union(box_1: Tuple[int, int, int, int], box_2: Tuple[int, int, int, int]) -> float:
    return 1.0


def find_strongest_correlation(box: Tuple[int, int, int, int], boxes: Iterable[Tuple[int, int, int, int]]):
    correlations = list()

    for polled_box in boxes:
        correlations.append((polled_box, intersection_over_union(box, polled_box)))

    correlations.sort(key=lambda x: x[1])
    return correlations.reverse()[0]


def error_from_match(matches: Dict[str, float]) -> float:
    error = 0.0

    for label in matches:
        error += matches[label]

    return error / len(matches)
