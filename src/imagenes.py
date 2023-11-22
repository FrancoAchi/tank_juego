import pygame
from pygame.locals import *
from configuracion import bloque_alto, bloque_ancho, TAMANIO_PANTALLA, tamanio_bala


#set imagenes
jugador_imagen = pygame.transform.scale(pygame.image.load("./src/assets/tanque.png"), (bloque_ancho, bloque_alto))
enemigo_imagen= pygame.transform.scale(pygame.image.load("./src/assets/enemigo_2.png"), (bloque_ancho, bloque_alto))
enemigo_imagen_2 = pygame.transform.scale(pygame.image.load("./src/assets/enemigo2.png"), (bloque_ancho, bloque_alto))
enemigo_imagen_3 = pygame.transform.scale(pygame.image.load("./src/assets/enemigo3.png"), (bloque_ancho, bloque_alto))
fondo = pygame.transform.scale(pygame.image.load("./src/assets/ground.jpg"), TAMANIO_PANTALLA) 
imagen_cursor = pygame.transform.scale(pygame.image.load("./src/assets/mira.png"),(30,30))
bala_imagen = pygame.transform.scale(pygame.image.load("./src/assets/bala.png"), tamanio_bala)
menu_fondo = pygame.transform.scale(pygame.image.load("./src/assets/fondo_menu.jpg"), TAMANIO_PANTALLA) 
bomba_imagen = pygame.transform.scale(pygame.image.load("./src/assets/bomba.png"), (40, 40))
cursor_rect = imagen_cursor.get_rect()
