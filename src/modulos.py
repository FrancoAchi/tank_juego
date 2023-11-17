import pygame
from pygame.locals import *
import math
from configuracion import * 
from random import randint





#usuario
def terminar():
    pygame.quit()
    exit()


def wait_user():
    while True:

        for e in pygame.event.get():
            if e.type == QUIT:
                terminar()
            if e.type == KEYDOWN:
                if e.key  == K_s or e.key == K_ESCAPE:
                    terminar()

                return

#texto   
def mostrar_texto(surface, text, font, coordenadas, color_fuente, color_fondo = (0,0,0)):
        surf_text = font.render(text, True, color_fuente, color_fondo)
        rect_text = surf_text.get_rect()
        rect_text.center = coordenadas
        surface.blit(surf_text, rect_text)



#creacion
def crear_modelo(imagen = None, left = 0 , top = 0, width = 40, height = 40, color = (255, 255, 255), dir = 3, edge = 0, radio = -1, speed_x = 5, speed_y = 5, angulo = 0):
    rec  = pygame.Rect(left, top, width, height)
    """
    Crea un bloque en un juego y devuelve un diccionario con sus propiedades.

    Args:
    - imagen: La imagen del bloque (opcional).
    - left, top: Las coordenadas de la esquina superior izquierda del bloque.
    - width, height: El ancho y alto del bloque.
    - color: El color del bloque si no se proporciona una imagen.
    - dir: La dirección del bloque.
    - edge: Un valor relacionado con el borde.
    - radio: El radio del bloque.
    - speed_x, speed_y: Las velocidades en las direcciones x e y del bloque.
    - angle: el angulo del personaje

    Returns:
    - Un diccionario con las propiedades del bloque.
    """

    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))
    
    return {"rect": rec,
    "color": color,
    "dir": dir,
    "edge": edge, 
    "radio": radio,
    "speed_x": speed_x,
    "speed_y": speed_y,
    "img": imagen,
    "angulo": angulo} 



def mover_rotar_jugador(jugador, move_left, move_right, move_up, move_down):
    """
    Mueve y rota al jugador según las teclas presionadas y la posición del mouse.

    Args:
    - jugador (dict): Diccionario que representa al jugador con las propiedades:
        - "img": Imagen del jugador.
        - "rect": Rectángulo que delimita la posición y tamaño del jugador.
    - move_left (bool): Indica si la tecla de movimiento hacia la izquierda está presionada.
    - move_right (bool): Indica si la tecla de movimiento hacia la derecha está presionada.
    - move_up (bool): Indica si la tecla de movimiento hacia arriba está presionada.
    - move_down (bool): Indica si la tecla de movimiento hacia abajo está presionada.

    Returns:
    - Tupla con la imagen rotada del jugador y el nuevo rectángulo del jugador.
    """
   
    if move_left and  jugador["rect"].left >= speed:
        jugador["rect"].left -= speed
    if move_right and jugador["rect"].right <= (WIDTH - speed):
        jugador["rect"].left += speed
    if move_up and jugador["rect"].top >= speed:
        jugador["rect"].top -= speed
    if move_down and jugador["rect"].bottom <= (HEIGHT - speed):
        jugador["rect"].top += speed

    pos = pygame.mouse.get_pos()
    x_dist = pos[0] - jugador["rect"].centerx
    y_dist = -(pos[1] - jugador["rect"].centery)
    jugador["angulo"] = math.degrees(math.atan2(y_dist, x_dist))

    jugador_rotado = pygame.transform.rotate(jugador["img"], jugador["angulo"] + 90)
    jugador["rect"] = jugador_rotado.get_rect(center=jugador["rect"].center)
    
    return jugador_rotado, jugador["rect"]




def dibujar_enemigos(surface, enemigos):
    for enemigo in enemigos:
        
        if enemigo["img"]:
            surface.blit(enemigo["img"], enemigo["rect"])
        else:
            pygame.draw.rect(surface, enemigo["color"], enemigo["rect"], enemigo["edge"], enemigo["radio"])


def cargar_lista_enemigos(enemigos, cantidad, imagen= None):
    for i in range(cantidad):
        tamanio_enemigo =(randint(tamanio_min_enemigo, tamanio_max_enemigo))
        velocidad_enemigo = velocidad_enemigo_max
        enemigos.append(crear_modelo(imagen, randint(0, WIDTH - tamanio_enemigo),randint(- HEIGHT, - tamanio_enemigo), BLOCK_WIDTH, BLOCK_HEIGHT, speed_y= velocidad_enemigo, speed_x= velocidad_enemigo))


def crear_bala(imagen, jugador_rect, tamanio_bala, velocidad_bala):
    midtop = jugador_rect.midtop
    return crear_modelo(imagen, midtop[0] - tamanio_bala[0] // 2, midtop[1] - tamanio_bala[1], tamanio_bala[0], tamanio_bala[1], None, speed_y=velocidad_bala, speed_x= velocidad_bala)

# def trayectoria_bala(jugador,imagen,):
#     mover_rotar_jugador(jugador)
#     bala = crear_bala(imagen)
    




# def crear_bala(imagen, jugador_rect, tamanio_bala, velocidad_bala ):
#     midbottom =  jugador_rect.midbottom
#     bala_w, bala_h =  tamanio_bala 
#     return crear_modelo(imagen, midbottom[0] - bala_w // 2, midbottom[1] - bala_h, bala_w, bala_h, speed_y= velocidad_bala, speed_x= velocidad_bala)
                            



#mascaras

