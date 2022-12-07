import unittest


def start_marker(str_buffer, length):
    for i in range(length, len(str_buffer) + 1):
        marker = str_buffer[i - length : i]
        if len(marker) == len(set(marker)):
            return i, marker

    return -1, []


class Test(unittest.TestCase):
    def test_start_marker(self):
        test_cases = [
            ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7, 19),
            ('bvwbjplbgvbhsrlpgdmjqwftvncz', 5, 23),
            ('nppdvjthqldpwncqszvftbrmjlhg', 6, 23),
            ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10, 29),
            ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11, 26),
            ('1111111111111111111112345', 24, -1),
            ('', -1, -1),
            ('aaaaaaaaaaaaaaaaaaaaaaaaa', -1, -1),
        ]

        for str_buffer, packet_marker, message_marker in test_cases:
            index, marker = start_marker(str_buffer, 4)

            self.assertEqual(index, packet_marker, f"Expected start packet marker to be {packet_marker} but got {index}.")

            index, marker = start_marker(str_buffer, 14)

            self.assertEqual(index, message_marker, f"Expected start message marker to be {message_marker} but got {index}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
