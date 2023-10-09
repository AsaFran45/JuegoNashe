from pygame import *
import sys, time

init()
screen = display.set_mode((800, 600))
def cargar_animacion(prefijo, sufijo, n):
    images = []
    for i in range(1, n+1):
        name = prefijo + str(i) + sufijo
        images.append(image.load(name))
    return images

def mostrar_animacion(images, freq,  x, y):
    frame = int(time.time()* freq) % len(images) 
    screen.blit(images[frame], (x, y))
    
runner = cargar_animacion("caminar", "izq.png", 6 )
while True:
    screen.fill((255, 255, 255))
    for e in event.get():
        if e.type == QUIT : sys.exit()
    mostrar_animacion(runner, 5,  100, 100)
   

    display.flip()
