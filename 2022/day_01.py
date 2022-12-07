import unittest


def get_max_elf(str_data):
    elves = get_elf_calories(str_data)
    max_index = elves.index(max(elves))

    return max_index, elves[max_index]


def get_top_elves(str_data, count):
    elves = get_elf_calories(str_data)

    result = []
    while len(result) != count and elves:
        i = elves.index(max(elves))
        result.append(elves.pop(i))

    return result


def get_elf_calories(str_data):
    parsed_data = str_data.split('\n')

    elves = [0]
    index = 0
    while parsed_data:
        val = parsed_data.pop(0)

        if not val:
            index += 1
            elves.append(0)

            continue

        val = int(val)
        elves[index] += val

    return elves


class Test(unittest.TestCase):
    def test_get_max_elf(self):
        data = [1000, 2000, 3000, '', 4000, '', 5000, 6000, '', 7000, 8000, 9000, '', 10000]
        str_data = '\n'.join(map(str, data))

        i, total_calories = get_max_elf(str_data)

        self.assertEqual(i, 3, f"Expected max elf index to be 3 but got {i}.")
        self.assertEqual(total_calories, 24000, f"Expected total calories to be 24000 but got {total_calories}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
