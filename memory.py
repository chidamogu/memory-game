# Simple Memory Game - Chidinma Amogu

import pygame, random


# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Memory')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
      self.board_size = 4
      self.image_list = []
      self.images = self.load_images()
      
      self.board = [] # will be represented by a list of lists
      self.create_board()
      self.score = 0
      self.records = []
      self.matches = 0
      #self.previous_tile = None
      
   def load_images(self):
      # loads all the images needed for the game, appends them to self.image_list
      images = ('image1.bmp', 'image2.bmp', 'image3.bmp', 'image4.bmp', 'image5.bmp', 'image6.bmp', 'image7.bmp', 'image8.bmp')
      for i in images:
         image = pygame.image.load(i)
         # appending twice because each image needs to be used twice
         self.image_list.append(image)
         self.image_list.append(image)

      
   def create_board(self):
      # creates the board object by using a nested for loop to build a list of lists
      # and calling on the instance attributes of the tile class to make up each component of the board
      for row_index in range(self.board_size):
         row = []
         for col_index in range(self.board_size):
            image = random.choice(self.image_list)
            self.image_list.remove(image)
            image_width = image.get_width()
            image_height = image.get_height()
            x = col_index * image_width
            y = row_index * image_height
            tile = Tile(x,y,image_width,image_height, image, self.surface)
            row.append(tile)
         self.board.append(row)
         
         
   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS)  # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.MOUSEBUTTONUP and self.continue_game:   
            self.handle_mouse_button_up(event.pos)
   
   def handle_mouse_button_up(self, position):
      # evaluates the mouse bottun up event, and finds the exact tile that was clicked
      # position is an (x,y) tuple that represents the position where the mousebuttonup event happened
      for row in self.board:
         for tile in row:
            exposed = tile.get_exposed(position) # get_exposed method is in the tile class
            if exposed:
               self.records.append(tile)
               
               
   def compare_records(self):
      # compares all the tiles that've been clicked and flipped over by the player to see if they're a match
      #    - if the tiles are a match, the self.matches int value is incremented by one
      #    - if the tiles are not a match, there is a pause, and each tile is set back to hidden
      if len(self.records) == 2:
         if self.records[0].__eq__(self.records[1]):  # calls on the __eq__ method in the tile class, returns a bool
            self.matches = self.matches + 1
         else: 
            pygame.time.wait(400)
            self.records[0].set_hidden(True)  # sends a bool value to the set_hidden method in the tile class
            self.records[1].set_hidden(True)
         self.records.clear()  # clears the list of selected tiles 
         
               
   def draw_score(self):
      # steps for drawing the score
      # Step 1 - create a font object
      score_string = (str(self.score))
      font_size = 80
      font = pygame.font.SysFont('', font_size)
      # Step 2 - Render the font to create the textbox
      foreground_color = pygame.Color('white')
      background_color = self.bg_color  # instance attribute of the game
      text_box = font.render(score_string, True, foreground_color, background_color)
      location = (self.surface.get_width() - text_box.get_width(),0)
      self.surface.blit(text_box, location)   
      

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.draw_score()
      # draw the board
      for row in self.board:
         for tile in row:
            tile.draw()
      pygame.display.update() # make the updated surface appear on the display

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      
      self.compare_records()
      self.score = pygame.time.get_ticks()//1000
      

   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      
      if self.matches == 8:
         self.continue_game = False

class Tile:
   # An object in this class represents a singular tile

   def __init__(self, x, y, width, height, image, surface):
      # Initializes a tile
      # - self is the Tile to initialize
      # - x and y are int objects that represent the (x,y) coordinate location of the tile 
      # - width and height are int objects that represent the (width, height) dimensions of the tile 
      # - image is the random image selected in the game class, of type pygame.Surface
      # - surface is the display window surface object      
      self.rect = pygame.Rect(x,y,width,height)
      self.color = pygame.Color('black')
      self.border_width= 3
      self.hidden_image = pygame.image.load('image0.bmp')
      self.exposed_image = image
      self.content = self.hidden_image
      self.hidden = True
      self.surface = surface
      
   def draw(self):
      # draws the tile object
      # - self: the tile object      
      self.surface.blit(self.content, self.rect)
      pygame.draw.rect(self.surface,self.color,self.rect, self.border_width)
      
      
   def get_exposed(self, position):
      # - self: the tile object      
      # - position: a tuple representing the (x,y) of the location of the click      
      # - returns exposed: a bool value that represents whether or not the tile object has been clicked
      exposed = False
      if self.rect.collidepoint(position) and self.content == self.hidden_image:  # is there a click? and is the tile clicked currently unexposed?
         exposed = True
         self.set_exposed_image()
         
      return exposed   
         
   def set_exposed_image(self):
      # flips the tile image from hidden to exposed
      # - self: the tile object      
      if self.content == self.hidden_image: 
         self.content = self.exposed_image
      
         
   def draw_content(self):
      # drawing out the tile object
      # - self: the tile object
      font = pygame.font.SysFont('',133) # height of the surface is 400 //3 = 133
      text_box = font.render(self.content,True,self.color)
      # text_box is a pygame.Surface object - get the rectangle from the surface
      rect1 = text_box.get_rect()
      #rect1  <---->  self.rect
      rect1.center = self.rect.center
      location = (rect1.x,rect1.y)
      self.surface.blit(text_box,location)
   
   
   def set_hidden(self, new_hidden):
      # sets the value of self.hidden to whatever new bool value is passed in 
      # - self is the tile object
      # - new_hidden: a bool value passed in from the Game class
      self.hidden = new_hidden
      if self.hidden == True:
         self.content = self.hidden_image
        
   
   def __eq__(self, other_tile):
      # compares the tile to the other_tile tile object passed in
      # - self: the tile object
      # - other_tile: represents another tile object
      # - Returns: a bool object
      return self.exposed_image == other_tile.exposed_image

main()