import unittest


def signal(str_data, poll_points):
    parsed_data = str_data.split('\n')

    sig = [1]
    for cmd in parsed_data:
        cycles, inc = parse_command(cmd)
        extension = [sig[-1] for _ in range(cycles)]
        extension[-1] += inc

        sig.extend(extension)

    return sig


def signal_sum(sig, poll_points):
    return sum(sig[i] * (i + 1) for i in poll_points)


def parse_command(cmd):
    if cmd == 'noop':
        return 1, 0

    _, inc = cmd.split(' ')
    inc = int(inc)

    return 2, inc


def crt(sig):
    screen = [['.' for _ in range(40)] for _ in range(6)]

    for i in range(len(screen)):
        for j in range(len(screen[i])):
            idx = i * 40 + j
            pixel = [sig[idx] - 1, sig[idx], sig[idx] + 1]
            if j in pixel:
                screen[i][j] = '#'

    return screen


def display(screen):
    output = '\n'
    for row in screen:
        output += f"{''.join(row)}\n"

    return output


class Test(unittest.TestCase):
    def test_signal_sum(self):
        data = [
            'addx 15',
            'addx -11',
            'addx 6',
            'addx -3',
            'addx 5',
            'addx -1',
            'addx -8',
            'addx 13',
            'addx 4',
            'noop',
            'addx -1',
            'addx 5',
            'addx -1',
            'addx 5',
            'addx -1',
            'addx 5',
            'addx -1',
            'addx 5',
            'addx -1',
            'addx -35',
            'addx 1',
            'addx 24',
            'addx -19',
            'addx 1',
            'addx 16',
            'addx -11',
            'noop',
            'noop',
            'addx 21',
            'addx -15',
            'noop',
            'noop',
            'addx -3',
            'addx 9',
            'addx 1',
            'addx -3',
            'addx 8',
            'addx 1',
            'addx 5',
            'noop',
            'noop',
            'noop',
            'noop',
            'noop',
            'addx -36',
            'noop',
            'addx 1',
            'addx 7',
            'noop',
            'noop',
            'noop',
            'addx 2',
            'addx 6',
            'noop',
            'noop',
            'noop',
            'noop',
            'noop',
            'addx 1',
            'noop',
            'noop',
            'addx 7',
            'addx 1',
            'noop',
            'addx -13',
            'addx 13',
            'addx 7',
            'noop',
            'addx 1',
            'addx -33',
            'noop',
            'noop',
            'noop',
            'addx 2',
            'noop',
            'noop',
            'noop',
            'addx 8',
            'noop',
            'addx -1',
            'addx 2',
            'addx 1',
            'noop',
            'addx 17',
            'addx -9',
            'addx 1',
            'addx 1',
            'addx -3',
            'addx 11',
            'noop',
            'noop',
            'addx 1',
            'noop',
            'addx 1',
            'noop',
            'noop',
            'addx -13',
            'addx -19',
            'addx 1',
            'addx 3',
            'addx 26',
            'addx -30',
            'addx 12',
            'addx -1',
            'addx 3',
            'addx 1',
            'noop',
            'noop',
            'noop',
            'addx -9',
            'addx 18',
            'addx 1',
            'addx 2',
            'noop',
            'noop',
            'addx 9',
            'noop',
            'noop',
            'noop',
            'addx -1',
            'addx 2',
            'addx -37',
            'addx 1',
            'addx 3',
            'noop',
            'addx 15',
            'addx -21',
            'addx 22',
            'addx -6',
            'addx 1',
            'noop',
            'addx 2',
            'addx 1',
            'noop',
            'addx -10',
            'noop',
            'noop',
            'addx 20',
            'addx 1',
            'addx 2',
            'addx 2',
            'addx -6',
            'addx -11',
            'noop',
            'noop',
            'noop',
        ]

        str_data = '\n'.join(map(str, data))

        sig = signal(str_data, poll_points=list(range(19, 220, 40)))
        sig_sum = signal_sum(sig, poll_points=list(range(19, 220, 40)))
        expected = 13140

        self.assertEqual(sig_sum, expected, f"Expected signal sum to be {expected} but got {sig_sum}.")

        screen = crt(sig)
        print(display(screen))


if __name__ == '__main__':
    unittest.main(verbosity=2)
