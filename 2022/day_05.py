import unittest


def top_crates(str_data):
    split_data = str_data.split('\n')

    empty_index = split_data.index('')

    crate_data = split_data[:empty_index]
    crates = parse_crates(crate_data)

    move_data = split_data[empty_index + 1 :]
    moves = parse_moves(move_data)
    for count, start, dest in moves:
        clump = list(reversed(crates[str(start)][-1 * count :]))
        crates[str(start)] = crates[str(start)][: -1 * count]
        crates[str(dest)].extend(clump)

    return ''.join([column[-1] for column in crates.values()])


def parse_crates(crate_data):
    headers = crate_data[-1]
    header_dict = {header: headers.index(header) for header in headers.split()}
    crate_lines = crate_data[:-1]

    crate_dict = {column: [] for column in header_dict}
    for line in crate_lines:
        for column, index in header_dict.items():
            crate = line[index].strip()
            if not crate:
                continue

            crate_dict[column].insert(0, crate)

    return crate_dict


def parse_moves(move_data):
    moves = []
    for line in move_data:
        move = [int(part) for part in line.split(' ') if part.isdigit()]
        if not move:
            continue

        moves.append(move)

    return moves


class Test(unittest.TestCase):
    def test_top_crates(self):
        str_data = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

        tops = top_crates(str_data)
        expected = 'CMZ'

        self.assertEqual(tops, expected, f"Expected top_crates to be {expected} but got {tops}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
