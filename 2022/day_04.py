import unittest


def contained_ranges(str_data):
    parsed_data = str_data.replace('-', '\n').replace(',', '\n').split('\n')

    pairs = [int(item) for item in parsed_data]
    contained = []
    for i in range(0, len(pairs), 4):
        range_one = set(range(pairs[i], pairs[i + 1] + 1))
        range_two = set(range(pairs[i + 2], pairs[i + 3] + 1))

        intersection = range_one & range_two
        if len(intersection) < len(range_one) and len(intersection) < len(range_two):
            continue

        contained.append([range_one, range_two])

    return len(contained)


class Test(unittest.TestCase):
    def test_contained_ranges(self):
        data = ['2-4,6-8', '2-3,4-5', '5-7,7-9', '2-8,3-7', '6-6,4-6', '2-6,4-8']
        str_data = '\n'.join(map(str, data))

        contained = contained_ranges(str_data)

        self.assertEqual(contained, 2, f"Expected contained ranges to be 2 but got {contained}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
