import numpy as np
import random as rand


class SnakeGame:

    start_snake_len = 2  # don't change, will break code
    snake_tail_addition = 2  # how many segments to add when an apple is eaten

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

    def __init__(self, play_width, play_height, seed):

        self.play_width = play_width
        self.play_height = play_height

        rand.seed = seed

        self.wall_width = play_width + 2
        self.wall_height = play_height + 2

        self.max_distance = distance_formula((0, 0), (self.wall_width, self.wall_height))

        self.walls = np.ones((self.wall_height, self.wall_width))
        self.walls[1:play_height + 1, 1:play_width + 1] = np.zeros((play_height, play_width))

        self.snake = np.zeros((self.wall_height, self.wall_width))

        snake_head_start = (rand.randint(int(self.wall_height / 4), int(self.wall_height * 2 / 4)),
                            rand.randint(int(self.wall_width / 4), int(self.wall_width * 2 / 4)))

        snake_body_start_direction = self.directions.get(rand.randint(0, 3))

        snake_body_start = (snake_head_start[0] + snake_body_start_direction[0],
                            snake_head_start[1] + snake_body_start_direction[1])

        self.snake[snake_head_start[0], snake_head_start[1]] = self.start_snake_len
        self.snake[snake_body_start[0], snake_body_start[1]] = (self.start_snake_len - 1)

        self.apple = None
        self._place_apple()

        self.distance_score = 0
        self.score = 0
        self.viewer = None

    def print_board(self):
        # print board
        print(self.walls + self.snake - self.apple)

    def get_board(self):
        # walls = self.walls.reshape((self.wall_height, self.wall_width, 1))
        snake = self.snake.reshape((self.wall_height, self.wall_width, 1))
        apple = self.apple.reshape((self.wall_height, self.wall_width, 1))

        return np.concatenate((snake, apple))

    # returns 0 to continue, 1 for end of game
    def move(self, m):
        move_direction = self.directions.get(m)
        head_value = np.max(self.snake)
        current_head = np.where(self.snake == head_value)
        current_head = (current_head[0][0], current_head[1][0])
        new_head = (current_head[1] + move_direction[1], current_head[0] + move_direction[0])

        self.distance_score = self.max_distance - self.distance_to_apple(current_head)

        if self._lose_state(new_head):
            return False

        self.snake[new_head[1], new_head[0]] = head_value + 1

        if self._win_state():
            self.score += 100000000
            return False

        # if we eat an apple
        elif self._eat_apple_state(new_head):
            self._extend_tail()

            self._place_apple()
            self.score += 100

        self._decrement_snake()
        return True

    def distance_to_apple(self, current_head):
        apple_location = np.where(self.apple == 1)
        apple_location = (apple_location[0][0], apple_location[1][0])
        return distance_formula(apple_location, current_head)

    def _place_apple(self):
        invalid_placement = self.snake + self.walls

        mask = invalid_placement == 0
        c = np.count_nonzero(mask)

        valid_spots = np.where(mask)

        rand_valid_location = rand.randint(0, c - 1)

        y = valid_spots[0][rand_valid_location]
        x = valid_spots[1][rand_valid_location]

        self.apple = np.zeros((self.wall_height, self.wall_width))
        self.apple[y][x] = 1

    def _extend_tail(self):
        snake_parts = self.snake > 0
        self.snake = self.snake + snake_parts.astype(int) * (self.snake_tail_addition + 1)

    def _decrement_snake(self):
        snake_parts = self.snake > 0
        self.snake = np.subtract(self.snake, snake_parts.astype(int))

    def _win_state(self):
        snake_parts = self.snake > 0
        snake_win_board = self.walls > 0
        ones_win = snake_parts + snake_win_board
        return np.array_equal(ones_win, np.ones((self.wall_height, self.wall_width)))

    def _lose_state(self, new_head):
        return self.snake[new_head[1], new_head[0]] > 1 or self.walls[new_head[1], new_head[0]] > 0

    def _eat_apple_state(self, new_head):
        return self.apple[new_head[1], new_head[0]] > 0

    def get_user_input(self):
        tmp = input('')
        tmp_direction = self.char_to_direction.get(tmp, '')
        if tmp_direction != '':
            return tmp_direction

    #  ripped off from https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py
    def render(self, mode='human'):
        screen_width = 600
        screen_height = 400

        world_width = self.x_threshold * 2
        scale = screen_width / world_width
        carty = 100  # TOP OF CART
        polewidth = 10.0
        polelen = scale * (2 * self.length)
        cartwidth = 50.0
        cartheight = 30.0

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)
            l, r, t, b = -cartwidth / 2, cartwidth / 2, cartheight / 2, -cartheight / 2
            axleoffset = cartheight / 4.0
            cart = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            self.carttrans = rendering.Transform()
            cart.add_attr(self.carttrans)
            self.viewer.add_geom(cart)
            l, r, t, b = -polewidth / 2, polewidth / 2, polelen - polewidth / 2, -polewidth / 2
            pole = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
            pole.set_color(.8, .6, .4)
            self.poletrans = rendering.Transform(translation=(0, axleoffset))
            pole.add_attr(self.poletrans)
            pole.add_attr(self.carttrans)
            self.viewer.add_geom(pole)
            self.axle = rendering.make_circle(polewidth / 2)
            self.axle.add_attr(self.poletrans)
            self.axle.add_attr(self.carttrans)
            self.axle.set_color(.5, .5, .8)
            self.viewer.add_geom(self.axle)
            self.track = rendering.Line((0, carty), (screen_width, carty))
            self.track.set_color(0, 0, 0)
            self.viewer.add_geom(self.track)

            self._pole_geom = pole

        if self.state is None: return None

        # Edit the pole polygon vertex
        pole = self._pole_geom
        l, r, t, b = -polewidth / 2, polewidth / 2, polelen - polewidth / 2, -polewidth / 2
        pole.v = [(l, b), (l, t), (r, t), (r, b)]

        x = self.state
        cartx = x[0] * scale + screen_width / 2.0  # MIDDLE OF CART
        self.carttrans.set_translation(cartx, carty)
        self.poletrans.set_rotation(-x[2])

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None


def distance_formula(coord_1, coord_2):
    y_1 = coord_1[0]
    x_1 = coord_1[1]
    y_2 = coord_2[0]
    x_2 = coord_2[1]

    x = abs(x_1 - x_2)
    y = abs(y_1 - y_2)

    return (x ** 2 + y ** 2) ** (1 / 2)
