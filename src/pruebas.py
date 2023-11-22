try:
    import pygame
    from pygame.locals import *
    from configuracion import *
    from modulos import *
    from colisiones import *
    import random
    
    
except:
    print("error falta de modulo")








pygame.init()

#reloj
clock = pygame.time.Clock()


#pantalla principal
screen = pygame.display.set_mode(TAMANIO_PANTALLA)
pygame.display.set_caption("Tanks")


#set imagenes
jugador_imagen = pygame.transform.scale(pygame.image.load("./src/assets/tanque.png"), (bloque_ancho, bloque_alto))
enemigo_imagen= pygame.transform.scale(pygame.image.load("./src/assets/enemigo_2.png"), (bloque_ancho, bloque_alto))
enemigo_imagen_2 = pygame.transform.scale(pygame.image.load("./src/assets/enemigo2.png"), (bloque_ancho, bloque_alto))
enemigo_imagen_3 = pygame.transform.scale(pygame.image.load("./src/assets/enemigo3.png"), (bloque_ancho, bloque_alto))
fondo = pygame.transform.scale(pygame.image.load("./src/assets/ground.jpg"), TAMANIO_PANTALLA) 
imagen_cursor = pygame.transform.scale(pygame.image.load("./src/assets/mira.png"),(30,30))
bala_imagen = pygame.transform.scale(pygame.image.load("./src/assets/bala.png"),tamanio_bala)
menu_fondo = pygame.transform.scale(pygame.image.load("./src/assets/fondo_menu.jpg"), TAMANIO_PANTALLA) 
cursor_rect = imagen_cursor.get_rect()

#sonidos
explosion_sonido = pygame.mixer.Sound("./src/assets/explosion.wav")
explosion_sonido.set_volume(0.1)
fin_del_juego = pygame.mixer.Sound("./src/assets/game_over.wav")

#musica
juego_musica = pygame.mixer.music.load("./src/assets/nivel.mp3")
juego_musica = pygame.mixer.music.set_volume(0.1)



reproducir_musica = True





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

#trucos
truco_bomba = False

velocidadx = 3


angulo = 360

while True:

    # screen.blit(menu_fondo, ORIGIN)

    # mostrar_texto(screen, "TANQUES", font, (WIDTH // 2, 20), BLUE)
    # pygame.display.flip()

    menu_principal(screen, fuente, menu_fondo,boton_comenzar, boton_instrucciones, boton_salir, AZUL, VERDE)


    #juego
    vidas = 3
    contador = 0
    texto_contador = fuente.render(f"Puntos: {contador}", True, ROJO)
    rect_texto = texto_contador.get_rect(topleft = (30, 40))

    vidas_texto = fuente.render(f"Vidas: {vidas}", True, ROJO)
    rect_vidas_texto = vidas_texto.get_rect(topright  = (ANCHO - 30, 40))
    pygame.mixer.music.stop()
    pygame.mouse.set_visible(False)

    juego_musica = pygame.mixer.music.play(-1)
    colision = False
    cantidad_enemigos = 10
    running = True
    enemigos = []
    enemigos_y = []
    balas = []
    rafaga = True


    cargar_lista_enemigos(enemigos, cantidad_enemigos, enemigo_imagen)
    # cargar_lista_enemigos(enemigos_y, cantidad_enemigos, enemigo_imagen)



    while running:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == QUIT:
                running = False

            
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
                        print("activado")

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

            if e.type == MOUSEBUTTONDOWN:
                
                if e.button == 1:
                
                    if rafaga:
                        proyectil = crear_bala(bala_imagen, jugador["rect"], tamanio_bala, velocidad_bala)
                        balas.append(proyectil)
                        
                print(rafaga)


        #mover jugador
        # jugador_rotado, jugador_rect = mover_rotar_jugador(jugador,angulo, mover_izquierda, mover_derecha, mover_arriba, mover_abajo)




        # for enemigo in enemigos[:]:
        #     enemigo["rect"].move_ip(0, 2)
            
        #     if enemigo["rect"].top > HEIGHT:
        #         enemigo["rect"].y = -enemigo["rect"].height
        #         enemigo["rect"].x = random.randint(0, WIDTH - enemigo["rect"].width)

        for enemigo in enemigos[:]:
            enemigo["rect"].move_ip(velocidadx, 0)  # Mover hacia la derecha (puedes ajustar la velocidad según sea necesario)
            
            if enemigo["rect"].left > ANCHO:
                enemigo["rect"].x = -enemigo["rect"].width
                enemigo["rect"].y = random.randint(0, ALTO - enemigo["rect"].height)
        
                

        

 

        #muevo el proyectil
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
                
                
               
                
               

       

    
       
        if rafaga:
            for bala in balas[:]:
                colision = False
                for enemigo in enemigos[:]:
                    if detect_collision_circ(enemigo["rect"], bala["rect"]):
                        enemigos.remove(enemigo)
                        contador += 1
                        texto_contador = fuente.render(f"Puntos: {contador}", True, ROJO)
                        rect_texto = texto_contador.get_rect(topleft = (30, 40))
                        gran_contador = 10
                        colision = True
                        explosion_sonido.play()
                        if reproducir_musica:
                            explosion_sonido.play()

                            
                        if len(enemigos) == 0:
                            
                            cargar_lista_enemigos(enemigos, cantidad_enemigos, enemigo_imagen_2)
                            velocidad_x += 1
                            

                        
                
                if colision == True:
                    balas.remove(bala)
       
                
              



        
        
        x, y = pygame.mouse.get_pos()
       





        screen.blit(fondo, ORIGIN)
        pygame.draw.rect(screen, ROJO, jugador["rect"], 2)
        jugador_rotado, jugador_rect = mover_rotar_jugador(jugador, angulo, mover_izquierda, mover_derecha, mover_arriba, mover_abajo)
        screen.blit(jugador_rotado, jugador_rect)
        screen.blit(imagen_cursor, (x - cursor_rect.width / 2, y - cursor_rect.height/2 ))
        dibujar_enemigos(screen, enemigos)
        screen.blit(texto_contador, rect_texto)
        screen.blit(vidas_texto, rect_vidas_texto)
 
        if rafaga:
            for bala in balas:
                screen.blit(bala["img"], bala["rect"])
                

    
    
        pygame.display.flip()

    if contador > contador_maximo:
        contador_maximo = contador

    pygame.mixer.music.stop()
    fin_del_juego.play()

    pantalla_final(screen, menu_fondo, fuente)

    esperar_usuario()

