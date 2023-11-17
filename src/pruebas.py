import pygame
import math

# Inicializar Pygame
pygame.init()

# Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Rectángulo Rotativo')

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)
        self.angle = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5

        # Rotar el rectángulo
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.rect = rotated_image.get_rect(center=self.rect.center)

        # Dibujar el rectángulo en la pantalla
        screen.fill(BLACK)
        screen.blit(rotated_image, self.rect.topleft)

        pygame.display.flip()

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Disparar proyectil en la dirección actual
            bullet = pygame.Surface((10, 5))
            bullet.fill(WHITE)
            bullet_rect = bullet.get_rect()
            bullet_rect.center = player.rect.center

            # Calcular la dirección del proyectil
            radian_angle = math.radians(player.angle)
            bullet_speed = 5
            bullet_velocity = [bullet_speed * math.cos(radian_angle), -bullet_speed * math.sin(radian_angle)]

            while bullet_rect.colliderect(player.rect):
                bullet_rect.move_ip(bullet_velocity)
                screen.fill(BLACK)
                rotated_image = pygame.transform.rotate(player.image, player.angle)
                screen.blit(rotated_image, player.rect.topleft)
                screen.blit(bullet, bullet_rect.topleft)
                pygame.display.flip()
                clock.tick(60)

    all_sprites.update()
    clock.tick(60)

pygame.quit()
