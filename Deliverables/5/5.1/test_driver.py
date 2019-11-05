# Import nonlocal dependencies.
import json, os, sys, typing

# Import local dependencies.
import constants
from point import Point
from board import Board
import rule_checker as rc


def main():
    # Parse the text input into a list of JSON elements.
    txt = sys.stdin.read().rstrip()
    json_elements = txt2json(txt)

    # Handle each input and collect the results.
    results = []
    for json_element in json_elements:
        if len(json_element) == constants.BOARD_ROW_LENGTH:
            b = Board(json_element)
            results.append(rc.get_scores(b))
        else:
            stone, move_json = json_element
            if move_json == PASS:
                move = PASS
            else:
                str_point, json_boards = move_json
                point = Point.from_str(str_point)
                boards = [Board(json_board) for json_board in json_boards]
                move = (point, boards)
            results.append(rc.is_move_legal(stone, move))
    json.dump(results, sys.stdout)


def txt2json(content: str) -> list:
    decoder = json.JSONDecoder()
    json_elements = []
    while content != '':
        content = content.strip()
        element, idx = decoder.raw_decode(content)
        json_elements.append(element)
        content = content[idx:]

    return json_elements


if __name__ == "__main__":
    main()
