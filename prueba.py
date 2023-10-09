import os
from pygame import *
import sys, time
import pygame
init()

def cargar_animacion(prefijo, sufijo, n):
    images = []
    for i in range(1, n+1):
        name = prefijo + str(i) + sufijo
        images.append(image.load(name))
        
    return images

def mostrar_animacion(images, freq,  x, y):
    frame = int(time.time()* freq) % len(images) 
    screen.blit(images[frame], (x, y))




# Definir colores
negro = (0, 0, 0)
blanco = (255, 255, 255)
azul = (0, 0, 255)
verde = (0, 255, 0)
rojo = (255, 0, 0)

size = (1360, 600)

screen = pygame.display.set_mode(size)

# Obtener la ruta completa de la imagen
ruta_imagen = os.path.join(os.path.abspath(os.path.dirname(__file__)), "calle-ejemplo.jpg")

# Cargar la imagen y redimensionarla para que coincida con el tamaño de la ventana
imagen_figura = pygame.image.load(ruta_imagen)
imagen_figura = pygame.transform.scale(imagen_figura, size)

# Cargar imagen del personaje y ajustar tamaño
jugador1_stand = pygame.image.load("6izq.png")
jugador1_stand = pygame.transform.scale(jugador1_stand, (120, 150))
jugador2_stand = pygame.image.load("6der2.png")
jugador2_stand = pygame.transform.scale(jugador2_stand, (120, 150))

# Variables para el movimiento del jugador 1
posicion_x1 = 30
posicion_y1 = 400
velocidad_x1 = 10
salto_velocidad1 = 10
salto_altura_maxima1 = 250
en_suelo1 = True
caminando = False

# Variables para el movimiento del jugador 2
posicion_x2 = 1100
posicion_y2 = 400
velocidad_x2 = 10
salto_velocidad2 = 10
salto_altura_maxima2 = 250
en_suelo2 = True
caminando2 = False


# Variables de control para las acciones del jugador 1
salto1 = False
golpe1 = False
golpe_tiempo_inicial1 = 0
golpe_duracion1 = 200  # Duración en milisegundos
tiempo = pygame.time.get_ticks
tomar_ms = 200



def SpriteSalto(personaje, sprite_path):
    personaje = pygame.image.load(sprite_path)


# Variables de control para las acciones del jugador 2
salto2 = False
golpe2 = False
golpe_tiempo_inicial2 = 0
golpe_duracion2 = 200  # Duración en milisegundos

#############------------------barras de vida---------------------########################

barras = [pygame.image.load("vida12.png"),
          pygame.image.load("vida11.png"),
          pygame.image.load("vida10.png"),
          pygame.image.load("vida9.png"),
          pygame.image.load("vida8.png"),
          pygame.image.load("vida7.png"),
          pygame.image.load("vida6.png"),
          pygame.image.load("vida5.png"),
          pygame.image.load("vida4.png"),
          pygame.image.load("vida3.png"),
          pygame.image.load("vida2.png"),
          pygame.image.load("vida1.png"),
          pygame.image.load("vida0.png")]

barra_de_vida1 = [barras]
contador = 0



# Número máximo de golpes antes de perder
max_golpes = 11

# Contadores de golpes para cada jugador
golpes_jugador1 = 1
golpes_jugador2 = 1

def manejar_colisiones():
    global posicion_x1, posicion_x2

    # Obtener los rectángulos de colisión de los personajes
    rect_jugador1 = pygame.Rect(posicion_x1, posicion_y1, 120, 150)
    rect_jugador2 = pygame.Rect(posicion_x2, posicion_y2, 120, 150)

    # Verificar si los rectángulos de colisión se superponen
    if rect_jugador1.colliderect(rect_jugador2):
        # Colisión detectada, ajustar las posiciones de los personajes
        distancia = 30
        # Ajustar posición del jugador 1
        if posicion_x1 < posicion_x2:
            posicion_x1 -= distancia // 2
        else:
            posicion_x1 += distancia // 2

        # Ajustar posición del jugador 2
        if posicion_x2 < posicion_x1:
            posicion_x2 -= distancia // 2
        else:
            posicion_x2 += distancia // 2

        # Actualizar la pantalla para reflejar los cambios
        pygame.display.flip()

