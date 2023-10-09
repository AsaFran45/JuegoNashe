import os
import sys, time
import pygame
from pygame import image


pygame.init()

# Definir colores
negro = (0, 0, 0)
blanco = (255, 255, 255)
azul = (0, 0, 255)
verde = (0, 255, 0)
rojo = (255, 0, 0)

size = (1360, 600)
screen = pygame.display.set_mode(size)

# Cargar la imagen de fondo
ruta_imagen = os.path.join(os.path.abspath(os.path.dirname(__file__)), "calle-ejemplo.jpg")
imagen_figura = pygame.image.load(ruta_imagen)
imagen_figura = pygame.transform.scale(imagen_figura, size)

# Cargar imágenes de los jugadores
jugador1_stand = pygame.image.load("E:\\Visual Studio WorkSpace\\Juego nashe\\6izq.png")
jugador1_stand = pygame.transform.scale(jugador1_stand, (120, 150))
jugador2_stand = pygame.image.load("E:\\Visual Studio WorkSpace\\Juego nashe\\6der2.png")
jugador2_stand = pygame.transform.scale(jugador2_stand, (120, 150))

# Variables de movimiento para el jugador 1
posicion_x1 = 30
posicion_y1 = 400
velocidad_x1 = 5
salto_velocidad1 = 10
salto_altura_maxima1 = 250
en_suelo1 = True
caminando = False

# Variables de movimiento para el jugador 2
posicion_x2 = 1100
posicion_y2 = 400
velocidad_x2 = 5
salto_velocidad2 = 10
salto_altura_maxima2 = 250
en_suelo2 = True
caminando2 = False

# Variables de control para las acciones del jugador 1
salto1 = False
golpe1 = False
golpe_tiempo_inicial1 = 0
golpe_duracion1 = 100  # Duración en milisegundos

# Variables de control para las acciones del jugador 2
salto2 = False
golpe2 = False
golpe_tiempo_inicial2 = 0
golpe_duracion2 = 100  # Duración en milisegundos

# Número máximo de golpes antes de perder
max_golpes = 11

# Contadores de golpes para cada jugador
golpes_jugador1 = 1
golpes_jugador2 = 1

velocidad_y1 = 0
velocidad_y2 = 0

####-------------- Funciones--------------------------####

def cargar_animacion(prefijo, sufijo, n):
    images = []
    for i in range(1, n+1):
        name = prefijo + str(i) + sufijo
        images.append(image.load(name))
        
    return images

def mostrar_animacion(images, freq,  x, y):
    frame = int(time.time()* freq) % len(images) 
    screen.blit(images[frame], (x, y))

def colision_entre_jugadores(pos1, pos2, ancho, alto):
    rect1 = pygame.Rect(pos1[0], pos1[1], ancho, alto)
    rect2 = pygame.Rect(pos2[0], pos2[1], ancho, alto)
    return rect1.colliderect(rect2)


####-------------- Funciones--------------------------####

