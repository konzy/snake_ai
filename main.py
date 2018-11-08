

# board coordinates- (0, 0) at the top left
import copy
import pickle
import random as rand
import keras

from snake_game import SnakeGame


def main():

    # Initialize snake stuff
    seed = rand.random
    y = 6
    x = 10
    num_agents = 500
    generation = 1

    brains = [num_agents]

    snake_game = SnakeGame(y, x, seed)

    for brain in brains:
        brain = create_brain()

    for i in range(num_agents):
        print('Start of generation ' + str(generation) + ' agent ' + str(i))
        turn = 0
        game = copy.deepcopy(snake_game)

        # Writes entire game object to file, could be more efficient but, whatever.
        pickle.dump(game, open("gen" + str(generation) + '/agent' + str(i) + 'turn' + str(turn)))


def create_brain():
    keras.layers.Conv2D(20, (3, 3), strides=(1, 1), padding='valid', data_format=None,
                        dilation_rate=(1, 1), activation=None, use_bias=True, kernel_initializer='glorot_uniform',
                        bias_initializer='zeros')


main()

