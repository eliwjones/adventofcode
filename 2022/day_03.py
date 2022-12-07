import unittest


def dupe_sum(str_data):
    parsed_data = str_data.split('\n')

    item_priority = {chr(i): i - 96 for i in range(97, 123)}  # a - z
    item_priority |= {chr(i): i - 38 for i in range(65, 91)}  # A - Z

    dupe_sum = 0
    for rucksack in parsed_data:
        midpoint = len(rucksack) // 2
        comp_one = {*rucksack[:midpoint]}
        comp_two = {*rucksack[midpoint:]}

        intersection = comp_one & comp_two
        dupe_sum += sum(item_priority[item] for item in intersection)

    return dupe_sum


class Test(unittest.TestCase):
    def test_dupe_sum(self):
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
