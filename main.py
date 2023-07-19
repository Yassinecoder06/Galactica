import pygame
import random
from screen import sound, view, configuration

pygame.init()
pygame.display.set_caption("Galactica game")
player_width, player_height, player_velocity = configuration.player_conf()
bullet_width, bullet_height, bullet_vel_multiplayer = configuration.bullet_conf()
projectile_width, projectile_height, _ = configuration.projectile_conf()
number_of_projectiles, _, _ = configuration.projectile_extra_conf()
fps = configuration.fps()
time_to_restart_the_game = configuration.time_to_restart_the_game()
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
player1_hit = pygame.USEREVENT + 1
player2_hit = pygame.USEREVENT + 2
sound.background_sound()


class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def collide(self, x, y):
        distance = abs(self.y + player_height // 2 - y)
        condition = self.x - player_width // 2 <= x <= self.x + player_width
        return (distance <= projectile_height or distance <= player_height) and condition


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def collide(self):
        return self.y <= 0

    def collide_projectile(self, x, y):
        distance = abs(self.y - y)
        condition = x <= self.x <= x + projectile_width
        return condition and distance <= projectile_height


class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.projectile_img = pygame.transform.scale(pygame.image.load('resources/projectile.png'),
                                                     (projectile_width, projectile_height))

    def collide(self, height):
        return self.y >= height


# multiplayer classes and functions
def bullet_collision(player1_bullets, player2_bullets, player1, player2, health_player1, health_player2, width):
    for bullet in player1_bullets:
        bullet.x -= bullet_vel_multiplayer
        if player2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(player2_hit))
            player1_bullets.remove(bullet)
        if bullet.x <= 0:
            player1_bullets.remove(bullet)
    for bullet in player2_bullets:
        bullet.x += bullet_vel_multiplayer
        if player1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(player1_hit))
            player2_bullets.remove(bullet)
        if bullet.x >= width - bullet_width:
            player2_bullets.remove(bullet)
    return health_player1, health_player2
# end


