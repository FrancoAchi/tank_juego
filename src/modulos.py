import pygame
from pygame.locals import *
import math
from configuracion import * 
from random import randint, random
from colisiones import detect_collision_circ





#usuario
def terminar():
    """
    Finaliza la aplicación, cerrando la ventana y saliendo del programa
    """
    pygame.quit()
    exit()


def esperar_usuario():
    """
    Espera la interacción del usuario, con los eventos de teclado y salida.

    return:
    - None: Si el usuario presiona la tecla "Esc" o  cierra la ventana, finaliza el programa
    """
    while True:

        for e in pygame.event.get():
            if e.type == QUIT:
                terminar()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    terminar()

                return 

#texto   
def mostrar_texto(superficie:pygame.surface, texto:str, fuente:pygame.font, coordenadas:tuple, color_fuente:tuple, color_fondo=NEGRO)->None:
    """
    Muestra texto en una superficie.

    Parámetros:
    - superficie (pygame.surface): La superficie de Pygame donde se mostrará el texto.
    - texto (str): El texto que se mostrará.
    - fuente (pygame.font): La fuente de Pygame utilizada para renderizar el texto.
    - coordenadas (tuple): Las coordenadas (x, y) donde se centrará el texto.
    - color_fuente (tuple): El color del texto en formato RGB.
    - color_fondo: El color del fondo detrás del texto. Puede ser None para un fondo transparente.

    Return:
    -None
    """
    superficie_texto = fuente.render(texto, True, color_fuente, color_fondo)
    rect_texto = superficie_texto.get_rect()
    rect_texto.center = coordenadas
    superficie.blit(superficie_texto, rect_texto)



#creacion
def crear_modelo(imagen = None, left = 0 , top = 0, width = 40, height = 40, color = (255, 255, 255), dir = 3, borde = 0, radio = -1, velocidad_x = 5, velocidad_y = 5, angulo = 0):
    rec  = pygame.Rect(left, top, width, height)
    """
    Crea un bloque en un juego y devuelve un diccionario con sus propiedades.

    Args:
    - imagen: La imagen del bloque (opcional).
    - left, top: Las coordenadas de la esquina superior izquierda del bloque.
    - width, height: El ancho y alto del bloque.
    - color: El color del bloque si no se proporciona una imagen.
    - dir: La dirección del bloque.
    - borde: Un valor relacionado con el borde.
    - radio: El radio del bloque.
    - velocidad_x, velocidad_y: Las velocidades en las direcciones x e y del bloque.
    - angulo(float): el angulo del personaje

    Returns:
    - Un diccionario con las propiedades del bloque.
    """

    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))
    
    return {"rect": rec,
    "color": color,
    "dir": dir,
    "borde": borde, 
    "radio": radio,
    "velocidad_x": velocidad_x,
    "velocidad_y": velocidad_y,
    "img": imagen,
    "angulo": angulo} 



def mover_rotar_jugador(jugador:dict, angulo:float, mover_izquierda:bool, mover_derecha:bool, mover_arriba:bool, mover_abajo:bool, velocidad:int)->tuple:
    """
    Mueve y rota al jugador según las teclas presionadas y la posición del mouse.

    Args:
    - jugador (dict): Diccionario que representa al jugador con las propiedades:
        - "img": Imagen del jugador.
        - "rect": Rectángulo que delimita la posición y tamaño del jugador.
    - angulo (float): Ángulo adicional que se suma al ángulo actual del jugador.
    - mover_izquierda (bool): Indica si la tecla de movimiento hacia la izquierda está presionada.
    - mover_derecha (bool): Indica si la tecla de movimiento hacia la derecha está presionada.
    - mover_arriba (bool): Indica si la tecla de movimiento hacia arriba está presionada.
    - mover_abajo (bool): Indica si la tecla de movimiento hacia abajo está presionada.
    -velocidad(int): Velocidad del jugador

    Returns:
    - Tupla con la imagen rotada del jugador y el nuevo rectángulo del jugador.
    """
   
    if mover_izquierda and  jugador["rect"].left >= velocidad:
        jugador["rect"].left -= velocidad
    if mover_derecha and jugador["rect"].right <= (ANCHO - velocidad):
        jugador["rect"].left += velocidad
    if mover_arriba and jugador["rect"].top >= velocidad:
        jugador["rect"].top -= velocidad
    if mover_abajo and jugador["rect"].bottom <= (ALTO - velocidad):
        jugador["rect"].top += velocidad

    pos = pygame.mouse.get_pos()
    x_dist = pos[0] - jugador["rect"].centerx
    y_dist = -(pos[1] - jugador["rect"].centery)
    jugador["angulo"] = math.degrees(math.atan2(y_dist, x_dist))

    jugador_rotado = pygame.transform.rotate(jugador["img"], jugador["angulo"] + angulo)
    jugador["rect"] = jugador_rotado.get_rect(center=jugador["rect"].center)
    
    return jugador_rotado, jugador["rect"]



