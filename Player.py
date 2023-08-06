import random
import math


class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter

    def get_move(self, game):
        pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8):')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val


class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves()) # randomly chose one
        else:
            # get the square based on the minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter # the actual player
        other_player = 'O' if player == 'X' else 'X'

        # first we want to check if the next move is a winning move
        # that's the base case
        if state.current_winner == other_player:
            # we should return position AND score because we need to track of the score for the minimax to work
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player
                    else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares(): # no empty squares
            return {'position': None, 'score': 0}

        # initialise some dictionaries
        if player == max_player:
            best = {'position': None, 'score': -math.inf} # each score should maximize
        else:
            best = {'position': None, 'score': math.inf}  # each score should minimize

        for possible_move in state.available_moves():
            # step1: make a move, try the spot
            state.make_move(possible_move, player)
            # step2: recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player) # we alternate the players
            # step3: undo that move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move # otherwise this will get messed up

            # step4: update the dictionaries if necessary
            if player == max_player: # maximise the max player
                if sim_score['score'] > best['score']:
                    best = sim_score # replace best
            else: # minimise the other player
                if sim_score['score'] < best['score']:
                    best = sim_score # replace best
        return best
