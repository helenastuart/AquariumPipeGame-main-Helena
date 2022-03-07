# import all of the necessary libraries
import random
import sys, pygame
import os
from pygame.locals import *
import AquariumGraphics

class Food():
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        self.radius = 15

    def move_down(self):
        speed = random.randint(1,5)
        self.y += speed


class PoisonousFood(Food):
    def move_down(self):
        speed = random.randint(5,10)
        self.y += speed


class Pipe():
    def __init__(self, x):
        self.x = x
        self.y = 100
        self.radius = 70
        # list of Food objects which have been added to this pipe
        self.food_pieces = []
        self.poisonous_food = []

    def add_food(self):
        self.food_pieces.append(Food(self.x, 70))

    def add_poisonous_food(self):
        self.poisonous_food.append(PoisonousFood(self.x, 70))

    def move_food(self, boundary_y, player):
        count = 0
        for food in self.food_pieces:
            if food.y > boundary_y:
                self.food_pieces.remove(food)
            food.move_down()

            #check if food has been eaten
            if food.x == player.x:
                if food.y >= player.y and food.y <= player.y+player.height:
                    self.food_pieces.remove(food)
                    count += 1
        return count

    def move_poisonous_food(self, boundary_y, player):
        count = 0
        for food in self.poisonous_food:
            if food.y > boundary_y:
                self.poisonous_food.remove(food)
            food.move_down()

            if food.x == player.x:
                if food.y >= player.y and food.y <= player.y+65:
                    self.poisonous_food.remove(food)
                    count -= 1
        return count

class Fish(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, aquarium_width):
        pygame.sprite.Sprite.__init__(self)
        self.x = x_pos
        self.y = y_pos
        self.aquarium_width = aquarium_width
        self.speed = 15

        self.height = 65
        self.width = 65

        # Load image for player
        # (you can open the image in the assets folder to see what it looks like)
        image_unscaled = pygame.image.load(os.path.join("assets", "goldfish_left.png"))
        image2_unscaled = pygame.image.load(os.path.join("assets", "goldfish_right.png"))

        # Scale the player's character have the specified height and width
        self.image_left = pygame.transform.rotate(pygame.transform.scale(
            image_unscaled, (self.width, self.height)), 0)

        self.image_right = pygame.transform.rotate(pygame.transform.scale(
            image2_unscaled, (self.width, self.height)), 0)

        self.rect = self.image_left.get_rect()
        self.rect = self.image_right.get_rect()
        self.image = self.image_left

    def handle_movement(self, keys_pressed):
        """
        Update player's position according to the key pressed
        """
        if keys_pressed[pygame.K_LEFT]:
            if self.x <= 35+self.speed:
                return
            self.x -= self.speed
            self.image = self.image_left
        elif keys_pressed[pygame.K_RIGHT]:
            if self.x >= self.aquarium_width-40-self.speed:
                return
            self.x += self.speed
            self.image = self.image_right
        else:
            return
        self.rect.x = self.x

class Aquarium():
    def __init__(self, width, height):
        ## initialise pygame
        pygame.init()
        pygame.font.init()

        self.score = 0
        self.game_running = True

        ## game constants
        self.width = width
        self.height = height

        ## player (the fish)
        self.player = Fish(x_pos=width/2,
                           y_pos=height-(height/7),
                           aquarium_width=self.width)

        ## pipes
        self.pipes = []
        self.pipes.append(Pipe(100))
        self.pipes.append(Pipe(400))
        self.pipes.append(Pipe(700))


        ## interface
        self.DISPLAY = AquariumGraphics.setup_display(self.width, self.height)

        ## draw initial board
        self.draw()

    def draw(self):
        # A wrapper around the `AquariumGraphics.draw_board` function that picks all
        # the right components of `self`.
        AquariumGraphics.draw_board(self.DISPLAY, self.width, self.height, self.score,
                                    self.game_running, self.player, self.pipes)

    def game_loop(self):
        while self.game_running:
            # Add food to the pipe
            for pipe in self.pipes:
                int = random.randint(0,100)
                if int == 1 or int == 2:
                    pipe.add_food()
                if int == 50 or int == 51:
                    pipe.add_poisonous_food()

            # Process all events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)

            # Check which key has been pressed (if any) and move player accordingly
            keys_pressed = pygame.key.get_pressed()
            self.player.handle_movement(keys_pressed)

            # Move food down pipe
            for pipe in self.pipes:
                count = pipe.move_food(boundary_y=self.height, player=self.player)
                self.score += count

                count = pipe.move_poisonous_food(boundary_y=self.height, player=self.player)
                self.score += count

            # Refresh the display and loop back
            self.draw()
            pygame.display.update()

            pygame.time.wait(40)

        # Once the game is finished, print the user's score and wait for the `QUIT` event.
        # Note: in its current form, this game doesn't end without the user closing the application
        # since the player can't lose. However, if you extend the game to enable the player to lose,
        # the following code will be useful.
        print('SCORE:  ', self.score)
        while True:
            event = pygame.event.wait()
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            pygame.time.wait(40)
