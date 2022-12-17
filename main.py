import sys, pygame, random
import const
from objects import Wall, Player, Background, Loser, Score

pygame.init

screen = pygame.display.set_mode(const.WINDOW_SIZE)
clock = pygame.time.Clock()

def main():
    pygame.init()
    pygame.mixer.music.load(const.MUSIC_FILENAME)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1)
    while 1:

        highscore: int = 0
        
        f = open("hackathon/high_score.txt", "r")
        for line in f:
            highscore = int(line)
        f.close

        player = Player()
        background = Background()
        player_vel_y: int = 0
        player_vel_x: int = 0
        timer: int = 0
        counter: int = 0
        countinuer: bool = False

        wall_list: list[Wall] = []

        while 1:
            time_delta = clock.tick(60)
            screen.fill((0, 0, 0))

            counter += 1
            i = 0

            if counter % const.DIFFICULTY_COEFFICIENT == 0:
                timer += 1
                counter = 0
                while i < const.WALLS:
                    wall_new: Wall = Wall( const.WIDTH + 50, random.randint(0, const.FLOOR), const.OBS_SIZE, const.OBS_SIZE)
                    wall_list.append(wall_new)
                    i += 1

            for wall in wall_list:
                wall.rect.centerx = wall.rect.centerx - (const.INIT_SPEED + int(timer))

            if player.vel_x > const.MOVEMENT:
                player.vel_x -= const.FRICTION
            elif player.vel_x > 0:
                player.vel_x -= player.vel_x
            elif player.vel_x < -const.MOVEMENT:
                player.vel_x += const.FRICTION
            elif player.vel_x < 0:
                player.vel_x += -(player.vel_x)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    if timer*60 > highscore:
                        f = open("hackathon/high_score.txt", "r+")
                        f.truncate(0)
                        f.write(str(timer*60) + "\n")
                        f.close
                        score.highscore()
                    else:
                        f = open("hackathon/high_score.txt", "r+")
                        f.truncate(0)
                        f.write(str(highscore) + "\n")
                        f.close
                        score.highscore()
                    sys.exit()
            pressed_keys = pygame.key.get_pressed()
            player.update(pressed_keys)
            player.vel_y += const.GRAV

            player.rect.centerx += player.vel_x
            player.rect.centery += player.vel_y

            if player.rect.centery >= const.FLOOR:
                player.rect.centery = const.FLOOR
                player.vel_y = 0

            j: int = 0
            while j < len(wall_list):
                if wall_list[j].rect.centerx < -5:
                    wall_list.pop(j)
                j += 1

            background.update(timer)

            background.render(screen)
            for wall in wall_list:
                screen.blit(wall.surf, wall.rect)

            if player.collide(wall_list):
                player.vel_x = 0
                player.vel_y = 0
                loser: Loser = Loser(player)
                score.end(timer)
                screen.blit(score.text_surface, score.font_rect)
                screen.blit(loser.surf, loser.rect)
                if timer*60 > highscore:
                    f = open("hackathon/high_score.txt", "r+")
                    f.truncate(0)
                    f.write(str(timer*60) + "\n")
                    f.close
                    score.highscore()
                else:
                    score.lower_score(highscore)
                screen.blit(score.text_surface, score.font_rect)
                score.restart()
                screen.blit(score.text_surface, score.font_rect)
                pygame.display.flip()
                while True:
                    score.restart()
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
                            sys.exit()
                        elif(event.type == pygame.KEYDOWN):
                            countinuer = True
                            break
                    if countinuer:
                        break
            
            if countinuer:
                break

            score: Score = Score(timer)
            screen.blit(score.text_surface, score.font_rect)
            

            screen.blit(player.surf, player.rect)


        
            pygame.display.flip()


if __name__ == '__main__':
    main()