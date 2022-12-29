# Matthew Neufeld

# Pong - left player controls the left paddle by pressing and holding down the q key to
# move the paddle up and the a key to move the paddle down. The right player
# controls the right paddle by pressing and holding down the p key to move the
# paddle up and the l key to move the paddle down.

# The objective is to make the ball hit the back of the other player's side.
# 1 point will be awarded if a player makes the ball hit the back of the other
# player's side. First to 11 wins.

import pygame

# User-defined functions

def main():
    # initialize all pygame modules
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('Pong')
    # get the display surface
    w_surface = pygame.display.get_surface()
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit()


# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        self.surface = surface
        self.bg_color = pygame.Color('#232b2b')

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        self.paddle_increment = 10
        paddle_width = 10
        self.left_score = 0
        self.right_score = 0
        y = self.surface.get_height() // 2 - paddle_width // 2
        self.paddle = Paddle(40, y, paddle_width, 75, '#8BC6FC', self.surface)
        self.paddle2 = Paddle(460, y, paddle_width, 75, '#FF6961', self.surface)
        self.ball = Ball('white', 5, [250, 200], [5, 5], self.surface)

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.
        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()
            if self.continue_game:
                self.check_collision()
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS)  # run at most with FPS Frames Per Second

    def check_collision(self):
        # check to see if the ball collides with a paddle
        if self.ball.getx_velocity() > 0:
            if self.paddle2.collide(self.ball.get_x_location(), self.ball.get_y_location()):
                self.ball.bounce_off_paddle()
        else:
            if self.paddle.collide(self.ball.get_x_location(), self.ball.get_y_location()):
                self.ball.bounce_off_paddle()

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            elif event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            elif event.type == pygame.KEYUP:
                self.handle_key_up(event)

    def handle_key_down(self, event):
        # reponds to KEYDOWN event
        # - self is the Game object
        if event.key == pygame.K_a:
            self.paddle.set_vertical_velocity(self.paddle_increment)
        elif event.key == pygame.K_q:
            self.paddle.set_vertical_velocity(-self.paddle_increment)
        if event.key == pygame.K_l:
            self.paddle2.set_vertical_velocity(self.paddle_increment)
        elif event.key == pygame.K_p:
            self.paddle2.set_vertical_velocity(-self.paddle_increment)

    def handle_key_up(self, event):
        # responds to KEYUP event
        # - self is the Game object
        if event.key == pygame.K_a:
            self.paddle.set_vertical_velocity(0)
        elif event.key == pygame.K_q:
            self.paddle.set_vertical_velocity(0)
        if event.key == pygame.K_p:
            self.paddle2.set_vertical_velocity(0)
        elif event.key == pygame.K_l:
            self.paddle2.set_vertical_velocity(0)

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
        self.surface.fill(self.bg_color)  # clear the display surface first
        self.paddle.draw()
        self.paddle2.draw()
        self.draw_score()
        self.ball.draw()
        pygame.display.update()  # make the updated surface appear on the display

    def draw_score(self):
        # draw the score on the surface
        self.draw_left_score()
        self.draw_right_score()

    def draw_left_score(self):
        # attributes of the left score
        font = pygame.font.SysFont('', 70)
        text_image = font.render(str(self.left_score), True, pygame.Color('#8BC6FC'), self.bg_color)
        location = (0, 0)
        self.surface.blit(text_image, location)

    def draw_right_score(self):
        # attributes of the right score
        font = pygame.font.SysFont('', 70)
        text_image = font.render(str(self.right_score), True, pygame.Color('#FF6961'), self.bg_color)
        location = (self.surface.get_width() - text_image.get_width(), 0)
        self.surface.blit(text_image, location)

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update
        if self.ball.getx_velocity() > 0:
            if self.ball.get_x_location() == self.ball.radius:
                self.right_score = self.right_score + 1
        else:
            if self.ball.get_x_location() == self.surface.get_size()[0] - self.ball.radius:
                self.left_score = self.left_score + 1

        self.paddle.move()
        self.paddle2.move()
        self.ball.move()

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        if self.left_score == 11 or self.right_score == 11:
            self.continue_game = False

class Paddle:
    # An object in this class represents a Paddle that moves
    def __init__(self, x, y, width, height, color, surface):
        # - self is the Paddle object
        # - x, y are the top left corner coordinates of the rectangle of type int
        # - width is the width of the rectangle of type int
        # - height is the heightof the rectangle of type int
        # - surface is the pygame.Surface object on which the rectangle is drawn

        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color(color)
        self.surface = surface
        self.vertical_velocity = 0  # paddle is not moving at the start

    def draw(self):
        # - self is the Paddle object to draw
        pygame.draw.rect(self.surface, self.color, self.rect)

    def set_vertical_velocity(self, vertical_distance):
        # set the vertical velocity of the Paddle object
        # -self is the Paddle object
        # -vertical_distance is the int increment by which the paddle moves vertically
        self.vertical_velocity = vertical_distance

    def move(self):
        # moves the paddle such that paddle does not move outside the window
        # - self is the Paddle object
        edge = None
        self.rect.move_ip(0, self.vertical_velocity)
        if self.rect.bottom >= self.surface.get_height():
            # hit the top edge of the window
            self.rect.bottom = self.surface.get_height()
            edge = "top"
        elif self.rect.top <= 0:
            # hit the bottom edge of the window
            self.rect.top = 0
            edge = "bottom"
        return edge

    def collide(self, x, y):
        # returns the collidepoint
        return self.rect.collidepoint(x, y) == 1

class Ball:
    # An object in this class represents a Ball that moves
    def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, surface):
        # Initialize a ball.
        # - self is the ball to initialize
        # - color is the pygame.Color of the ball
        # - center is a list containing the x and y int
        #   coords of the center of the ball
        # - radius is the int pixel radius of the ball
        # - velocity is a list containing the x and y components
        # - surface is the window's pygame.Surface object

        self.color = pygame.Color(ball_color)
        self.radius = ball_radius
        self.center = ball_center
        self.velocity = ball_velocity
        self.surface = surface

    def move(self):
        # Change the location of the Dot by adding the corresponding
        # speed values to the x and y coordinate of its center
        # - self is the Dot
        size = self.surface.get_size()  # get_size is a method in pygame.Surface class and it returns a tuple (width, height)
        for i in range(0, 2):
            self.center[i] = (self.center[i] + self.velocity[i])
            if self.center[i] < self.radius:  # left or the top edge
                self.velocity[i] = -self.velocity[i]
            elif self.center[i] + self.radius > size[i]:  # right or bottom edge
                self.velocity[i] = - self.velocity[i]

    def draw(self):
        # Draw the dot on the surface
        # - self is the Dot
        pygame.draw.circle(self.surface, self.color, self.center, self.radius)

    def getx_velocity(self):
        # obtains the velocity in the x direction
        return self.velocity[0]

    def get_x_location(self):
        # obtains the x coordinate
        return self.center[0]

    def get_y_location(self):
        # obtains the y coordinate
        return self.center[1]

    def bounce_off_paddle(self):
        # changes direction of the velocity when ball bounces off paddle
        self.velocity[0] = -self.velocity[0]

main()
