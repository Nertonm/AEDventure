import pygame 
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
		super().__init__(groups)
		self.sprite_type = sprite_type
		self.image = surface
		if sprite_type == 'object':
			self.rect = self.image.get_rect(topleft = (pos[0],pos[1]))
		if sprite_type == 'invisible':
			self.rect = self.image.get_rect(topleft = pos)
		if sprite_type == 'npc':
			self.image = pygame.transform.scale(self.image,(TILESIZE*2,TILESIZE*2))
			self.rect = self.image.get_rect(topleft = pos)
		else:
			self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,0)
