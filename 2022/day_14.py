import unittest

ROCK = '#'
SAND = 'o'


def simulate(cave, sand_source):
    """
    Simulate falling sand until grains begin falling past
    the "floor".
    """

    """
      If sand gets to edge of cave, simulation is over
      next move would fall off.
    """
    print('\n')
    for row in cave:
        print(''.join(row[-50:]))

    while True:
        print(sand_source)

        break

    return cave


def build_cave(paths):
    max_x = max([paths[i][j][0] for i, j in ijs(paths)])
    max_y = max([paths[i][j][1] for i, j in ijs(paths)])

    cave = [['.' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for path, i in [(path, i) for path in paths for i in range(len(path) - 1)]:
        one, two = sort_points(path[i], path[i + 1])

        if one[0] != two[0]:
            y = one[1]
            for x in range(one[0], two[0] + 1):
                cave[y][x] = ROCK

        if one[1] != two[1]:
            x = one[0]
            for y in range(one[1], two[1] + 1):
                print(f"x: {x}, y: {y}, len(cave[0]): {len(cave[0])}, len(cave): {len(cave)}")
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
        str_data = '\n'.join(map(str, data))

        print()

        paths = parse_path_data(str_data)
        cave = simulate(cave=build_cave(paths), sand_source=(500, 0))
        sand_count = count_things(cave=cave, thing='o')
        expected = 24

        self.assertEqual(sand_count, expected, f"Expected to see {expected} grains of sand but got {sand_count}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
