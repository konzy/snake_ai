

# board coordinates- (0, 0) at the top left
from snake_game import SnakeGame


def main():

    snake_game = SnakeGame(6, 6)
    cont = True

    while cont:
        snake_game.print_board()
        cont = snake_game.move(0)
        print(snake_game.score + snake_game.distance_score)


main()