#Interfaz de Usuario
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Acciones para el jugador 1
            if event.key == pygame.K_w and en_suelo1:
                salto1 = True
            if event.key == pygame.K_n:
                golpe1 = True
                golpe_tiempo_inicial1 = pygame.time.get_ticks()  # Capturar el tiempo actual
                
                golpes_jugador2 += 1

            # Acciones para el jugador 2
            if event.key == pygame.K_UP and en_suelo2:
                salto2 = True
            if event.key == pygame.K_RSHIFT:
                golpe2 = True
                golpe_tiempo_inicial2 = pygame.time.get_ticks()  # Capturar el tiempo actual
                golpes_jugador1 += 1


    # Restablecer los estados de las acciones cuando no se estén realizando
    if not salto1 and not golpe1 and not caminando:
        personaje_sprite1 = jugador1_stand
    if not salto2 and not golpe2:
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
        if not salto1:
            salto_velocidad1 = 10

            
    if keys[pygame.K_d] and not colisionando1_der:
        posicion_x1 += velocidad_x1
        caminando = True
        if posicion_x1 > 1250:
            posicion_x1 = 1250
        if not salto1:
            salto_velocidad2 = 10

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
    # Salto para el jugador 1
    if salto1:

        if posicion_y1 > (400 - salto_altura_maxima1):
            posicion_y1 -= salto_velocidad1
        else:
            salto1 = False
    elif posicion_y1 < 400:
        posicion_y1 += salto_velocidad1

    # Salto para el jugador 2
    if salto2:
        if posicion_y2 > (400 - salto_altura_maxima2):
            posicion_y2 -= salto_velocidad2
        else:
            salto2 = False
    elif posicion_y2 < 400:
        posicion_y2 += salto_velocidad2

    # Detectar si los jugadores están en el suelo
    if posicion_y1 == 400:
        en_suelo1 = True
    else:
        en_suelo1 = False
    if posicion_y2 == 400:
        en_suelo2 = True
    else:
        en_suelo2 = False


    # Durante el bucle del juego, verifica si las zonas de golpe se superponen

    manejar_colisiones()
    runner = cargar_animacion("caminar", "der.png", 6)
    runner2 = cargar_animacion("caminar", "der.png", 6)
    

    if posicion_y1 <= posicion_y2 or posicion_y2 <= posicion_y1:
        colisionando1_der = False
        colisionando1_izq = False
        colisionando2_der = False
        colisionando2_izq = False
    

    # Colision de jugadores
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
   
    
    if not caminando2 and not salto2:
        screen.blit(personaje_sprite2, (posicion_x2, posicion_y2))
    else: 
        if posicion_x1 < posicion_x2:
            if keys[pygame.K_LEFT] and not salto2:
                runner2 = cargar_animacion("caminar", "izq.png", 6)
                mostrar_animacion(runner2, 5, posicion_x2, posicion_y2)
            if keys[pygame.K_RIGHT] and not salto2:
                runner2 = cargar_animacion("caminar", "der.png", 6)
                mostrar_animacion(runner2, 5, posicion_x2, posicion_y2)
        else: 
            if keys[pygame.K_LEFT] and not salto2:
                runner2 = cargar_animacion("caminar", "izq.png", 6)
                mostrar_animacion(runner2, 5, posicion_x2, posicion_y2)
            if keys[pygame.K_RIGHT] and not salto2:
                runner2 = cargar_animacion("caminar", "der.png", 6)
                mostrar_animacion(runner2, 5, posicion_x2, posicion_y2)



    if not caminando and not salto1:
        screen.blit(personaje_sprite1, (posicion_x1, posicion_y1))
    else: 
        if posicion_x2 > posicion_x1:
            if keys[pygame.K_a] and not salto1:
                runner = cargar_animacion("caminar", "izq.png", 6)
                mostrar_animacion(runner, 5, posicion_x1, posicion_y1)
            if keys[pygame.K_d] and not salto1:
                runner = cargar_animacion("caminar", "der.png", 6)
                mostrar_animacion(runner, 5, posicion_x1, posicion_y1)
        else:
            if posicion_x2 < posicion_x1: 
                if keys[pygame.K_d] and not salto1:
                    runner = cargar_animacion("caminar", "izq.png", 6)
                    mostrar_animacion(runner, 5, posicion_x1, posicion_y1)
                if keys[pygame.K_a] and not salto1:
                    runner = cargar_animacion("caminar", "der.png", 6)
                    mostrar_animacion(runner, 5, posicion_x1, posicion_y1)
            
        
    #direccion personaje 1

    #direccion de vista
    if posicion_x1 > posicion_x2:
        jugador1_stand = pygame.image.load("6izq2.png")
        jugador1_stand = pygame.transform.scale(jugador1_stand, (120, 150))
        if salto1 is True:
            SpriteSalto(personaje_sprite1, "jumpizq2.png")

        #Direccion de salto
        if salto1 is True:
            personaje_sprite1 = pygame.image.load("jumpizq2.png")
            personaje_sprite1 = pygame.transform.scale(personaje_sprite1, (120, 150))
        #Direccion de golpe
        if golpe1 is True:
            personaje_sprite1 = pygame.image.load("golpe2.png")
            personaje_sprite1 = pygame.transform.scale(personaje_sprite1, (160, 150))
    else:
        ##direccion derecha
        jugador1_stand = pygame.image.load("6der2.png")
        jugador1_stand = pygame.transform.scale(jugador1_stand, (120, 150))
        #direccion salto derecha
        if salto1 is True:
            personaje_sprite1 = pygame.image.load("jumpder2.png")
            personaje_sprite1 = pygame.transform.scale(personaje_sprite1, (120, 150))
        #direccion golpe derecha
        if golpe1 is True:
            personaje_sprite1 = pygame.image.load("golpe.png")
            personaje_sprite1 = pygame.transform.scale(personaje_sprite1, (160, 150))
    
    #direccion personaje 2
    if posicion_x1 < posicion_x2:
        jugador2_stand = pygame.image.load("6izq2.png")
        jugador2_stand = pygame.transform.scale(jugador2_stand, (120, 150))
        if salto2 is True:
            personaje_sprite2 = pygame.image.load("jumpizq2.png")
            personaje_sprite2 = pygame.transform.scale(personaje_sprite2, (120, 150))
        if golpe2 is True:
            personaje_sprite2 = pygame.image.load("golpe2.png")
            personaje_sprite2 = pygame.transform.scale(personaje_sprite2, (160, 150))
    else:
        jugador2_stand = pygame.image.load("6der2.png")
        jugador2_stand = pygame.transform.scale(jugador2_stand, (120, 150))
        if salto2 is True:
            personaje_sprite2 = pygame.image.load("jumpder2.png")
            personaje_sprite2 = pygame.transform.scale(personaje_sprite2, (120, 150))
        if golpe2 is True:
            personaje_sprite2 = pygame.image.load("golpe.png")
            personaje_sprite2 = pygame.transform.scale(personaje_sprite2, (160, 150))

    pygame.display.flip()
    
    #animacion caminar

    # Actualizar pantalla
    