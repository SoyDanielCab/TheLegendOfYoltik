import pygame

def game_intro():
    intro = True
    while intro :
        for event in pygame.event.get():
            if event.type == pygame.Quit:
                pygame.quit()
                quit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_e:
            intro = False
        if event.key == pygame.K_q:
            pygame.quit()
            quit()

game_intro()