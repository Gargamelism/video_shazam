import Levenshtein


def get_distance(str1: str, str2: str) -> int:
    distance = Levenshtein.distance(str1, str2)
    return distance
