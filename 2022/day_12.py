import unittest


def process_maze(maze):
    moves = []
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    start = (0, 0)
    end = (0, 0)
    for i in range(len(maze)):
        moves.append([])
        for j in range(len(maze[i])):
            moves[i].append([])

            if maze[i][j] == 'S':
                start = (i, j)
                maze[i][j] = 'a'
            elif maze[i][j] == 'E':
                end = (i, j)
                maze[i][j] = 'z'

            pos_val = ord(maze[i][j])
            for k, l in directions:
                if not 0 <= i + k < len(maze) or not 0 <= j + l < len(maze[i]):
                    continue

                mov = maze[i + k][j + l]
                if mov == 'S':
                    mov = 'a'
                if mov == 'E':
                    mov = 'z'

                mov_val = ord(mov) - pos_val
                if mov_val > 1:
                    continue

                moves[i][j].append((i + k, j + l))

    return moves, start, end, maze


def find_paths(moves, start, end):
    from copy import deepcopy

    winners = []
    paths = [{start: None}]

    visited = {}

    while paths:
        new_paths = []
        for path in paths:
            pos = list(path.keys())[-1]

            if pos == end:
                winners.append(path)
                continue

            seen = path | visited
            valid_moves = [(i, j) for i, j in moves[pos[0]][pos[1]] if (i, j) not in seen]
            if not valid_moves:
                continue

            for i, j in valid_moves:
                new_path = deepcopy(path)
                new_path[(i, j)] = None
                visited[(i, j)] = None

                new_paths.append(new_path)

        paths = new_paths

    return winners


def manhattan(one, two):
    d = abs(one[0] - two[0]) + abs(one[1] - two[1])

    return d


def trim_moves(valid_moves, pos, end):
    """
    Not used! But kept around just in case.
    """
    weights = []
    for m in valid_moves:
        move_pos = (pos[0] + m[0], pos[1] + m[1])
        weight = manhattan(move_pos, end)

        weights.append((weight, m))

    min_weight = min(w[0] for w in weights)

    return [w[1] for w in weights if w[0] == min_weight]


def best_start(starts, moves, end):
    winners = []
    for start in starts:
        winners.extend(find_paths(moves, start, end))

    return min_path(winners)


def valid_starts(maze, moves):
    ijs = [(i, j) for i in range(len(maze)) for j in range(len(maze[i]))]
    a_positions = [(i, j) for i, j in ijs if maze[i][j] == 'a']

    starts = []
    for i, j in a_positions:
        valid_moves = moves[i][j]
        valid_moves = [m for m in valid_moves if maze[m[0]][m[1]] != 'a']

        if not valid_moves:
            continue

        starts.append((i, j))

    return starts


def min_path(paths):
    result = paths[0]
    for path in paths[1:]:
        if len(path) < len(result):
            result = path

    return result


class Test(unittest.TestCase):
    def test_find_paths(self):
        data = ['Sabqponm', 'abcryxxl', 'accszExk', 'acctuvwj', 'abdefghi']
        maze = [[*line] for line in data]

        moves, start, end, maze = process_maze(maze)
        winners = find_paths(moves, start, end)

        min_len = len(min_path(winners)) - 1
        expected = 31

        self.assertEqual(min_len, expected, f"Expected min length to be {expected} but got {min_len}.")

        starts = valid_starts(maze, moves)
        path = best_start(starts, moves, end)

        min_len = len(path) - 1
        expected = 29

        self.assertEqual(min_len, expected, f"Expected min length to be {expected} but got {min_len}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
