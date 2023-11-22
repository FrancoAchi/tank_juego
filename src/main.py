try:
    import pygame
    from pygame.locals import *
    from configuracion import *
    from modulos import *
    from colisiones import *
    import random
    from jason import cargar_puntajes, guardar_puntajes
    from imagenes import *
    
except:
    print("error falta de modulo")


def mover_enemigos_y(enemigos_y, movimiento_enemigo):
        for enemigo_y in enemigos_y[:]:
            enemigo_y["rect"].move_ip(0, movimiento_enemigo)  

            if enemigo_y["rect"].top > ALTO:
                enemigo_y["rect"].y = -enemigo_y["rect"].height
                enemigo_y["rect"].x = random.randint(0, ANCHO - enemigo_y["rect"].width)


def mover_enemigos(enemigos, movimiento_enemigo):
        for enemigo in enemigos[:]:
            enemigo["rect"].move_ip(movimiento_enemigo, 0)  
            
            if enemigo["rect"].left > ANCHO:
                enemigo["rect"].x = -enemigo["rect"].width
                enemigo["rect"].y = random.randint(0, ALTO - enemigo["rect"].height)


        



pygame.init()

#reloj
clock = pygame.time.Clock()


#pantalla principal
screen = pygame.display.set_mode(TAMANIO_PANTALLA)
pygame.display.set_caption("Tanks")

#sonidos
explosion_sonido = pygame.mixer.Sound("./src/assets/explosion.wav")
explosion_sonido.set_volume(0.1)
fin_del_juego = pygame.mixer.Sound("./src/assets/game_over.wav")
poder_sonido = pygame.mixer.Sound("./src/assets/power_up.wav")
poder_sonido.set_volume(0.3)

#musica
juego_musica = pygame.mixer.music.load("./src/assets/nivel.mp3")
juego_musica = pygame.mixer.music.set_volume(0.1)
reproducir_musica = True


#evento:
evento_aumento_velocidad =  pygame.USEREVENT + 1 
pygame.time.set_timer(evento_aumento_velocidad, 10000)

