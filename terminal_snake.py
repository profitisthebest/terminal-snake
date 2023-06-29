import random

# global constants
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4


class Snake:
    # store each body part of snake as a coordinate in a tuple
    def __init__(self, body, direction):
        self.direction = direction
        self.body = body

    # add to the head of the snake and pop off the back of the snake
    def move(self, pos):
        # add to the head and pop off of the back
        self.body = [pos] + self.body[:-1]

    def set_direction(self, new_direction):
        self.direction = new_direction

    def get_direction(self):
        return self.direction

    def get_head(self):
        return self.body[0]

    def extend(self):
        self.body.append(self.body[-1])


class Apple:
    def __init__(self, pos):
        self.location = pos


class Game:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.snake = Snake(
            [(height//2,  width//2), ((height//2)+1, width//2)], UP)
        self.live = True
        self.score = 0
        # generate random apple
        self.apple = Apple((random.randint(1, height-2),
                           random.randint(1, width-2)))

    def over(self):
        return not self.live

    # generate an empty board
    def generate_empty_board(self):
        matrix = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(' ')
            matrix.append(row)

        # add solid borders
        for w in range(self.width):
            matrix[0][w] = '-'
            matrix[self.height-1][w] = '-'
        for h in range(self.height):
            matrix[h][0] = '|'
            matrix[h][self.width-1] = '|'

        return matrix

    # render the board to the terminal screen
    def render(self):
        matrix = self.generate_empty_board()

        # add snake to the board
        head = self.snake.get_head()
        matrix[head[0]][head[1]] = 'X'
        for body in self.snake.body[1:]:
            matrix[body[0]][body[1]] = 'O'

        # add apple to the board and make sure it is not on the snake (if it is generate new apple)
        while self.apple.location in self.snake.body:
            self.apple = Apple(
                (random.randint(1, self.height-2), random.randint(1, self.width-2)))
        matrix[self.apple.location[0]][self.apple.location[1]] = 'A'

        # render the board to the terminal screen
        for i in range(self.height):
            for j in range(self.width):
                print(matrix[i][j], end=' ')
            print('\n')

    # get the coordinate of the new position to move
    def get_new_position(self):
        head = self.snake.get_head()

        if self.snake.get_direction() == UP:
            return (head[0]-1, head[1])
        elif self.snake.get_direction() == RIGHT:
            return (head[0], head[1]+1)
        elif self.snake.get_direction() == DOWN:
            return (head[0]+1, head[1])
        elif self.snake.get_direction() == LEFT:
            return (head[0], head[1]-1)

    # check if the new position is valid (not out of bounds)
    def check_valid_move(self, choice):
        if self.snake.get_direction() == UP and choice == 's':
            return False
        if self.snake.get_direction() == RIGHT and choice == 'a':
            return False
        if self.snake.get_direction() == DOWN and choice == 'w':
            return False
        if self.snake.get_direction() == LEFT and choice == 'd':
            return False
        return True

    # return true if the snake collided into a wall
    def check_collision(self, new_pos):
        # wall collision
        if new_pos[0] <= 0 or new_pos[0] >= self.height-1 or new_pos[1] <= 0 or new_pos[1] >= self.width-1:
            self.live = False
            return True

        # snake collision
        if new_pos in self.snake.body:
            self.live = False
            return True

    def do_something(self):
        # get input from user
        choice = input(
            'Press enter to move the snake in the selected direction OR select a new direction with the valid keys.')

        # check that move isn't a 180 degree turn (invalid)
        if not self.check_valid_move(choice):
            print('Invalid move. Please try again.')
            return

        # move the snake or change direction
        if choice == 'w':
            self.snake.set_direction(UP)
        elif choice == 'd':
            self.snake.set_direction(RIGHT)
        elif choice == 's':
            self.snake.set_direction(DOWN)
        elif choice == 'a':
            self.snake.set_direction(LEFT)
        else:
            print('Invalid key. Please try again.')
            return

        new_pos = self.get_new_position()

        # if the snake collides with a wall or itself, game over
        if self.check_collision(new_pos):
            return

        self.snake.move(new_pos)

        # if the snake eats the apple, increase score and body length
        if new_pos == self.apple.location:
            self.score += 1
            self.snake.extend()


def main():
    print('Welcome to Snake! Enter the desired height and width of the board below (perferrably odd numbers).')
    height = int(input('Height: '))
    width = int(input('Width: '))
    game = Game(height, width)
    game.render()
    while not game.over():
        game.do_something()
        game.render()
    print('Game over!' + '\n' + 'Score: ' + str(game.score))


if __name__ == '__main__':
    main()
