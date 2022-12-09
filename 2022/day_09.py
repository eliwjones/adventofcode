import unittest


sign = lambda a: (a > 0) - (a < 0)


def tail_moves(str_data, num_knots):
    moves = unpack_moves(moves=str_data.split('\n'))

    knots = [(0, 0) for _ in range(num_knots)]
    tail_positions = {(0, 0)}
    for move in moves:
        knots[0] = move_head(move, knots[0])
        for i in range(1, num_knots):
            knots[i] = move_tail(knots[i], knots[i - 1])

        tail_positions.add(knots[-1])

    return tail_positions


def unpack_moves(moves):
    unpacked_moves = []
    for move in moves:
        dir, count = move.split(' ')
        unpacked_moves.extend([f"{dir} 1" for _ in range(int(count))])

    return unpacked_moves


def move_head(move, head):
    dir, count = move.split(' ')

    inc = int(count)
    if dir in ['L', 'D']:
        inc = -1 * int(count)

    if dir in ['R', 'L']:
        return (head[0] + inc, head[1])
    elif dir in ['U', 'D']:
        return (head[0], head[1] + inc)

    raise Exception(f"Unacceptable move: {move}")


def move_tail(tail, head):
    diff = (head[0] - tail[0], head[1] - tail[1])

    if abs(diff[0]) <= 1 and abs(diff[1]) <= 1:
        """We are touching so no move to make."""
        return tail

    if diff[0] == 0 or diff[1] == 0:
        return (tail[0] + diff[0] // 2, tail[1] + diff[1] // 2)

    """
    We are in position of:

        (1,2) (1,-2) (-1,2) (-1,-2)
        (2,1) (-2,1) (2,-1) (-2,-1)

    Thus, we just need to move (1,1) but in the correct direction
    so we shall use sign() for that.

    """
    return (tail[0] + sign(diff[0]), tail[1] + sign(diff[1]))


class Test(unittest.TestCase):
    def test_tail_moves(self):
        data = ['R 4', 'U 4', 'L 3', 'D 1', 'R 4', 'D 1', 'L 5', 'R 2']
        str_data = '\n'.join(data)

        moves = tail_moves(str_data, num_knots=2)
        expected = 13

        self.assertEqual(len(moves), expected, f"Expected tail to have visited {expected} spots but got {len(moves)}.")

        data = ['R 5', 'U 8', 'L 8', 'D 3', 'R 17', 'D 10', 'L 25', 'U 20']
        str_data = '\n'.join(data)

        moves = tail_moves(str_data, num_knots=10)
        expected = 36

        self.assertEqual(len(moves), expected, f"Expected tail to have visited {expected} spots but got {len(moves)}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
