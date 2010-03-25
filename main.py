# -*- coding: utf-8 -*-

import vermell
import pygame, math

pygame.init()
window = pygame.display.set_mode( (640,480), pygame.DOUBLEBUF )
screen = pygame.display.get_surface()
vermell.initCapture()
while 1:
	screen.fill((0,0,0))
	d = vermell.getData()
	if d:
		for e in d:
			angle = e['angle']
			size = 10
			print e['size'].width
			print e['size'].height
			p = (e['center'].x,e['center'].y)
			v = (size*math.cos(angle), size*math.sin(angle))
			p2 = (p[0]+v[0],p[1]+v[1])
			pygame.draw.line(screen,(255,255,255),p,p2)
	
	pygame.display.flip()