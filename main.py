import numpy as np
import random as rand

play_width = 3
play_height = 5

start_snake_len = 2  # don't change, will break code
snake_tail_addition = 2

directions = {
    0: (0, -1),  # left
    1: (-1, 0),  # up
    2: (0, 1),  # right
    3: (1, 0),  # down
}

char_to_direction = {
    'j': (0, -1),  # left
    'k': (-1, 0),  # up
    'l': (0, 1),  # right
    ';': (1, 0),  # down
}

wall_width = play_width + 2
wall_height = play_height + 2

# board start with (0, 0) at the top left


def main():

    walls = np.ones((wall_height, wall_width))
    walls[1:play_height + 1, 1:play_width + 1] = np.zeros((play_height, play_width))

    snake = np.zeros((wall_height, wall_width))

    snake_head_start = (rand.randint(int(wall_height / 3), int(wall_height * 2 / 3)),
                        rand.randint(int(wall_width / 3), int(wall_width * 2 / 3)))

    snake_body_start_direction = directions.get(rand.randint(0, 3))

    snake_body_start = (snake_head_start[0] + snake_body_start_direction[0],
                        snake_head_start[1] + snake_body_start_direction[1])

    snake[snake_head_start[0], snake_head_start[1]] = start_snake_len
    snake[snake_body_start[0], snake_body_start[1]] = (start_snake_len - 1)

    apple = place_apple(snake, walls)

    score = 0
    # Game Loop
    while True:
        # print board
        print(walls + snake + apple)
        print('Enter a Direction, "j" = left "k" = up "l" = right ";" = down')

        move_direction = get_user_input()

        head_value = np.max(snake)
        current_head = np.where(snake == head_value)
        current_head = (current_head[0][0], current_head[1][0])
        new_head = (current_head[1] + move_direction[1], current_head[0] + move_direction[0])

        if snake[new_head[1], new_head[0]] > 1 or walls[new_head[1], new_head[0]] > 0:
            print('you died, your score is: ' + str(score))
            exit(0)

        snake[new_head[1], new_head[0]] = head_value + 1

        if win_state(snake, walls):
            score = 100000000
            print('you won, your score is: ' + str(score))
            break

        # if we eat an apple
        if apple[new_head[1], new_head[0]] > 0:
            snake = extend_tail(snake)

            apple = place_apple(snake, walls)
            score += 100

        snake = decrement_snake(snake)


def place_apple(snake, walls):
    invalid_placement = snake + walls

    mask = invalid_placement == 0
    c = np.count_nonzero(mask)

    valid_spots = np.where(mask)

    rand_valid_location = rand.randint(0, c - 1)

    y = valid_spots[0][rand_valid_location]
    x = valid_spots[1][rand_valid_location]

    apple = np.zeros((wall_height, wall_width))
    apple[y][x] = 1

    return apple


def extend_tail(snake):
    snake_parts = snake > 0
    return snake + snake_parts.astype(int) * (snake_tail_addition + 1)


def decrement_snake(snake):
    snake_parts = snake > 0
    return np.subtract(snake, snake_parts.astype(int))


def win_state(snake, walls):
    snake_parts = snake > 0
    snake_win_board = walls > 0
    ones_win = snake_parts + snake_win_board
    return np.array_equal(ones_win, np.ones((wall_height, wall_width)))


def get_user_input():
    while True:
        tmp = input('')
        tmp_direction = char_to_direction.get(tmp, '')
        if tmp_direction != '':
            return tmp_direction


main()

