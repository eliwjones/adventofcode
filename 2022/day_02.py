import unittest


def calculate_score(str_data):
    moves = {'A': 'Rock', 'X': 'Rock', 'B': 'Paper', 'Y': 'Paper', 'C': 'Scissors', 'Z': 'Scissors'}
    move_scores = {'Rock': 1, 'Paper': 2, 'Scissors': 3}
    outcome_scores = {'win': 6, 'lose': 0, 'draw': 3}
    outcomes = {('Paper', 'Rock'): 'Paper', ('Paper', 'Scissors'): 'Scissors', ('Rock', 'Scissors'): 'Rock'}

    parsed_data = str_data.split('\n')
    suggested_moves = [line.split(' ') for line in parsed_data]
    suggested_moves = [(moves[opp], moves[you]) for opp, you in suggested_moves]

    your_score = 0
    opponent_score = 0
    for opponent, you in suggested_moves:
        sorted_key = tuple(sorted((opponent, you)))

        winner = you
        if sorted_key in outcomes:
            winner = outcomes[sorted_key]

        your_score += move_scores[you]
        opponent_score += move_scores[opponent]

        if winner == you and winner == opponent:
            your_score += outcome_scores['draw']
            opponent_score += outcome_scores['draw']
        elif winner == you:
            your_score += outcome_scores['win']
        else:
            opponent_score += outcome_scores['win']

    return your_score, opponent_score


class Test(unittest.TestCase):
    def test_calculate_score(self):
        data = ['A Y', 'B X', 'C Z']
        str_data = '\n'.join(map(str, data))

        you, opponent = calculate_score(str_data)

        self.assertEqual(you, 15, f"Expected your score to be 15 but got {you}.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
