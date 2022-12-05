import pygame
from src.field import Field

class Game():
    def __init__(self, settings):
        # setup pygame
        self.window = pygame.display.set_mode(settings["WINDOW_SIZE"])
        self.screen = pygame.Surface(settings["SCREEN_SIZE"])
        self.settings = settings
        self.clock = pygame.time.Clock()

        self.field = Field(settings['GHOST_SHAPE'])

        # main cycle
        self.run()
    
    def run(self):
        run = True
        events = {
            'left': False,
            'right': False,
            'down': False,
            'rotate': False,
            'drop': False
        }
        while run:
            # screen clear
            self.window.fill((0,0,0))
            self.screen.fill((0,0,0))

            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        events['right'] = True
                    elif event.key == pygame.K_a:
                        events['left'] = True
                    elif event.key == pygame.K_s:
                        events['down'] = True
                    elif event.key == pygame.K_w:
                        events['rotate'] = True
                    elif event.key == pygame.K_SPACE:
                        events['drop'] = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        events['right'] = False
                    elif event.key == pygame.K_a:
                        events['left'] = False
                    elif event.key == pygame.K_s:
                        events['down'] = False
                    elif event.key == pygame.K_w:
                        events['rotate'] = False
                    elif event.key == pygame.K_SPACE:
                        events['drop'] = False

            # field update
            field = self.field.update(events)
            self.screen.blit(field, (0, 0))
            
            # clock
            self.clock.tick(self.settings["FPS"])

            # window
            self.window.blit(pygame.transform.scale(self.screen, self.settings["WINDOW_SIZE"]), (0, 0))
            pygame.display.update()
            
        # quit if closed
        pygame.quit()
