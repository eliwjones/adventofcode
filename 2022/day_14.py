import unittest

ROCK = '#'
SAND = 'o'
AIR = '.'


def simulate(cave, sand_source):
    sand_moves = ((0, 1), (-1, 1), (1, 1))

    while True:
        pos = list(sand_source)

        while True:
            moved = False
            for x, y in sand_moves:
                i = pos[1] + y
                j = pos[0] + x

                if not (0 <= i < len(cave)) or not (0 <= j < len(cave[i])):
                    return cave

                if cave[i][j] != AIR:
                    continue

                pos = [j, i]
                moved = True

                break

            if not moved:
                cave[pos[1]][pos[0]] = SAND

                break

    return cave


def build_cave(paths):
    max_x = max([paths[i][j][0] for i, j in ijs(paths)])
    max_y = max([paths[i][j][1] for i, j in ijs(paths)])

    cave = [[AIR for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for path, i in [(path, i) for path in paths for i in range(len(path) - 1)]:
        one, two = sort_points(path[i], path[i + 1])

        if one[0] != two[0]:
            y = one[1]
            for x in range(one[0], two[0] + 1):
                cave[y][x] = ROCK

        if one[1] != two[1]:
            x = one[0]
            for y in range(one[1], two[1] + 1):
                cave[y][x] = ROCK

    return cave


def count_things(cave, thing):
    things = [(i, j) for i, j in ijs(cave) if cave[i][j] == thing]

    return len(things)


def ijs(matrix):
    return [(i, j) for i in range(len(matrix)) for j in range(len(matrix[i]))]


def parse_path_data(str_data):
    data = str_data.split('\n')
    paths = [d.split(' -> ') for d in data]

    for i, j in ijs(paths):
        paths[i][j] = tuple(map(int, paths[i][j].split(',')))

    return paths


def print_cave(cave):
    print('\n')
    for row in cave:
        print(''.join(row[-50:]))


def sort_points(one, two):
    if one[0] < two[0]:
        return one, two
    elif one[0] > two[0]:
        return two, one
    elif one[1] < two[1]:
        return one, two
    elif one[1] > two[1]:
        return two, one

    return one, two


class Test(unittest.TestCase):
    def test_simulate(self):
        data = ['498,4 -> 498,6 -> 496,6', '503,4 -> 502,4 -> 502,9 -> 494,9']
        str_data = '\n'.join(data)

        paths = parse_path_data(str_data)
        cave = build_cave(paths)

        print_cave(cave)
        cave = simulate(cave=cave, sand_source=(500, 0))
        print_cave(cave)

        sand_count = count_things(cave=cave, thing=SAND)
        expected = 24

        self.assertEqual(sand_count, expected, f"Expected to see {expected} grains of sand but got {sand_count}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
