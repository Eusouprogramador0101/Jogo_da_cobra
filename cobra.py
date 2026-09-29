import pygame 
import json
from pygame.locals import *
from sys import exit 
from random import randint 
pygame.init()
from time import sleep
import os
import sys

def recurso(nome):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, nome)
    return os.path.join(os.path.abspath("."), nome)

def save(nome):
    if getattr(sys, "frozen", False):
        pasta = os.path.dirname(sys.executable)
    else:
        pasta = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pasta, nome)

try:
    with open(save("save_pontuacao_max.json"), "r") as arquivo:
        save_data = json.load(arquivo)
except FileNotFoundError:
    save_data = {"max": 0}
    with open(save("save_pontuacao_max.json"), "w") as arquivo:
	    json.dump(save_data, arquivo, indent=4)

musica_de_fundo = pygame.mixer.music.load(recurso("smw_course_clear.wav"))
pygame.mixer.music.play (-1)

som_de_colisao = pygame.mixer.Sound(recurso("smw_1-up.wav"))
	
tela = pygame.display.set_mode ((640,480))
pygame.display.set_caption ("Game")
tempo = pygame.time.Clock ()
fonte = pygame.font.SysFont ("gabriola",20,True,False)
fonte2 = pygame.font.SysFont ("gabriola",40,True,False)

msg_pontos = "10 Pontos"
venceu = "Você Venceu!"
text_perdeu = "Você perdeu!"
text_venceu = fonte2.render (venceu,True,(0,255,0))
text_inicial = fonte2.render ('pressione w para iniciar',True,(255,255,255))
text_ganhou_pontos = fonte.render (msg_pontos,True,(255,255,255))
perdeu = fonte2.render (text_perdeu,True,(255,0,0))
text_venceu = fonte2.render (venceu,True,(0,255,0))
altura = 480
largura = 640
x = largura/2 - (20 / 2)
y = altura / 2 - (20 / 2)
z = randint (50,570)
w = randint (50,410)
over = (100*10)
p = 0
t = 0
tamanho_cobra = 8
lista_cobra = [ ]
morreu = False
comecou = False

def aumenta_cobra (lista_cobra) :
	for XeY in lista_cobra:
		cobra1 = pygame.draw.rect (tela,(0,200,0),(XeY[0],XeY[1],20,20))	
		 
def resetar_jogo ():
	global p,x,y,tamanho_cobra,t,z,w,morreu,lista_cobra,lista_cabeca,comecou
	p = 0
	x = largura/2 - (20 / 2)
	y = altura / 2 - (20 / 2)
	tamanho_cobra = 8
	t = 0
	pygame.mixer.music.play (-1)
	lista_cobra = [ ]
	lista_cabeca = [ ]
	z = randint (50,570)
	w = randint (50,410)
	morreu = False
	comecou = False
	

while True:
	tempo.tick (60)
	tela.fill ((0,0,0))
	points = f"Pontos: {p}"
	text_pontos = fonte2.render (points,True,(255,255,255))
	for event in pygame.event.get():
		if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit ()
					exit ()
		if event.type == KEYDOWN:
			if event.key == K_w or event.key == K_UP:
				comecou = True
				if t != 2:
					t = 1
			if event.key == K_s or event.key == K_DOWN:
				if t != 1:
					t = 2
			if event.key == K_d or event.key == K_RIGHT:
				if t != 4:
					t = 3
			if event.key == K_a or event.key == K_LEFT:
				if t != 3:
					t = 4
	fundo = pygame.draw.line (tela,(100,80,40),(320,30),(320,440),(600))
	esquerda = pygame.draw.rect (tela,(0,0,255),(0,0,50,480)) 
	direita = pygame.draw.rect (tela,(0,0,255),(590,0,50,480)) 
	cima =  pygame.draw.rect (tela,(0,0,255),(0,0,640,50)) 
	baixo = pygame.draw.rect (tela,(0,0,255),(0,430,640,50))  
	cobra = pygame.draw.rect (tela,(0,200,0),(x,y,20,20))	
	maca = pygame.draw.rect (tela,(200,0,0),(z,w,20,20))
	if not comecou:
		tela.blit(text_inicial,(130,200))
	else:
		if t == 1 :
			y -= 3
		elif t == 2 :
			y += 3
		elif t == 3 :
			x += 3
		elif t == 4 :
			x -= 3
	if cobra.colliderect(maca):
		som_de_colisao.play ()
		z = randint (50,570)
		w = randint (50,410)
		p += 10
		tamanho_cobra += 3
		tela.blit(text_ganhou_pontos,(x,y))

	if cobra.colliderect(esquerda):
		morreu = True 
	elif cobra.colliderect(direita):
		morreu = True
	elif cobra.colliderect(cima):
		morreu = True 
	elif cobra.colliderect(baixo):
		morreu = True

	lista_cabeca = [ ]
	lista_cabeca.append (x)
	lista_cabeca.append (y)
	lista_cobra.append (lista_cabeca)
	if len (lista_cobra) > tamanho_cobra:
		del lista_cobra [0]
	aumenta_cobra (lista_cobra)
	tela.blit (text_pontos,(10, 10))
	if lista_cobra.count(lista_cabeca) > 1 and t != 0 and comecou :
		morreu = True

	while morreu :
		if p > save_data['max']:
			save_data['max'] = p
			with open(save("save_pontuacao_max.json"), "w") as arquivo:
				json.dump(save_data, arquivo, indent=4)
		pont_max = fonte.render (f"Pontuação Máxima: {save_data['max']}",True,(255,255,255))
		pygame.draw.circle (tela,(0,0,0),(600,300),(2000))
		tela.blit (pont_max,(210,240))
		pygame.draw.circle(tela,(255,255,255),(700,1980),(80))
		tela.blit (perdeu,(200,200))
		pygame.mixer.music.stop ()
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit ()
					exit ()
				if event.key == K_SPACE:
					resetar_jogo()
		pygame.display.update ()
	if p >= over:
		pygame.draw.circle (tela,(0,0,0),(320,240),(4,0,0),(940,1980),(80))
		tela.blit (text_venceu,(300, 240))
		pygame.display.update()
		sleep (1)
		pygame.quit()
		exit ()
	pygame.display.update()