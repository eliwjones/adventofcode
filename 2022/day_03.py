import unittest


ITEM_PRIORITY = {chr(i): i - 96 for i in range(97, 123)}  # a - z
ITEM_PRIORITY |= {chr(i): i - 38 for i in range(65, 91)}  # A - Z


def dupe_sum(str_data):
    parsed_data = str_data.split('\n')

    dupe_sum = 0
    for rucksack in parsed_data:
        midpoint = len(rucksack) // 2
        comp_one = {*rucksack[:midpoint]}
        comp_two = {*rucksack[midpoint:]}

        intersection = comp_one & comp_two
        dupe_sum += sum(ITEM_PRIORITY[item] for item in intersection)

    return dupe_sum


def badge_sum(str_data):
    parsed_data = str_data.split('\n')

    badge_sum = 0
    for i in range(2, len(parsed_data), 3):
        pack_one = {*parsed_data[i - 2]}
        pack_two = {*parsed_data[i - 1]}
        pack_three = {*parsed_data[i]}

        intersection = pack_one & pack_two & pack_three
        badge_sum += ITEM_PRIORITY[intersection.pop()]

    return badge_sum


class Test(unittest.TestCase):
    def test_dupe_and_badge_sum(self):
        data = [
            'vJrwpWtwJgWrhcsFMMfFFhFp',
            'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
            'PmmdzqPrVvPwwTWBwg',
            'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
            'ttgJtRGJQctTZtZT',
            'CrZsJsPPZsGzwwsLwLmpwMDw',
        ]
        str_data = '\n'.join(map(str, data))

        total = dupe_sum(str_data)

        self.assertEqual(total, 157, f"Expected your total to be 157 but got {total}.")

        total = badge_sum(str_data)

        self.assertEqual(total, 70, f"Expected badge sum to be 70 but got {total}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
