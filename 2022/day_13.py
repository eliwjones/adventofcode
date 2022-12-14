import json
import unittest


def ordered_group_indices(data):
    ordered_groups = []

    for i in range(0, len(data), 2):
        left = data[i]
        right = data[i + 1]

        comp = compare(left, right)
        if comp == -1:
            ordered_groups.append(i // 2 + 1)

    return ordered_groups


def compare(left, right):
    if left == right:
        return 0

    if right == []:
        return 1
    elif left == []:
        return -1

    if type(left) == type(right) == int:
        if left < right:
            return -1
        elif left > right:
            return 1
        return 0

    if type(left) is int:
        left = [left]

    if type(right) is int:
        right = [right]

    result = compare(left[0], right[0])
    if result:
        return result

    return compare(left[1:], right[1:])


def parse_str_data(str_data):
    parsed_data = str_data.split()
    data = [json.loads(d) for d in parsed_data]

    return data


class Test(unittest.TestCase):
    def test_ordered_group_indices(self):
        data = [
            '[1,1,3,1,1]',
            '[1,1,5,1,1]',
            '',
            '[[1],[2,3,4]]',
            '[[1],4]',
            '',
            '[9]',
            '[[8,7,6]]',
            '',
            '[[4,4],4,4]',
            '[[4,4],4,4,4]',
            '',
            '[7,7,7,7]',
            '[7,7,7]',
            '',
            '[]',
            '[3]',
            '',
            '[[[]]]',
            '[[]]',
            '',
            '[1,[2,[3,[4,[5,6,7]]]],8,9]',
            '[1,[2,[3,[4,[5,6,0]]]],8,9]',
        ]
        str_data = '\n'.join(data)

        ordered_groups = ordered_group_indices(parse_str_data(str_data))
        s = sum(ordered_groups)
        expected = 13

        self.assertEqual(s, expected, f"Expected the sum of ordered group indices to be {expected} but got {s}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
