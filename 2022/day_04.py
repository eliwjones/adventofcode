import unittest


def overlapping_ranges(str_data):
    parsed_data = str_data.replace('-', '\n').replace(',', '\n').split('\n')

    pairs = [int(item) for item in parsed_data]
    overlapping = []
    for i in range(0, len(pairs), 4):
        range_one = set(range(pairs[i], pairs[i + 1] + 1))
        range_two = set(range(pairs[i + 2], pairs[i + 3] + 1))

        intersection = range_one & range_two
        if not intersection:
            continue

        overlapping.append([range_one, range_two])

    return len(overlapping)


class Test(unittest.TestCase):
    def test_overlapping_ranges(self):
        data = ['2-4,6-8', '2-3,4-5', '5-7,7-9', '2-8,3-7', '6-6,4-6', '2-6,4-8']
        str_data = '\n'.join(map(str, data))

        overlapping = overlapping_ranges(str_data)

        self.assertEqual(overlapping, 4, f"Expected overlapping ranges to be 4 but got {overlapping}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