# Interfaz de Usuario
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Acciones para el jugador 1
            if event.key == pygame.K_w and en_suelo1:
                salto1 = True
                caminando = False  
            if event.key == pygame.K_n:
                golpe1 = True
                golpe_tiempo_inicial1 = pygame.time.get_ticks()  # Capturar el tiempo actual
                golpes_jugador2 += 1

            # Acciones para el jugador 2
            if event.key == pygame.K_UP and en_suelo2:
                salto2 = True
                caminando2 = False  
            if event.key == pygame.K_RSHIFT:
                golpe2 = True
                golpe_tiempo_inicial2 = pygame.time.get_ticks()  # Capturar el tiempo actual
                golpes_jugador1 += 1

    ##### si los jugadores se encuentran cruzados####
    personaje1_del_lado_der = (posicion_x1 > posicion_x2)
    personaje1_del_lado_izq = (posicion_x1 < posicion_x2)
    personaje2_del_lado_der = (posicion_x2 > posicion_x1)
    personaje2_del_lado_izq = (posicion_x2 < posicion_x1)
    

    runner2 = cargar_animacion("caminar", "izq.png", 6)
    runner = cargar_animacion("caminar", "der.png", 6)
    
    personaje_sprite1 = jugador1_stand
    
    # Restablecer los estados de las acciones cuando no se estén realizando
    if not salto1 and not golpe1:
        if caminando:
            frame = int(time.time() * 5) % len(runner)  
            current_sprite = runner[frame]
        else:
            current_sprite = personaje_sprite1   
    if not salto2 and not golpe2:
        if caminando2:
            personaje_sprite2 = runner2  
        else:
            personaje_sprite2 = jugador2_stand  
    
    
    # Restablecer golpe después de que pase el tiempo de duración
    if golpe1 and pygame.time.get_ticks() - golpe_tiempo_inicial1 >= golpe_duracion1:
        golpe1 = False
        personaje_sprite1 = jugador1_stand
    if golpe2 and pygame.time.get_ticks() - golpe_tiempo_inicial2 >= golpe_duracion2:
        golpe2 = False
        personaje_sprite2 = jugador2_stand

    # Movimiento horizontal para el jugador 1
    keys = pygame.key.get_pressed()
    caminando = False
    if keys[pygame.K_a] and not colisionando1_izq:
        caminando = True
        posicion_x1 -= velocidad_x1
        if posicion_x1 < 0:
            posicion_x1 = 0

    if keys[pygame.K_d] and not colisionando1_der:
        posicion_x1 += velocidad_x1
        caminando = True
        if posicion_x1 > 1250:
            posicion_x1 = 1250

    # Movimiento horizontal para el jugador 2
    caminando2 = False
    if keys[pygame.K_LEFT] and not colisionando2_der:
        posicion_x2 -= velocidad_x2
        caminando2 = True
        if posicion_x2 < 0:
            posicion_x2 = 0
    if keys[pygame.K_RIGHT] and not colisionando2_izq:
        caminando2 = True
        posicion_x2 += velocidad_x2
        if posicion_x2 > 1250:
            posicion_x2 = 1250
    pos_1 = (posicion_x1, posicion_y1)
    pos_2 = (posicion_x2, posicion_y2)
    
    
    if colision_entre_jugadores((posicion_x1, posicion_y1), (posicion_x2, posicion_y2), 120, 150):
        separacion = 10  
        if posicion_x1 < posicion_x2:
            posicion_x1 -= separacion
            posicion_x2 += separacion
        else:
            posicion_x1 += separacion
            posicion_x2 -= separacion

    gravedad = 0.5

    # Salto para el jugador 1
    if salto1:
        if en_suelo1:  # Solo puede saltar si está en el suelo
            velocidad_y1 = salto_velocidad1
            salto1 = False
        else:
            if posicion_y1 < 400:  # Verifica si el jugador está en el aire
                velocidad_y1 += gravedad  # Agregamos la gravedad para simular la caída
            else:
                posicion_y1 = 400
                velocidad_y1 = 0

        # Salto para el jugador 2
    if salto2:
        if en_suelo2:  # Solo puede saltar si está en el suelo
            velocidad_y2 = salto_velocidad2
            salto2 = False
        else:
            if posicion_y2 < 400:  # Verifica si el jugador está en el aire
                velocidad_y2 += gravedad  # Agregamos la gravedad para simular la caída
            else:
                posicion_y2 = 400
                velocidad_y2 = 0

     # Movimiento vertical para los jugadores
    posicion_y1 -= velocidad_y1
    posicion_y2 -= velocidad_y2

     # Limitar la posición vertical de los jugadores para que no salgan de la pantalla
    posicion_y1 = max(posicion_y1, 0)
    posicion_y2 = max(posicion_y2, 0)
                
    
    

    # Detectar si los jugadores están en el suelo
    if posicion_y1 == 400:
        en_suelo1 = True
    else:
        en_suelo1 = False
    if posicion_y2 == 400:
        en_suelo2 = True
    else:
        en_suelo2 = False

    if posicion_y1 <= posicion_y2 or posicion_y2 <= posicion_y1:
        colisionando1_der = False
        colisionando1_izq = False
        colisionando2_der = False
        colisionando2_izq = False

    # Colisión de jugadores
    limite_sprite1_der = posicion_x1 + 120
    limite_sprite1_izq = posicion_x1 - 120
    limite_sprite2_izq = posicion_x2 - 120
    limite_sprite2_der = posicion_x2 + 120
    colisionando1_der = (posicion_x1 == limite_sprite2_izq)
    colisionando1_izq = (posicion_x1 == limite_sprite2_der)
    colisionando2_der = (posicion_x2 == limite_sprite1_der)
    colisionando2_izq = (posicion_x2 == limite_sprite1_izq)
    


    if posicion_y1 <= posicion_y2 or posicion_y2 <= posicion_y1:
        colisionando1_der = False
        colisionando1_izq = False
        colisionando2_der = False
        colisionando2_izq = False

    

    # Dibujar elementos en pantalla
    screen.blit(imagen_figura, (0, 0))
    if not caminando and not salto1:
        screen.blit(personaje_sprite1, (posicion_x1, posicion_y1))
    else:
        if keys[pygame.K_d] and not salto1:
            mostrar_animacion(runner, 5, posicion_x1, posicion_y1)
        else:
            mostrar_animacion(runner, 5, posicion_x1, posicion_y1)


    if not caminando2 and not salto2:
        screen.blit(jugador2_stand, (posicion_x2, posicion_y2))
    else:
        if keys[pygame.K_RIGHT] and not salto2:
            runner2 = cargar_animacion("caminar", "izq.png", 6)
            mostrar_animacion(runner2, 5, posicion_x2, posicion_y2)
        else:
            mostrar_animacion(runner2, 5, posicion_x2, posicion_y2)

    # Dirección personaje 1
    if posicion_x1 > posicion_x2:
        jugador1_stand = pygame.image.load("6izq2.png")
        jugador1_stand = pygame.transform.scale(jugador1_stand, (120, 150))
        if salto1:
            personaje_sprite1 = pygame.image.load("jumpizq2.png")
            personaje_sprite1 = pygame.transform.scale(personaje_sprite1, (120, 150))
        if golpe1:
            personaje_sprite1 = pygame.image.load("golpe.png")
            personaje_sprite1 = pygame.transform.scale(personaje_sprite1, (120, 150))
    else:
        # Dirección derecha
        jugador1_stand = pygame.image.load("6der2.png")
        jugador1_stand = pygame.transform.scale(jugador1_stand, (120, 150))
        if salto1:
            personaje_sprite1 = pygame.image.load("jumpder2.png")
            personaje_sprite1 = pygame.transform.scale(personaje_sprite1, (120, 150))
        if golpe1:
            personaje_sprite1 = pygame.image.load("golpe.png")
            personaje_sprite1 = pygame.transform.scale(personaje_sprite1, (120, 150))

    # Dirección personaje 2
    if posicion_x1 < posicion_x2:
        jugador2_stand = pygame.image.load("6izq2.png")
        jugador2_stand = pygame.transform.scale(jugador2_stand, (120, 150))
        if salto2:
            personaje_sprite2 = pygame.image.load("jumpizq2.png")
            personaje_sprite2 = pygame.transform.scale(personaje_sprite2, (120, 150))
        if golpe2:
            personaje_sprite2 = pygame.image.load("golpe2.png")
            personaje_sprite2 = pygame.transform.scale(personaje_sprite2, (120, 150))
    else:
        jugador2_stand = pygame.image.load("6der2.png")
        jugador2_stand = pygame.transform.scale(jugador2_stand, (120, 150))
        if salto2:
            personaje_sprite2 = pygame.image.load("jumpder2.png")
            personaje_sprite2 = pygame.transform.scale(personaje_sprite2, (120, 150))
        if golpe2:
            personaje_sprite2 = pygame.image.load("golpe.png")
            personaje_sprite2 = pygame.transform.scale(personaje_sprite2, (120, 150))

    pygame.display.flip()
