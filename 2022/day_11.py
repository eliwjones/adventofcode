import unittest

from operator import mul, add
from functools import partial


def square(x):
    return mul(x, x)


def mod(m, x):
    return x % m == 0


def parse_monkey_data(str_data):
    lines = str_data.split('\n\n')
    ops = {'*': mul, '+': add}

    monkeys = {}
    modulus_product = 1
    for line in lines:
        data = line.split('\n')
        data = [datum.strip() for datum in data]

        _id = data[0].lower()[:-1]
        items = data[1].replace('Starting items: ', '').replace(' ', '').split(',')

        op = data[2].replace('Operation: new = old ', '')
        op_num = op.split(' ')[-1]
        op_num = 'old' if op_num == 'old' else int(op_num)

        test_modulus = int(data[3].replace('Test: divisible by ', ''))
        dest = {'True': data[4].split(' throw to ')[-1], 'False': data[5].split(' throw to ')[-1]}

        monkeys[_id] = {
            'items': [int(item) for item in items],
            'op': partial(ops[op[0]], op_num) if op_num != 'old' else partial(square),
            'test': partial(mod, test_modulus),
            'dest': dest,
        }

        modulus_product *= test_modulus

    return monkeys, modulus_product


def monkey_play_score(monkeys, modulus_product, rounds, worry_divisor):
    counter = {key: 0 for key in monkeys.keys()}
    while rounds:
        for idx in range(len(monkeys.keys())):
            key = f"monkey {idx}"
            while monkeys[key]['items']:
                item = monkeys[key]['items'].pop(0)

                new_item = monkeys[key]['op'](item) // worry_divisor
                new_item = new_item % modulus_product

                test = monkeys[key]['test'](new_item)
                dest_key = monkeys[key]['dest'][str(test)]
                counter[key] += 1

                monkeys[dest_key]['items'].append(new_item)

        rounds -= 1

    top = []
    while len(top) != 2:
        m = max(counter.values())
        top.append(m)
        counter = {key: value for key, value in counter.items() if value != m}

    return top[0] * top[1]


class Test(unittest.TestCase):
    def test_overlapping_ranges(self):
        str_data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

        monkeys, modulus_product = parse_monkey_data(str_data)
        score = monkey_play_score(monkeys, modulus_product, rounds=20, worry_divisor=3)
        expected = 10605

        self.assertEqual(score, expected, f"Expected sum of {expected} but got {score}.")

        monkeys, modulus_product = parse_monkey_data(str_data)
        score = monkey_play_score(monkeys, modulus_product, rounds=10000, worry_divisor=1)
        expected = 2713310158

        self.assertEqual(score, expected, f"Expected sum of {expected} but got {score}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