#--------------------------------------------------


def dibujar_enemigos(superficie:pygame.surface, enemigos:list)-> None:
    """
    Dibuja enemigos en una superficie.

    Args:
    -superficie(pygame.surface): superficie donde se van a dibujar los enemigos
    -enemigos(list): lista de enemigos que se va a dibujar en pantalla

    Return:
    -None
    """

    try:
        for enemigo in enemigos:
            
            if enemigo["img"]:
                superficie.blit(enemigo["img"], enemigo["rect"])
            else:
                pygame.draw.rect(superficie, enemigo["color"], enemigo["rect"], enemigo["edge"], enemigo["radio"])
    except:
        print("Error al cargar enemigos")

def dibujar_enemigos_y(superficie, enemigos_y):
    dibujar_enemigos(superficie, enemigos_y)


#--------------------------------------------------------

def cargar_lista_enemigos(enemigos:list, cantidad:int, imagen= None)-> None:
    """
    Carga una lista de enemigos con propiedades aleatorias.

    Args:
    -enemigos(list): Lista que se utilizara para generar enemigos .
    -cantidad(int): Número de enemigos que se quieran generar.
    -imagen: imagen opcional de los enemigos.

    Return:
    -None
    """
    for i in range(cantidad):
        tamanio_enemigo =(randint(tamanio_min_enemigo, tamanio_max_enemigo))
        velocidad_enemigo = movimiento_enemigo
        enemigos.append(crear_modelo(imagen, randint(0, ANCHO - tamanio_enemigo),randint(- ALTO, - tamanio_enemigo), bloque_ancho, bloque_alto, velocidad_y= velocidad_enemigo, velocidad_x= velocidad_enemigo))

def cargar_lista_enemigos_y(enemigos_y:list, cantidad:int, imagen=None)-> None:
    cargar_lista_enemigos(enemigos_y, cantidad, imagen)

def crear_bala(imagen:pygame.image, jugador_rect:pygame.Rect, tamanio_bala:tuple, velocidad_bala:int)->dict:
    """
    Crea un proyectil (bala) a partir de la imagen proporcionada y la posición del jugador.

    Args:
    -imagen: Imagen de la bala.
    -jugador["rect"]: rectangulo del jugador por donde va a dispararse la bala.
    -tamanio_bala(tuple): Tamaño de la bala, representado como una tupla.
    -velocidad_bala(int): Velocidad de movimiento de la bala.

    Return:
    -Diccionario con las propiedades del proyectil(bala).

    """
    try:
        centro_jugador = jugador_rect.center
        bala_w, bala_h = tamanio_bala
        
        # Ajustar las coordenadas iniciales de la bala al centro del jugador
        x_inicial = centro_jugador[0] - bala_w // 2
        y_inicial = centro_jugador[1] - bala_h
        
        return crear_modelo(imagen, x_inicial, y_inicial, tamanio_bala[0], tamanio_bala[1],
                            None, velocidad_y=velocidad_bala, velocidad_x=velocidad_bala, angulo=0)
    except:
        print("error al generar proyectil")

def mostrar_texto_boton(superficie,  texto,x, y, font_size = 36, color = (0, 0, 0)):
    """
    Muestra texto en una superficie en la posición especificada.

    Args:
    - superficie: Superficie de Pygame donde se mostrará el texto.
    - texto: Texto que se mostrará en el botón.
    - x, y: Coordenadas (x, y) donde se posicionará el centro del texto.
    - font_size: Tamaño de la fuente del texto (por defecto, 36).
    - color: Color del texto (por defecto, negro).

    Returns:
    - None
    """
    fuente = pygame.font.SysFont("Arial Black", font_size)
    render = fuente.render(texto, True, color)
    rect_texto = render.get_rect(center = (x, y))
    superficie.blit(render, rect_texto)

