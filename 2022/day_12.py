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
    winners = []
    paths = [[start]]
    while paths:
        new_paths = []
        for path in paths:
            pos = path[-1]

            if pos == end:
                winners.append(path)
                continue

            valid_moves = [(i, j) for i, j in moves[pos[0]][pos[1]] if (i, j) not in path]
            if not valid_moves:
                continue

            for i, j in valid_moves:
                new_paths.append(path + [(i, j)])

        paths = new_paths

    return winners


class Test(unittest.TestCase):
    def test_find_paths(self):
        data = ['Sabqponm', 'abcryxxl', 'accszExk', 'acctuvwj', 'abdefghi']
        maze = [[*line] for line in data]

        moves, start, end, maze = process_maze(maze)

        print(f"\nstart: {start}, end: {end}")

        ijs = [(i, j) for i in range(len(moves)) for j in range(len(moves[i]))]
        for i, j in ijs:
            if end not in moves[i][j]:
                continue
            print(f"moves[{i}][{j}]: {moves[i][j]}")

        winners = find_paths(moves, start, end)

        min_len = min([len(winner) for winner in winners]) - 1
        expected = 31

        for winner in [w for w in winners if len(w) == min_len]:
            print("***************** winner ****************")
            print(winner)

        self.assertEqual(min_len, expected, f"Expected min length to be {expected} but got {min_len}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
