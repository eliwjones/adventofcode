import unittest


def start_marker(str_buffer):
    for i in range(4, len(str_buffer) + 1):
        marker = str_buffer[i - 4 : i]
        if len(marker) == len(set(marker)):
            return i, marker

    return -1, []


class Test(unittest.TestCase):
    def test_start_marker(self):
        test_cases = [
            ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7),
            ('bvwbjplbgvbhsrlpgdmjqwftvncz', 5),
            ('nppdvjthqldpwncqszvftbrmjlhg', 6),
            ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10),
            ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11),
            ('1111111111111111111112345', 24),
            ('', -1),
            ('aaaaaaaaaaaaaaaaaaaaaaaaa', -1),
        ]

        for str_buffer, expected in test_cases:
            index, marker = start_marker(str_buffer)

            self.assertEqual(index, expected, f"Expected start_marker to be {expected} but got {index}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