def crear_boton(screen: pygame.surface, rect: pygame.Rect, texto: str, color_normal: tuple, color_secundario: tuple) -> None:
    """
    Crea un botón y lo muestra en la pantalla.

    Args:
    - screen (pygame.surface): Superficie de Pygame donde se mostrará el botón.
    - rect (pygame.Rect): Rectángulo que define la posición y el tamaño del botón.
    - texto (str): Texto que se mostrará en el botón.
    - color_normal (tuple): Color del botón cuando no está resaltado.
    - color_secundario (tuple): Color del botón cuando está resaltado.

    Return:
    - None
    """
    try:
        # Obtener la posición del mouse
        posicion_mouse = pygame.mouse.get_pos()

        # Verificar si el mouse está sobre el botón y ajustar el color en consecuencia
        if rect.collidepoint(posicion_mouse):
            pygame.draw.rect(screen, color_secundario, rect, border_radius=30)
        else:
            pygame.draw.rect(screen, color_normal, rect, border_radius=30)

        # Mostrar el texto en el centro del botón
        mostrar_texto_boton(screen, texto, rect.centerx, rect.centery)
    except Exception as e:
        print(f"Error al crear y mostrar el botón: {e}")






def menu_principal(screen:pygame.surface, fuente:pygame.font, fondo:pygame.image ,boton_1:pygame.Rect, boton_2:pygame.Rect, boton_3:pygame.Rect, color_principal=(0,0,0), color_secundario=(0,0,0)):
    """
    Muestra el menú principal del juego.

    Args:
    - screen(pygame.surface): La superficie donde se mostrará el menú.
    - fuente(pygame.font): La fuente de texto utilizada para el título del menú.
    - fondo(pygame.image): La imagen del fondo del menú.
    - boton_1(pygame.Rect): Rectángulo que representa el botón "Jugar".
    - boton_2(pygame.Rect): Rectángulo que representa el botón "Controles".
    - boton_3(pygame.Rect): Rectángulo que representa el botón "Salir".
    - color_principal(tuple): El color principal del botón.
    - color_secundario(tuple): El color secundario del botón al ser seleccionado.
    """
    

    pygame.mouse.set_visible(True)
    menu_principal = True
    try:
        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                        terminar()

                if e.type == MOUSEBUTTONDOWN:
                    if e.button == 1:
                        cursor = e.pos
                        if boton_1.collidepoint(cursor[0], cursor[1]):     
                                return None
                        elif boton_2.collidepoint(cursor[0], cursor[1]):
                                menu_principal = False
                        elif boton_3.collidepoint(cursor[0], cursor[1]):
                                terminar()
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        menu_principal = True  

            screen.blit(fondo, ORIGIN)

            if menu_principal:
                mostrar_texto(screen, "TANQUES", fuente, (ANCHO // 2, 20), AZUL, color_fondo=None)
                crear_boton(screen, boton_1, "Jugar", color_principal, color_secundario)
                crear_boton(screen, boton_2, "Controles", color_principal, color_secundario)
                crear_boton(screen, boton_3, "Salir", color_principal, color_secundario)
            else:
                # Si está en la pantalla de controles, muestra la imagen y un botón para volver al menú principal
                controles = pygame.transform.scale(pygame.image.load("./src/assets/controles.jpg"), TAMANIO_PANTALLA)
                screen.blit(controles, ORIGIN)
            pygame.display.flip()
    except Exception as e:
        print(f"Error en menu_princiapl: {e}")

def pantalla_final(screen:pygame.surface, pantalla_final:pygame.image, fuente:pygame.font, contador_maximo:int)-> None:
    """
    Muestra la pantalla final del juego.

    Args:
    - screen:(pygame.surface) La superficie donde se mostrará la pantalla final.
    - pantalla_final(pygame.image): La imagen de fondo de la pantalla final.
    - fuente(pygame.font): La fuente de texto utilizada para mostrar información en la pantalla final.

    Returns:
    - None
    """
    try:
       
        screen.blit(pantalla_final, ORIGIN)

        
        mostrar_texto(screen, "Has perdido", fuente, (ANCHO // 2, 20), AZUL, color_fondo=None)
        mostrar_texto(screen, f"Maximo puntaje: {contador_maximo}", fuente, CENTRO_PANTALLA, AZUL, color_fondo=None)
        mostrar_texto(screen, "Presione una tecla para continuar", fuente, (ANCHO // 2, ALTO - 30), AMARILLO, color_fondo=None)

        
        pygame.display.flip()
    except Exception as e:
        print(f"Error al cargar la pantalla final: {e}")

  



def dibujar_item(superficie:pygame.surface, items:list)-> None:
    """
    Dibuja enemigos que se mueven en el eje Y en una superficie.

    Args:
    - superficie (pygame.surface): Superficie donde se van a dibujar los enemigos.
    - enemigos_y (list): Lista de enemigos que se van a dibujar en pantalla.

    Return:
    - None
    """
    try:
        for item in items:
            if item["img"]:
                superficie.blit(item["img"], item["rect"])
            else:
                pygame.draw.rect(superficie, item["color"], item["rect"], item["edge"], item["radio"])
    except:
        print("Error al cargar enemigos en el eje Y")



def colision_proyectil_enemigo_y(rafaga:list, contador:int, texto_contador, enemigos_y:list, balas:list, sonido, reproducir:bool, fuente:pygame.font, cantidad_enemigos:int, imagen:pygame.image)-> tuple:
    """
    Maneja las colisiones entre proyectiles y enemigos de tipo "y".

    Parámetros:
    - rafaga (list): Lista que indica si se debe realizar una rafaga de proyectiles.
    - contador (int): Contador actual de puntos.
    - texto_contador: Objeto de texto que muestra el contador.
    - enemigos_y (list): Lista de enemigos de tipo "y".
    - balas (list): Lista de proyectiles.
    - sonido (pygame.mixer.Sound): Objeto de sonido para reproducir al haber colisión.
    - reproducir (bool): Indica si se debe reproducir el sonido al haber colisión.
    - fuente (pygame.font): Objeto de fuente para renderizar texto.
    - cantidad_enemigos (int): Cantidad de enemigos a cargar en caso de eliminar todos los enemigos "y".
    - imagen (pygame.image): Imagen para cargar enemigos en caso de eliminar todos los enemigos "y".

    Devuelve una tupla con el contador actualizado y el objeto de texto del contador actualizado.
    """
    if rafaga:
        for bala in balas[:]:
            colision = False
            for enemigo_y in enemigos_y[:]:
                if detect_collision_circ(enemigo_y["rect"], bala["rect"]):
                    enemigos_y.remove(enemigo_y)
                    contador += 10
                    texto_contador = fuente.render(f"Puntos: {contador}", True, ROJO)
                    rect_texto = texto_contador.get_rect(topleft = (30, 40))
                    colision = True
                    sonido.play()
                    if reproducir:
                            sonido.play()                    
                    if len(enemigos_y) == 0:
                                
                            cargar_lista_enemigos_y(enemigos_y, cantidad_enemigos, imagen)                               
            if colision == True:
                balas.remove(bala)
        return  contador, texto_contador


def colision_proyectil_enemigo(rafaga, contador, texto_contador, enemigos, balas, sonido, reproducir, fuente, cantidad_enemigos, imagen):
        if rafaga:
            for bala in balas[:]:
                colision = False
                for enemigo in enemigos[:]:
                    if detect_collision_circ(enemigo["rect"], bala["rect"]):
                        enemigos.remove(enemigo)
                        contador += 10
                        texto_contador = fuente.render(f"Puntos: {contador}", True, ROJO)
                        rect_texto = texto_contador.get_rect(topleft = (30, 40))
                        colision = True
                        sonido.play()
                        if reproducir:
                                sonido.play()                    
                        if len(enemigos) == 0:
                                    
                                cargar_lista_enemigos_y(enemigos, cantidad_enemigos, imagen)                               
                if colision == True:
                    balas.remove(bala)
        return  contador, texto_contador

