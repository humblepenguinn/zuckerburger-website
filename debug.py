import pygame

pygame.init()
font = pygame.font.Font(None,30)

def debug(info,y = 10, x = 10):
    """
    It takes a string, and displays it on the screen

    :param info: The information you want to display
    :param y: The y coordinate of the top left corner of the text, defaults to 10 (optional)
    :param x: The x coordinate of the top left corner of the text, defaults to 10 (optional)
    """
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info),True,'White')
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    pygame.draw.rect(display_surface,'Black',debug_rect)
    display_surface.blit(debug_surf,debug_rect)