def main():
    run = True
    width, height = configuration.screen_size()
    _, _, projectile_velocity = configuration.projectile_conf()
    _, time_to_add_projectile_velocity, projectile_required_to_add_bullet_velocity =\
        configuration.projectile_extra_conf()
    _, clone_time_to_add_projectile_velocity, clone_projectile_required_to_add_bullet_velocity =\
        configuration.projectile_extra_conf()
    _, _, bullet_velocity = configuration.bullet_conf()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    player0 = pygame.Rect(width // 2 - player_width // 2, height - player_height, player_width, player_height)
    bullet0 = pygame.Rect(player0.x + player_width // 2 - bullet_width // 2, player0.y - bullet_height,
                          bullet_width, bullet_height)
    projectile0 = pygame.Rect(0, 0, projectile_width, projectile_height)
    projectiles = []
    all_smashed_projectiles = 0
    smashed_projectile = 0
    elapsed_time = 0
# multiplayer
    player1 = pygame.Rect(width - player_height, height // 2 - player_width // 2, player_height, player_width)
    player2 = pygame.Rect(0, height // 2 - player_width // 2, player_height, player_width)
    max_bullet = configuration.max_bullet()
    health_player1, health_player2 = configuration.player_health()
    player1_bullets = []
    player2_bullets = []
# end
    width, height, screen, full_screen, single_player, player0.x, player0.y, \
        player1.x, player1.y, player2.x, player2.y, bullet0.x, bullet0.y =\
        view.start(screen, player_width, player_height, bullet_width, bullet_height)
    while run:
        if single_player:
            clock.tick(fps)
            elapsed_time += 1 / fps
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        if full_screen:
                            width = monitor_size[0]
                            height = monitor_size[1]
                            screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                            player0.x, player0.y = width // 2 - player_width // 2, height - player_height
                            bullet0.x, bullet0.y = player0.x + player_width // 2 - bullet_width // 2,\
                                player0.y - bullet_height
                            full_screen = False
                        else:
                            width, height = configuration.screen_size()
                            screen = pygame.display.set_mode((width, height))
                            player0.x, player0.y = width // 2, height - player_height
                            bullet0.x, bullet0.y = player0.x + player_width // 2 - bullet_width // 2,\
                                player0.y - bullet_height
                            full_screen = True
                    if event.key == pygame.K_p:
                        view.pause(screen, width, height, fps)
                        elapsed_time -= view.pause(screen, width, height, fps)
                    if event.key == pygame.K_q:
                        run = False

            ship = Ship(player0.x, player0.y)
            bullet = Bullet(bullet0.x, bullet0.y)
            projectile = Projectile(projectile0.x, projectile0.y)

            if projectile0.y == 0:
                for _ in range(number_of_projectiles):
                    projectile0.x = random.randint(projectile_width + player_width // 2,
                                                   width - projectile_width - player_width // 2)
                    projectile = Projectile(projectile0.x, projectile0.y)
                    projectiles.append(projectile)

            bullet0.y -= bullet_velocity
            projectile0.y += projectile_velocity
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player0.x - player_velocity >= 0:
                player0.x -= player_velocity
            if keys[pygame.K_RIGHT] and player0.x + player_velocity + player_width <= width:
                player0.x += player_velocity
            if keys[pygame.K_UP] and player0.y - player_velocity >= 0:
                player0.y -= player_velocity
            if keys[pygame.K_DOWN] and player0.y + player_velocity + player_height <= height:
                player0.y += player_velocity

            for i in projectiles:
                if ship.collide(i.x, projectile0.y):
                    view.restart(screen, width, height, elapsed_time, all_smashed_projectiles, time_to_restart_the_game)
                    projectile0.y = 0
                    pygame.time.delay(time_to_restart_the_game)
                    projectiles.clear()
                    all_smashed_projectiles = 0
                    smashed_projectile = 0
                    elapsed_time = 0.01
                    player0.x = width // 2
                    player0.y = height - player_height
                    _, _, bullet_velocity = configuration.bullet_conf()
                    _, _, projectile_velocity = configuration.projectile_conf()
                    _, time_to_add_projectile_velocity, projectile_required_to_add_bullet_velocity =\
                        configuration.projectile_extra_conf()
                if bullet.collide_projectile(i.x, projectile0.y):
                    sound.explosion_sound()
                    projectiles.remove(i)
                    smashed_projectile += 1
                    all_smashed_projectiles += 1

            if bullet.collide():
                bullet0.y = player0.y - bullet_height
                bullet0.x = player0.x + player_width // 2 - bullet_width // 2
                sound.bullet_sound()
            if projectile.collide(height) or smashed_projectile == number_of_projectiles:
                projectile0.y = 0
                smashed_projectile = 0
                projectiles.clear()
            if elapsed_time >= time_to_add_projectile_velocity:
                projectile_velocity += 0.5
                time_to_add_projectile_velocity += clone_time_to_add_projectile_velocity
            if all_smashed_projectiles >= projectile_required_to_add_bullet_velocity:
                bullet_velocity += 2
                projectile_required_to_add_bullet_velocity += clone_projectile_required_to_add_bullet_velocity
            view.draw(player0.x, player0.y, bullet0.x, bullet0.y, projectile0.y, screen, elapsed_time,
                      projectiles, all_smashed_projectiles, width, player_width, player_height,
                      bullet_width, bullet_height)
        else:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == player1_hit:
                    health_player1 -= 1
                if event.type == player2_hit:
                    health_player2 -= 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        if full_screen:
                            width = monitor_size[0]
                            height = monitor_size[1]
                            screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                            player1.x, player1.y = width - player_height, height // 2 - player_width // 2
                            player2.x, player2.y = 0, height // 2 - player_width // 2
                            full_screen = False
                        else:
                            width, height = configuration.screen_size()
                            screen = pygame.display.set_mode((width, height))
                            player1.x, player1.y = width - player_height, height // 2 - player_width // 2
                            player2.x, player2.y = 0, height // 2 - player_width // 2
                            full_screen = True
                    if event.key == pygame.K_p:
                        view.pause(screen, width, height, fps)
                        elapsed_time -= view.pause(screen, width, height, fps)
                    if event.key == pygame.K_q:
                        run = False
                    if event.key == pygame.K_RCTRL and len(player1_bullets) < max_bullet:
                        sound.bullet_sound()
                        bullet_player1 = pygame.Rect(player1.x - bullet_height,
                                                     player1.y + player_width // 2 - bullet_width // 2,
                                                     bullet_height, bullet_width)
                        player1_bullets.append(bullet_player1)
                    if event.key == pygame.K_LCTRL and len(player2_bullets) < max_bullet:
                        sound.bullet_sound()
                        bullet_player2 = pygame.Rect(player2.x + player_height,
                                                     player2.y + player_width // 2 - bullet_width // 2,
                                                     bullet_height, bullet_width)
                        player2_bullets.append(bullet_player2)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player1.x - player_velocity >= width // 2:
                player1.x -= player_velocity
            if keys[pygame.K_RIGHT] and player1.x + player_velocity + player_height <= width:
                player1.x += player_velocity
            if keys[pygame.K_UP] and player1.y - player_velocity >= 0:
                player1.y -= player_velocity
            if keys[pygame.K_DOWN] and player1.y + player_velocity + player_width <= height:
                player1.y += player_velocity
            if keys[pygame.K_s] and player2.x - player_velocity >= 0:
                player2.x -= player_velocity
            if keys[pygame.K_d] and player2.x + player_velocity + player_height <= width // 2:
                player2.x += player_velocity
            if keys[pygame.K_e] and player2.y - player_velocity >= 0:
                player2.y -= player_velocity
            if keys[pygame.K_x] and player2.y + player_velocity + player_width <= height:
                player2.y += player_velocity

            bullet_collision(player1_bullets, player2_bullets, player1, player2, health_player1, health_player2, width)
            view.draw2(screen, player1.x, player2.x, player1.y, player2.y, player1_bullets, player2_bullets,
                       health_player1, health_player2, width, player_width, player_height, bullet_width, bullet_height)

            if health_player1 <= 0:
                winner = " Player 2"
                view.restart2(screen, width, height, time_to_restart_the_game, winner)
                pygame.time.delay(time_to_restart_the_game)
                player1_bullets.clear(), player2_bullets.clear()
                health_player1, health_player2 = configuration.player_health()
                player1.x, player1.y = width - player_height, height // 2 - player_width // 2
                player2.x, player2.y = 0, height // 2 - player_width // 2
            if health_player2 <= 0:
                winner = "Player 1"
                view.restart2(screen, width, height, time_to_restart_the_game, winner)
                pygame.time.delay(time_to_restart_the_game)
                player1_bullets.clear(), player2_bullets.clear()
                health_player1, health_player2 = configuration.player_health()
                player1.x, player1.y = width - player_height, height // 2 - player_width // 2
                player2.x, player2.y = 0, height // 2 - player_width // 2

    pygame.quit()


if __name__ == "__main__":
    main()