#crear personajes
jugador = crear_modelo(jugador_imagen, ANCHO // 2, ALTO // 2, bloque_ancho, bloque_alto, ROJO, angulo= 0)

#fuente
fuente = pygame.font.SysFont(None, 48)

#botones
centro_x = screen.get_width() // 2
boton_comenzar = pygame.Rect(centro_x - ancho_del_boton // 2, 150, ancho_del_boton, alto_del_boton)
boton_instrucciones = pygame.Rect(centro_x - ancho_del_boton // 2, 250, ancho_del_boton, alto_del_boton)
boton_salir = pygame.Rect(centro_x - ancho_del_boton // 2, 350, ancho_del_boton, alto_del_boton)

#contadores
contador_maximo = 0
contador = 0
puntajes = cargar_puntajes()
#trucos
truco_bomba = False
truco_velocidad = False



angulo = 360

while True:
    #menu
    menu_principal(screen, fuente, menu_fondo,boton_comenzar, boton_instrucciones, boton_salir, AZUL, VERDE)


    #juego
    vidas = 3
    contador = 0
    texto_contador = fuente.render(f"Puntos: {contador}", True, ROJO)
    rect_texto = texto_contador.get_rect(topleft = (30, 40))
    vidas_texto = fuente.render(f"Vidas: {vidas}", True, ROJO)
    rect_vidas_texto = vidas_texto.get_rect(topright  = (ANCHO - 30, 40))
    pygame.mouse.set_visible(False)


    #musica
    juego_musica = pygame.mixer.music.play(-1)
    colision = False
    cantidad_enemigos = 7
    running = True
    enemigos = []
    enemigos_y = []
    balas = []
    rafaga = True
    items = []
    


    cargar_lista_enemigos(enemigos, cantidad_enemigos, enemigo_imagen)
    cargar_lista_enemigos_y(enemigos_y, cantidad_enemigos, enemigo_imagen_3)



    while running:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == QUIT:
                running = False

            if e.type == evento_aumento_velocidad:
                tamanio_item = 40
                item_velocidad = 1
                items.append(crear_modelo(bomba_imagen, randint(0, ANCHO - tamanio_item), randint(0, ALTO - tamanio_item), tamanio_item, tamanio_item, item_velocidad))
                
            
            if e.type == KEYDOWN:

                if e.key == K_SPACE:
                
                    if rafaga:
                        proyectil = crear_bala(bala_imagen, jugador["rect"], tamanio_bala, velocidad_bala)
                        balas.append(proyectil)
                if e.key == K_w:
                    mover_arriba = True
                    mover_abajo = False

                if e.key == K_s:
                    mover_abajo = True
                    mover_arriba = False

                if e.key == K_d:
                    mover_derecha = True
                    mover_izquierda = False

                if e.key == K_a:
                    mover_izquierda = True
                    mover_derecha = False

                if e.key == K_b:
                    truco_bomba = not truco_bomba
                    if truco_bomba:
                        explosion_sonido.play()
                        enemigos.clear()
                        enemigos_y.clear()
                    else:
                        # Cargar nuevos enemigos después de desactivar el truco
                        if len(enemigos) == 0:
                            cargar_lista_enemigos(enemigos, cantidad_enemigos, enemigo_imagen_2)
                        if len(enemigos_y) == 0:
                            cargar_lista_enemigos_y(enemigos_y, cantidad_enemigos, enemigo_imagen_3)
                
                if e.key == K_v:       
                    truco_velocidad = not truco_velocidad

                  

                if e.key == K_m:
                    if reproducir_musica:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    
                    reproducir_musica = not reproducir_musica

                if e.key == K_p:
                    if reproducir_musica:
                        pygame.mixer.music.pause()
                        pass
                    mostrar_texto(screen, "PAUSA", fuente, CENTRO_PANTALLA, AZUL, color_fondo= None)
                    pygame.display.flip()

                    esperar_usuario()
                    if reproducir_musica:
                        pygame.mixer.music.unpause()
                


            if e.type == KEYUP:
                if e.key == K_w:
                    mover_arriba = False

                if e.key == K_s:
                    mover_abajo = False

                if e.key == K_d:
                    mover_derecha = False

                if e.key == K_a:
                    mover_izquierda = False

                if e.key == K_v:       
                    truco_velocidad = False

            if e.type == MOUSEBUTTONDOWN:
                
                if e.button == 1:
                
                    if rafaga:
                        proyectil = crear_bala(bala_imagen, jugador["rect"], tamanio_bala, velocidad_bala)
                        balas.append(proyectil)
                        
                print(rafaga)

        #mover jugador
        if not truco_velocidad:
            jugador_rotado, jugador_rect = mover_rotar_jugador(jugador,angulo, mover_izquierda, mover_derecha, mover_arriba, mover_abajo, velocidad)
        elif truco_velocidad:
            velocidad += 1

        #muevo enemigos
        mover_enemigos_y(enemigos_y, movimiento_enemigo)
        mover_enemigos(enemigos, movimiento_enemigo)

        #muevo el proyectil---------------------
        if rafaga:
            for bala in balas[:]:
                velocidad_x = bala["velocidad_x"] * math.sin(math.radians(jugador["angulo"]))
                velocidad_y = bala["velocidad_y"] * math.cos(math.radians(jugador["angulo"]))


                bala["rect"].move_ip(velocidad_x, velocidad_y)

                # Verificar si la bala se sale de la pantalla
                if bala["rect"].right < 0 or bala["rect"].left > ANCHO or bala["rect"].bottom < 0  or bala["rect"].top > ALTO:
                    balas.remove(bala)
                print("Velocidad_x:", velocidad_x)
                print("Velocidad_y:", velocidad_y)
                print("Ángulo:", jugador["angulo"])
        

        #colision de enmigos con el jugador-----------------------------------
        for enemigo in enemigos:
            if detect_collision(enemigo["rect"], jugador["rect"]):
                enemigos.remove(enemigo)
                if vidas > 1:
                    vidas -= 1
                    vidas_texto = fuente.render(f"Vidas: {vidas}", True, ROJO)
                    rect_vidas_texto = vidas_texto.get_rect(topright =  (ANCHO -30, 40))
                else:
                    running = False

                explosion_sonido.play()
                if reproducir_musica:
                    explosion_sonido.play()

        for enemigo_y in enemigos_y:
            if detect_collision(enemigo_y["rect"], jugador["rect"]):
                enemigos_y.remove(enemigo_y)
                if vidas > 1:
                    vidas -= 1
                    vidas_texto = fuente.render(f"Vidas: {vidas}", True, ROJO)
                    rect_vidas_texto = vidas_texto.get_rect(topright =  (ANCHO -30, 40))
                else:
                    running = False

                explosion_sonido.play()
                if reproducir_musica:
                    explosion_sonido.play()
                
        #colision del item
        for item in items:
            if detect_collision(item["rect"], jugador["rect"]):
                poder_sonido.play()
                velocidad += item ["velocidad_y"]
                items.remove(item)

        #colision proyectiles a enemigos
        contador, texto_contador = colision_proyectil_enemigo(rafaga, contador, texto_contador, enemigos, balas, explosion_sonido, reproducir_musica, fuente, cantidad_enemigos, enemigo_imagen_2)
        contador, texto_contador = colision_proyectil_enemigo_y(rafaga, contador, texto_contador, enemigos_y, balas, explosion_sonido, reproducir_musica, fuente, cantidad_enemigos, enemigo_imagen_3)

        
        #----------------------------------------------------------------------------------------
        x, y = pygame.mouse.get_pos()
        screen.blit(fondo, ORIGIN)
        screen.blit(jugador_rotado, jugador_rect)
        screen.blit(imagen_cursor, (x - cursor_rect.width / 2, y - cursor_rect.height/2 ))
        dibujar_enemigos(screen, enemigos)
        dibujar_enemigos_y(screen, enemigos_y)
        dibujar_item(screen, items)
        screen.blit(texto_contador, rect_texto)
        screen.blit(vidas_texto, rect_vidas_texto)
 
        if rafaga:
            for bala in balas:
                screen.blit(bala["img"], bala["rect"])
                

    
    
        pygame.display.flip()

    if contador > contador_maximo:
        contador_maximo = contador

    puntajes.append(contador)
    guardar_puntajes(puntajes)

    velocidad = velocidad_normal
    pygame.mixer.music.stop()
    fin_del_juego.play()

    pantalla_final(screen, menu_fondo, fuente, contador_maximo)

    esperar_usuario()

