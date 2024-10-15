from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list


class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action


class Menu:
	def load_button_images(self):
		# Carregar as imagens dos botões
		self.resume_img = pygame.image.load('../graphics/grass/grass_1.png').convert_alpha()
		self.options_img = pygame.image.load('../graphics/grass/grass_1.png').convert_alpha()
		self.quit_img = pygame.image.load('../graphics/grass/grass_1.png').convert_alpha()
		self.video_img = pygame.image.load('../graphics/grass/grass_1.png').convert_alpha()
		self.audio_img = pygame.image.load('../graphics/grass/grass_1.png').convert_alpha()
		self.keys_img = pygame.image.load('../graphics/grass/grass_1.png').convert_alpha()
		self.back_img = pygame.image.load('../graphics/grass/grass_1.png').convert_alpha()

		# Definindo as posições dos botões
		self.resume_button = Button(304, 125, self.resume_img, 1)
		self.options_button = Button(297, 250, self.options_img, 1)
		self.quit_button = Button(336, 375, self.quit_img, 1)
		self.video_button = Button(226, 75, self.video_img, 1)
		self.audio_button = Button(225, 200, self.audio_img, 1)
		self.keys_button = Button(246, 325, self.keys_img, 1)
		self.back_button = Button(332, 450, self.back_img, 1)


