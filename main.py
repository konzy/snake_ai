

# board coordinates- (0, 0) at the top left
import copy
import os
import random as rand
import neat

from snake_game import SnakeGame

seed = rand.random
y = 6
x = 6
snake_game = SnakeGame(y, x, seed)
generations = 1000


def eval_genomes(genomes, config):

    for genome_id, genome in genomes:
        game = copy.deepcopy(snake_game)
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        total_moves = 0
        cont = True
        # moves_since_apple = 0
        # last_score = 0
        #  moves_since_apple > y * x * 2
        while cont and (game.score / 100 + 1) * x * y * 2 > total_moves:
            # last_score = game.score
            output = net.activate(game.get_board().flat)
            index_of_max = output.index(max(output))
            # print('move=' + str(index_of_max))
            cont = game.move(index_of_max)
            total_moves += 1

        total_score = game.score
        genome.fitness = total_score
        # print('total score=' + str(total_score))


def main():
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'config-feedforward')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, generations)

    print('\nBest genome:\n{!s}'.format(winner))

    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    game = copy.deepcopy(snake_game)
    cont = True
    while cont:
        print(game.print_board())
        output = winner_net.activate(game.get_board())
        cont = game.move(output)

    print(game.print_board())



main()

