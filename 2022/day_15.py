import unittest

from collections import defaultdict


def draw_map(sensor_data):
    m = defaultdict(dict)

    for sensor, beacon in sensor_data:
        min_dist = manhattan(sensor, beacon)

        clear_net = net(sensor, min_dist)

        for x, y in clear_net:
            m[x][y] = '#'

        m[sensor[1]][sensor[0]] = 'S'
        m[beacon[1]][beacon[0]] = 'B'

    return m


def manhattan(one, two):
    d = abs(one[0] - two[0]) + abs(one[1] - two[1])

    return d


def net(center, dist):
    points = [(x, y) for x in range(dist + 1) for y in range(dist + 1) if 0 < x + y <= dist]

    return [(center[0] + x, center[1] + y) for x, y in points]


def parse_sensor_data(str_data):
    data = str_data.replace('Sensor at x=', '').replace(' closest beacon is at x=', '').replace(' y=', '')

    sensor_data = []
    for d in data.split('\n'):
        sensor, beacon = d.split(':')

        sensor = tuple(map(int, sensor.split(',')))
        beacon = tuple(map(int, beacon.split(',')))

        sensor_data.append([sensor, beacon])

    return sensor_data


class Test(unittest.TestCase):
    def test_overlapping_ranges(self):
        data = [
            'Sensor at x=2, y=18: closest beacon is at x=-2, y=15',
            'Sensor at x=9, y=16: closest beacon is at x=10, y=16',
            'Sensor at x=13, y=2: closest beacon is at x=15, y=3',
            'Sensor at x=12, y=14: closest beacon is at x=10, y=16',
            'Sensor at x=10, y=20: closest beacon is at x=10, y=16',
            'Sensor at x=14, y=17: closest beacon is at x=10, y=16',
            'Sensor at x=8, y=7: closest beacon is at x=2, y=10',
            'Sensor at x=2, y=0: closest beacon is at x=2, y=10',
            'Sensor at x=0, y=11: closest beacon is at x=2, y=10',
            'Sensor at x=20, y=14: closest beacon is at x=25, y=17',
            'Sensor at x=17, y=20: closest beacon is at x=21, y=22',
            'Sensor at x=16, y=7: closest beacon is at x=15, y=3',
            'Sensor at x=14, y=3: closest beacon is at x=15, y=3',
            'Sensor at x=20, y=1: closest beacon is at x=15, y=3',
        ]

        str_data = '\n'.join(data)

        sensor_data = parse_sensor_data(str_data)
        m = draw_map(sensor_data)

        print(f"\ny: {9}, x's: {m[9].values()}")
        print(f"\ny: {10}, x's: {m[10].values()}")
        print(f"\ny: {11}, x's: {m[11].values()}")

        count = sum(1 for x in m[10].keys() if m[10][x] == '#')
        expected = 26

        self.assertEqual(count, expected, f"Expected {expected} no gos but got {count}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
