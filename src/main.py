try:
    import pygame
    from pygame.locals import *
    from configuracion import *
    from modulos import *
    from colisiones import *
    
except:
    print("error falta de modulo")




# def crear_bala(imagen, jugador_rect, tamanio_bala, velocidad_bala):
#     # Obtener el punto de inicio de la bala en función del ángulo del jugador
#     start_x = jugador_rect.centerx
#     start_y = jugador_rect.centery

#     # Calcular las componentes x e y de la velocidad basadas en el ángulo
#     velocidad_x = velocidad_bala * math.sin(math.radians(jugador["angulo"]))
#     velocidad_y = velocidad_bala * math.cos(math.radians(jugador["angulo"]))

#     # Crear el rectángulo de la bala en la posición calculada
#     bala_rect = pygame.Rect(start_x - tamanio_bala[0] // 2, start_y - tamanio_bala[1], tamanio_bala[0], tamanio_bala[1])

#     # Crear el diccionario de la bala
#     bala = {
#         "img": imagen,
#         "rect": bala_rect,
#         "speed_x": velocidad_x,
#         "speed_y": velocidad_y
#     }

#     return bala


pygame.init()

#reloj
clock = pygame.time.Clock()


#pantalla principal
screen = pygame.display.set_mode(SIZE_SCREEN)
pygame.display.set_caption("Tanks")


#set imagenes
jugador_imagen = pygame.transform.scale(pygame.image.load("./src/assets/tank.png"), (BLOCK_WIDTH, BLOCK_HEIGHT))
enemigo_imagen= pygame.transform.scale(pygame.image.load("./src/assets/enemy.png"), (BLOCK_WIDTH, BLOCK_HEIGHT))
fondo = pygame.transform.scale(pygame.image.load("./src/assets/ground.jpg"), SIZE_SCREEN) 
imagen_cursor = pygame.transform.scale(pygame.image.load("./src/assets/mira.png"),(30,30))
bala_imagen = pygame.transform.scale(pygame.image.load("./src/assets/bala.png"),tamanio_bala)


cursor_rect = imagen_cursor.get_rect()

#sonidos

explosion_sonido = pygame.mixer.Sound("./src/assets/explosion.wav")
explosion_sonido.set_volume(0.1)


pygame.mouse.set_visible(False)


#crear bloque

jugador = crear_modelo(jugador_imagen, WIDTH // 2, HEIGHT // 2, BLOCK_WIDTH, BLOCK_HEIGHT, RED, angulo=0)






while True:


    colision = False
    cantidad_enemigos = 5
    running = True
    enemigos = []
    balas = []
    rafaga = True

    cargar_lista_enemigos(enemigos, cantidad_enemigos, enemigo_imagen)


    while running:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == QUIT:
                running = False

            
            if e.type == KEYDOWN:
                if e.key == K_w:
                    move_up = True
                    move_down = False

                if e.key == K_s:
                    move_down = True
                    move_up = False

                if e.key == K_d:
                    move_right = True
                    move_left = False

                if e.key == K_a:
                    move_left = True
                    move_right = False


            if e.type == KEYUP:
                if e.key == K_w:
                    move_up = False

                if e.key == K_s:
                    move_down = False

                if e.key == K_d:
                    move_right = False

                if e.key == K_a:
                    move_left = False

            if e.type == MOUSEBUTTONDOWN:
                
                if e.button == 1:
                
                    if rafaga:
                        balas.append(crear_bala(bala_imagen,jugador["rect"], tamanio_bala, velocidad_bala))
                        
                print(rafaga)


        #mover jugador
        jugador_rotado, jugador_rect = mover_rotar_jugador(jugador, move_left, move_right, move_up, move_down)




        #enemigos movimientos 
        for enemigo in enemigos[:]:
            enemigo["rect"].move_ip(0, 2)
            if enemigo["rect"].top > HEIGHT:
                enemigo["rect"].y = -enemigo["rect"].height



        #muevo el proyectil
        if rafaga:
            for bala in balas[:]:
                if bala["rect"].bottom >= 0:
                    velocidad_x = bala["speed_x"] * math.sin(math.radians(jugador["angulo"]))
                    velocidad_y = bala["speed_y"] * math.cos(math.radians(jugador["angulo"]))

            
                    bala["rect"].move_ip(velocidad_x, velocidad_y)
                else:
                    balas.remove(bala)
                

        
      

       

    
       
        if rafaga:
                
                for bala in balas[:]:
                    colision = False
                    for enemigo in enemigos[:]:
                        if detect_collision_circ(enemigo["rect"], bala["rect"]):
                            enemigos.remove(enemigo)
                            

                            colision = True
                            explosion_sonido.play()

                            
                        if len(balas) == 0:
                            cargar_lista_enemigos(enemigos, cantidad_enemigos, enemigo_imagen)
                
                    if colision == True:
                        balas.remove(bala)
       
                
              



        
        
        x, y = pygame.mouse.get_pos()
       





        screen.blit(fondo, ORIGIN)

        screen.blit(jugador_rotado, jugador_rect)
        screen.blit(imagen_cursor, (x - cursor_rect.width / 2, y - cursor_rect.height/2 ))
        dibujar_enemigos(screen, enemigos)
 
        if rafaga:
            for bala in balas:
                screen.blit(bala["img"], bala["rect"])

    
    
        pygame.display.flip()
        

    terminar()


