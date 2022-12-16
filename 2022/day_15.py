import unittest

from collections import defaultdict


def build_sensors_and_beacons(sensor_data):
    sensors = {}
    beacons = {}

    max_xy = [0, 0]
    min_xy = [0, 0]
    for sensor, beacon in sensor_data:
        distance = manhattan(sensor, beacon)

        sensors[sensor] = {'y_range': [sensor[1] - distance, sensor[1] + distance], 'intersects': intersects(sensor, distance)}

        beacons[beacon] = True

        for i in range(2):
            max_xy[i] = max(sensor[i] + distance, beacon[i], max_xy[i])
            min_xy[i] = min(sensor[i] - distance, beacon[i], min_xy[i])

    return sensors, beacons, max_xy, min_xy


def get_y_count(sensors, beacons, y, min_x, max_x):
    viable_sensors = []
    for sensor in sensors.values():
        if sensor['y_range'][0] <= y <= sensor['y_range'][1]:
            viable_sensors.append(sensor)

    count = 0
    for x in range(min_x, max_x + 1):
        for sensor in viable_sensors:
            if sensor['intersects']((x, y)) and (x, y) not in beacons:
                count += 1
                break

    return count


def intersects(center, radius):
    def func(point):
        distance = manhattan(center, point)

        return distance <= radius

    return func


def manhattan(one, two):
    d = abs(one[0] - two[0]) + abs(one[1] - two[1])

    return d


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
    def test_day_15(self):
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
        sensors, beacons, max_xy, min_xy = build_sensors_and_beacons(sensor_data)

        count = get_y_count(sensors, beacons, 10, min_xy[0], max_xy[0])
        expected = 26

        self.assertEqual(count, expected, f"Expected {expected} no gos but got {count}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
