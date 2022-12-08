import unittest


LS = '$ ls'
CD = '$ cd '
DIR = 'dir '
TOTAL_SIZE = 70_000_000
MIN_SPACE = 30_000_000


def dir_sizes(str_buffer):
    lines = str_buffer.split('\n')

    dir_sizes = {}
    stack = []
    for line in lines:
        if line.startswith(CD):
            curr_dir = line.replace(CD, '')
            if curr_dir == '..':
                stack.pop()
            else:
                stack.append(curr_dir)
        elif line.startswith(LS):
            continue  # Not sure if we need any special notes here.
        elif line.startswith(DIR):
            continue
        else:
            size, filename = line.split(' ')
            size = int(size)

            for i in range(1, len(stack) + 1):
                dir = '/'.join(stack[:i]).replace('//', '/')
                if dir not in dir_sizes:
                    dir_sizes[dir] = 0

                dir_sizes[dir] += size

    return dir_sizes


def threshold_sum(dir_sizes, threshold):
    filtered_dirs = {dir: size for dir, size in dir_sizes.items() if size <= threshold}

    return sum(filtered_dirs.values())


def min_dir_to_delete(dir_sizes, total_size, min_space):
    free_space = total_size - dir_sizes['/']
    space_needed = min_space - free_space

    if space_needed <= 0:
        return 0, ''

    filtered_dirs = {size: dir for dir, size in dir_sizes.items() if size >= space_needed}
    min_size = min(filtered_dirs.keys())

    return min_size, filtered_dirs[min_size]


class Test(unittest.TestCase):
    def test_start_marker(self):
        data = [
            '$ cd /',
            '$ ls',
            'dir a',
            '14848514 b.txt',
            '8504156 c.dat',
            'dir d',
            '$ cd a',
            '$ ls',
            'dir e',
            '29116 f',
            '2557 g',
            '62596 h.lst',
            '$ cd e',
            '$ ls',
            '584 i',
            '$ cd ..',
            '$ cd ..',
            '$ cd d',
            '$ ls',
            '4060174 j',
            '8033020 d.log',
            '5626152 d.ext',
            '7214296 k',
        ]

        str_data = '\n'.join(data)
        directories = dir_sizes(str_data)
        size = threshold_sum(directories, 100000)
        expected = 95437

        self.assertEqual(size, expected, f"Expected size to be {expected} but got {size}.")

        size, dirname = min_dir_to_delete(directories, TOTAL_SIZE, MIN_SPACE)
        expected = 24933642

        self.assertEqual(size, expected, f"Expected min_dir size to be {expected} but got {size} for dir '{dirname}'.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
