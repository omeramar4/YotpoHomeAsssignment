from typing import List


def sublist(lst1: List[str], lst2: List[str]) -> bool:
    ls1 = [element for element in lst1 if element in lst2]
    ls2 = [element for element in lst2 if element in lst1]
    return ls1 == ls2


def number_of_appeared_elements(search_list: List[str], target_list: List[str]) -> int:
    return sum([1 if s in target_list else 0 for s in search_list])


def get_lines_from_text_file(path_to_file: str) -> List[str]:
    try:
        with open(path_to_file, 'r') as f:
            lines = f.read().splitlines()
    except FileNotFoundError as e:
        raise e

    return lines
