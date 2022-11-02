import pygame
import pytmx
import pyscroll
import player

class Game: # fonction chargée au lancement du jeu (comme ROM)
    def __init__(self):
        # creer la fenetre du jeu #

        # dimension fenêtre
        self.screen=pygame.display.set_mode((800,600))

        # titre
        pygame.display.set_caption("Ambhalla")

        # charge la carte
        tmx_data = pytmx.util_pygame.load_pygame("..\\map\\carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map = "world"

        # regrouper tous les calques créés sur Tiled
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        # On zoom
        map_layer.zoom = 2

        # generer le joueur
        player_position = tmx_data.get_object_by_name("Player") # recupere le point "player"
        self.player = player.Player(player_position.x,player_position.y) # + position perso

        # definir une liste qui va stcoker les classes collisions
        self.walls = []
        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # definir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)


    def handle_input(self): # fonction qui s'occupe des touches du claviers
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation("up")

        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation("down")

        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation("left")

        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation("right")

    def switch_house(self):
        tmx_data = pytmx.util_pygame.load_pygame("..\\map\\house.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)

        # regrouper tous les calques créés sur Tiled
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        # On zoom
        map_layer.zoom = 2

        # pas besoin de regenerer le joueur

        # definir une liste qui va stcoker les classes collisions
        self.walls = []
        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # definir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name("exit_house") # le nouvelle entrée est donc la sortie
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)        

        spawn_house_point = tmx_data.get_object_by_name("spawn_house")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 40

    def switch_world(self):
        tmx_data = pytmx.util_pygame.load_pygame("..\\map\\carte.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)

            # regrouper tous les calques créés sur Tiled
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        # On zoom
        map_layer.zoom = 2

            # pas besoin de regenerer le joueur

            # definir une liste qui va stcoker les classes collisions
        self.walls = []
        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

            # definir le rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name("enter_house") # le nouvelle entrée est donc la sortie
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)        

        spawn_house_point = tmx_data.get_object_by_name("enter_house_exit")
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 20

    def update(self): # met à jour position mais aussi si collision
        self.group.update()


        # verif entrer dans la maison
        if self.map == "world" and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = "house"

        # verif l'entrer dans "le monde"
        if self.map == "house" and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()
            self.map = "world"


        # verif collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()


    def run(self): # lance le jeu
        # boucle du jeu
        clock = pygame.time.Clock() # fps
        running=True
        while running:

            self.player.save_location()
            self.handle_input() # prends en charge les boutons pressés
            # On importe le groupe de calques pour les dessiner
            self.update()
            self.group.center(self.player.rect) # centre la vision sur le joueur
            self.group.draw(self.screen)

            # On actualise
            pygame.display.flip()

            for event in pygame.event.get(): # pour touts les evenements dans la fenetre pygame
                if event.type == pygame.QUIT: # si c'est la croix
                    running=False # alors arrêter

            clock.tick(60) # 60 fps

        pygame.quit()