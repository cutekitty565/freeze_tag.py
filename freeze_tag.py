import pygame
import math

def move_diagonally(red_position, red_vector):
  if red_position[1] >= SCREEN_HEIGHT:
    red_vector[1] = -1
  elif red_position[1] <= 0:
    red_vector[1] = 1
    
  if red_position[0] >= SCREEN_WIDTH:
    red_vector[0] = -1
  elif red_position[0] <= 0:
    red_vector[0] = 1

  return red_vector	
  
def sign_of(n):  
  if n>0:
    return 1
  elif n<0:
    return -1
  else:
    return 0
  
def chase_players(red_position, player1_position, player2_position, player1_tagged, player2_tagged):

  player1_x_diff = player1_position[0] - red_position[0]
  player1_y_diff = player1_position[1] - red_position[1]

  player2_x_diff = player2_position[0] - red_position[0]
  player2_y_diff = player2_position[1] - red_position[1]

  player1_distance = math.sqrt(player1_x_diff**2 + player1_y_diff**2)
  player2_distance = math.sqrt(player2_x_diff**2 + player2_y_diff**2)	

  if player1_tagged:
    if player2_tagged:
      return [sign_of(SCREEN_WIDTH/2 - red_position[0]), sign_of(SCREEN_HEIGHT/2 - red_position[1])]
    return [sign_of(player2_x_diff), sign_of(player2_y_diff)]
  elif player2_tagged:
    return [sign_of(player1_x_diff), sign_of(player1_y_diff)]
  elif player1_distance < player2_distance:
    return [sign_of(player1_x_diff), sign_of(player1_y_diff)]
  else:
    return [sign_of(player2_x_diff), sign_of(player2_y_diff)]


pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1300
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player1 = pygame.Rect((400, 100, 50, 50))
player1_color = ( 0,250, 0)
player1_is_tagged = False


player2 = pygame.Rect((100,400, 50, 50))
player2_color = ( 0, 0,255)
player2_is_tagged = False
player3 = pygame.Rect(( 0, 0, 50, 50))

player3_vector = [1,1]

font = pygame.font.Font('freesansbold.ttf', 96)
text = font.render('You Lose', True, (0,255,0), (0,0,255))
textRect = text.get_rect()
textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200)

lose_time = 999999

# red_mode = 'diagonal'
red_mode = 'chase'

run = True
while run:

  milliseconds = pygame.time.get_ticks()
  
  screen.fill((0,250,250))

  pygame.draw.rect(screen, player1_color, player1)
  pygame.draw.rect(screen, player2_color, player2)
  pygame.draw.rect(screen, (250, 0, 0), player3)

  key = pygame.key.get_pressed()
  if not player1_is_tagged:
    if key[pygame.K_a] == True and player1.center[0] >= 0:
      player1.move_ip(-4, 0)
    elif key[pygame.K_d] == True and player1.center[0] <= SCREEN_WIDTH:
      player1.move_ip(4, 0)
    elif key[pygame.K_w] == True and player1.center[1] >= 0:
      player1.move_ip(0, -4)
    elif key[pygame.K_s] == True and player1.center[1] <= SCREEN_HEIGHT:
      player1.move_ip(0, 4)

  if not player2_is_tagged:
    if key[pygame.K_LEFT] == True and player2.center[0] >= 0:
      player2.move_ip(-4, 0)
    elif key[pygame.K_RIGHT] == True and player2.center[0] <= SCREEN_WIDTH:
      player2.move_ip(4, 0)
    elif key[pygame.K_UP] == True and player2.center[1] >= 0:
      player2.move_ip(0, -4)
    elif key[pygame.K_DOWN] == True and player2.center[1] <= SCREEN_HEIGHT:
      player2.move_ip(0, 4)

  #print(player3_vector)
  if red_mode == 'diagonal':
    player3_vector = move_diagonally(player3.center, player3_vector)
    
  elif red_mode == 'chase':
    player3_vector = chase_players(player3.center, player1.center, player2.center, player1_is_tagged, player2_is_tagged)
  
  player3.move_ip(player3_vector[0], player3_vector[1])
  
  collision_1_and_2 = pygame.Rect.colliderect(player1, player2)
  collision_1_and_3 = pygame.Rect.colliderect(player1, player3)
  collision_2_and_3 = pygame.Rect.colliderect(player2, player3)
  
  if collision_1_and_3:
    player1_color = ( 0,100, 0)
    player1_is_tagged = True

  if collision_2_and_3:
    player2_color = ( 0, 0, 100)
    player2_is_tagged = True
    
  if collision_1_and_2:
    player1_color = ( 0,255, 0)
    player2_color = ( 0, 0,255)
    player1_is_tagged = False
    player2_is_tagged = False
 
  if player1_is_tagged and player2_is_tagged:
    #print ("you lost")
    screen.blit(text, textRect) 
    if lose_time == 999999:
      lose_time = milliseconds
    
  if milliseconds > lose_time+2000 and player3.center==(SCREEN_WIDTH/2,SCREEN_HEIGHT/2):
    run = False
    
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    
  pygame.display.update()
    
pygame.quit()



