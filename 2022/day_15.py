import unittest

from collections import defaultdict


def build_sensors_and_beacons(sensor_data):
    sensors = {}
    beacons = {}

    max_xy = [0, 0]
    min_xy = [0, 0]
    for sensor, beacon in sensor_data:
        distance = manhattan(sensor, beacon)

        sensors[sensor] = {
            'bounds': {'x': [sensor[0] - distance, sensor[0] + distance], 'y': [sensor[1] - distance, sensor[1] + distance]},
            'intersects': intersects(sensor, distance),
            'radius': distance,
        }

        beacons[beacon] = True

        for i in range(2):
            max_xy[i] = max(sensor[i] + distance, beacon[i], max_xy[i])
            min_xy[i] = min(sensor[i] - distance, beacon[i], min_xy[i])

    return sensors, beacons, max_xy, min_xy


def filter_sensors(sensors):
    keep = []
    keys = list(reversed(sorted(sensors.keys(), key=lambda k: sensors[k]['radius'])))
    while keys:
        max_key = keys.pop(0)
        keep.append(max_key)
        max_sensor = sensors[max_key]
        print(f"max_sensor: {max_sensor}")
        for key in keys:
            sensor = sensors[key]
            if sensor['bounds']['x'][0] < max_sensor['bounds']['x'][0]:
                continue
            if sensor['bounds']['x'][1] > max_sensor['bounds']['x'][1]:
                continue
            if sensor['bounds']['y'][0] < max_sensor['bounds']['y'][0]:
                continue
            if sensor['bounds']['y'][1] > max_sensor['bounds']['y'][1]:
                continue

            print(f"removing sensor: {sensor}")

            keys.remove(key)

    return {sensor: sensors[sensor] for sensor in keep}


def find_point(intersections, sensors):
    my_point = (0, 0)
    for p in [p for v in intersections.values() for p in v]:
        seen = False
        for sensor in sensors:
            if sensors[sensor]['intersects'](p):
                seen = True
                break
        if not seen:
            my_point = p
            break

    return my_point


def get_boundaries(sensors):
    sign = lambda a: 1 if a > 0 else -1 if a < 0 else 0

    boundaries = {}
    for sensor in sensors:
        r = sensors[sensor]['radius'] + 1

        """
          Just draw the boundary directly.
        """

        paths = [
            {'start': (sensor[0] - r, sensor[1]), 'stop': (sensor[0], sensor[1] - r)},
            {'start': (sensor[0], sensor[1] - r), 'stop': (sensor[0] + r, sensor[1])},
            {'start': (sensor[0] + r, sensor[1]), 'stop': (sensor[0], sensor[1] + r)},
            {'start': (sensor[0], sensor[1] + r), 'stop': (sensor[0] - r, sensor[1])},
        ]

        boundary = set()
        for p in paths:
            boundary.add(p['start'])
            boundary.add(p['stop'])

            x_sign = sign(p['stop'][0] - p['start'][0])
            y_sign = sign(p['stop'][1] - p['start'][1])

            point = p['start']
            while point != p['stop']:
                point = (point[0] + x_sign, point[1] + y_sign)
                boundary.add(point)

        boundaries[sensor] = boundary

    return boundaries


def get_intersections(boundaries):
    from itertools import combinations

    intersections = dict()
    combos = combinations(boundaries.keys(), 3)
    for c in combos:
        one = boundaries[c[0]]
        two = boundaries[c[1]]
        three = boundaries[c[2]]

        intersection = one & two & three
        if intersection:
            intersections[f"{c[0]}_{c[1]}_{c[2]}"] = list(intersection)

    return intersections


def get_y_count(sensors, beacons, y, min_x, max_x):
    viable_sensors = []
    for sensor in sensors.values():
        if sensor['bounds']['y'][0] <= y <= sensor['bounds']['y'][1]:
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

        sensors = filter_sensors(sensors)

        count = get_y_count(sensors, beacons, 10, min_xy[0], max_xy[0])
        expected = 26

        self.assertEqual(count, expected, f"Expected {expected} no gos but got {count}.")

        boundaries = get_boundaries(sensors)
        intersections = get_intersections(boundaries)

        point = find_point(intersections, sensors)
        value = 4000000 * point[0] + point[1]
        expected = 56000011

        self.assertEqual(value, expected, f"Expected {expected} but got {value} for point: {point}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
