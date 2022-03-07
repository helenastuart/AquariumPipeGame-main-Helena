import pygame
import os
import AquariumEngine

# This module handles the graphical interface. This includes drawing the shapes and
# displaying the text that together make the game window.

# display constants
fontsize = 25
game_side_padding = 25
top_offset = 25
bottom_spacing = 65

# colour constants
BORDER_COLOUR = (13, 161, 146)
CREAM = (242, 235, 211)
BACKGROUND_COLOUR = (19, 189, 172)
WHITE = (255, 255, 255)
PIPE_COLOUR = (131, 214, 206)
RED = (223, 59, 26)
GREEN = (26, 105, 50)


def setup_display(game_width, game_height):
    window_width = 2 * game_side_padding + game_width
    window_height = 2 * game_side_padding + top_offset + bottom_spacing + game_height
    display = pygame.display.set_mode((window_width, window_height), 0, 32)
    pygame.display.set_caption('Aquarium Pipe Game')
    gamefont = pygame.font.Font(None, fontsize)
    return (display, gamefont)

def draw_board(
    game_display,
    game_width,
    game_height,
    score,
    game_running,
    player,
    pipes
):
    (display, gamefont) = game_display
    display.fill(BACKGROUND_COLOUR)

    coral = pygame.image.load(os.path.join("assets", "coral.jfif"))
    coral = pygame.transform.rotate(pygame.transform.scale(coral, (game_width, game_height)), 0)
    display.blit(coral, (game_side_padding, top_offset))

    # draw all food
    for pipe in pipes:
        for food_item in pipe.food_pieces:
            pygame.draw.circle(display, BORDER_COLOUR, (pipe.x + (pipe.radius / 2), food_item.y),
                           food_item.radius, 0)

        for food_item in pipe.poisonous_food:
            pygame.draw.circle(display, RED, (pipe.x + (pipe.radius / 2), food_item.y),
                           food_item.radius, 0)

    # draw over food overlapping border
    pygame.draw.rect(display, BACKGROUND_COLOUR,
                     (game_side_padding,
                      top_offset + game_height,
                      game_width,
                      50)
                     )

    pygame.draw.rect(display, BACKGROUND_COLOUR,
                     (game_side_padding,
                      0,
                      game_width,
                      top_offset)
                     )

    # display player's score
    score_surf = gamefont.render('SCORE: ' + str(score), False, CREAM)
    score_x = game_side_padding
    score_y = 2 * game_side_padding + top_offset + game_height
    display.blit(score_surf, (score_x, score_y))

    # display pipes
    num_pipes = len(pipes)
    position = game_width/num_pipes
    for pipe in pipes:
        pygame.draw.rect(display, PIPE_COLOUR, (pipe.x, pipe.y, pipe.radius, 330))

    # display player
    display.blit(player.image, (player.x, player.y))

    # draw border
    pygame.draw.rect(display, BORDER_COLOUR,
                     (game_side_padding,
                      top_offset,
                      game_width,
                      game_height
                      ),
                     10)
