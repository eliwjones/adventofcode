import unittest


def parse_tree_matrix(str_data):
    parsed_data = str_data.split('\n')
    tree_matrix = [list(map(int, [*line])) for line in parsed_data]

    m_len = len(tree_matrix[0])
    n_len = len(tree_matrix)

    return tree_matrix, m_len, n_len


def scenic_scores(str_data):
    tree_matrix, m_len, n_len = parse_tree_matrix(str_data)

    scores = {}
    for i in range(m_len):
        for j in range(n_len):
            up = scan_out(tree_matrix=tree_matrix, n_len=n_len, m_len=m_len, m=i, n=j, n_inc=-1)
            down = scan_out(tree_matrix=tree_matrix, n_len=n_len, m_len=m_len, m=i, n=j, n_inc=1)
            left = scan_out(tree_matrix=tree_matrix, n_len=n_len, m_len=m_len, m=i, n=j, m_inc=-1)
            right = scan_out(tree_matrix=tree_matrix, n_len=n_len, m_len=m_len, m=i, n=j, m_inc=1)

            scores[(i, j)] = up * down * left * right

    return scores


def visible_trees(str_data):
    tree_matrix, m_len, n_len = parse_tree_matrix(str_data)

    seen_trees = set()
    for i in range(m_len):
        seen_trees = scan_line(tree_matrix=tree_matrix, n_len=n_len, m_len=m_len, seen_trees=seen_trees, m=i, n_inc=1)
        seen_trees = scan_line(
            tree_matrix=tree_matrix, n_len=n_len, m_len=m_len, seen_trees=seen_trees, m=i, n=n_len - 1, n_inc=-1
        )

    for j in range(n_len):
        seen_trees = scan_line(tree_matrix=tree_matrix, n_len=n_len, m_len=m_len, seen_trees=seen_trees, n=j, m_inc=1)
        seen_trees = scan_line(
            tree_matrix=tree_matrix, n_len=n_len, m_len=m_len, seen_trees=seen_trees, n=j, m=m_len - 1, m_inc=-1
        )

    return seen_trees


def scan_line(tree_matrix, n_len, m_len, seen_trees, n=0, m=0, n_inc=0, m_inc=0):
    prev_height = -1
    while 0 <= m < m_len and 0 <= n < n_len:
        curr_height = tree_matrix[n][m]
        if curr_height > prev_height:
            seen_trees.add((n, m))
            prev_height = curr_height

        m += m_inc
        n += n_inc

    return seen_trees


def scan_out(tree_matrix, n_len, m_len, n=0, m=0, n_inc=0, m_inc=0):
    height = tree_matrix[n][m]
    tree_count = 0
    while 0 < m < m_len - 1 and 0 < n < n_len - 1:
        m += m_inc
        n += n_inc

        tree_count += 1
        if tree_matrix[n][m] >= height:
            break

    return tree_count


class Test(unittest.TestCase):
    def test_visible_trees_and_scenic_scores(self):
        data = ['30373', '25512', '65332', '33549', '35390']
        str_data = '\n'.join(map(str, data))

        trees = visible_trees(str_data)
        count = len(trees)
        expected = 21

        self.assertEqual(count, expected, f"Expected {expected} visible trees but got {count}.")

        scores = scenic_scores(str_data)
        max_score = max(scores.values())
        expected = 8

        self.assertEqual(max_score, expected, f"Expected {expected} max scenic score but got {max_score}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
