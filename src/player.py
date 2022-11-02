import pygame


class Player(pygame.sprite.Sprite): # cette classe hérite de ...
    def __init__(self,x,y): # cette classe contient les méthodes et les fonctions de ...
        super().__init__() # Initialise le Sprite
        self.sprite_sheet = pygame.image.load("..\\sprites\\Galaad_spritsheet.png")
        self.image = self.get_image(2,104) # 2 + 32*k , 14 + 45*k
        self.image.set_colorkey([0,0,0]) # enleve la couleur du fond
        self.rect = self.image.get_rect() # prends un rectangle
        self.position = [x,y] # prends position perso
        self.speed = 3 # vitesse

        # changer d'image lorsque l'on change de sens
        self.images = { 
            'down': self.get_image(2,104),
            'left': self.get_image(2,14+45*3),
            'right': self.get_image(2,14+45),
            'up': self.get_image(2,14)
        }

        # la collision se passe au niveau des pieds (du rectangle donc la moitié) du sprit
        self.feet = pygame.Rect(0,0, self.rect.width*0.5, 12)
        self.old_position = self.position.copy()

        # permet de sauvegarder l'anciennce position du joueur
    def save_location(self): self.old_position = self.position.copy()

 # changer d'image lorsque l'on change de sens
    def change_animation(self,name):
        self.image = self.images[name]
        self.image.set_colorkey((0,0,0))
    # Déplacements du perso

    def move_right(self): self.position[0] += self.speed

    def move_left(self): self.position[0] -= self.speed

    def move_up(self): self.position[1] -= self.speed

    def move_down(self): self.position[1] += self.speed



    def update(self): # met à jour position du joueur
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self): # permet de se remettre à la position avant si collision
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom        


    def get_image(self,x,y): # prends les coordonnées du sprite
        image = pygame.Surface([32,32]) # taille de l'image (largeur et hauteur)
        image.blit(self.sprite_sheet, (0,0), (x,y,32,32))
        return image # retourne l'image découpée