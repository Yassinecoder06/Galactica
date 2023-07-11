import pygame
import random

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("comicsansms", 30)
font2 = pygame.font.SysFont("comicsansms", 60)
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
# you can change the configuration down below
player_width = 100
player_height = 60
player_velocity = 6
bullet_width = 6
bullet_height = 10
projectile_width = 60
projectile_height = 60
number_of_projectiles = 5
fps = 60
time_to_restart_the_game = 10000  # milliseconds
# end
pygame.display.set_caption("Galactica game")
img = pygame.transform.scale(pygame.image.load('resources/field.jpg'),
                             (monitor_size[0], monitor_size[1]))
ship_img = pygame.transform.scale(pygame.image.load('resources/space_ship.png'),
                                  (player_width, player_height))
pygame.mixer.music.load('resources/background.wav')
pygame.mixer.music.play(-1)
explosion_sound = pygame.mixer.Sound('resources/explosion.wav')
bullet_sound = pygame.mixer.Sound('resources/bullet.wav')


class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def collide(self, x3, y3):
        distance = abs(self.y + player_height // 2 - y3)
        condition = self.x - player_width // 2 <= x3 <= self.x + player_width
        return (distance <= projectile_height or distance <= player_height) and condition


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def collide(self):
        return self.y <= 0

    def collide_projectile(self, x3, y3):
        distance = abs(self.y - y3)
        condition = x3 <= self.x <= x3 + projectile_width
        return condition and distance <= projectile_height


class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.projectile_img = pygame.transform.scale(pygame.image.load('resources/projectile.png'),
                                                     (projectile_width, projectile_height))

    def collide(self, height):
        return self.y >= height


def draw(x, y, x2, y2, y3, win, elapsed_time, projectiles, all_smashed_projectiles, width):
    time_text = font.render(f"Time: {round(elapsed_time)}s", True, "white")
    score = font.render(f"Score : {all_smashed_projectiles}", True, "red")
    smashing_average = font.render(f"Smashing Average : "
                                   f"{round(all_smashed_projectiles / (elapsed_time + 0.01), 2)} p/s",
                                   True, "green")
    win.blit(img, (0, 0))
    win.blit(ship_img, (x, y))
    win.blit(time_text, (0, 0))
    win.blit(score, (width - score.get_width(), 0))
    win.blit(smashing_average,
             (width // 2 - smashing_average.get_width() // 2, 0))
    bullet = pygame.Rect(x2, y2, bullet_width, bullet_height)
    pygame.draw.rect(win, "white", bullet)
    for projectile in projectiles:
        win.blit(projectile.projectile_img, (projectile.x, y3))
    pygame.display.update()


def pause(win, width, height):
    paused = True
    paused_time = 0
    while paused:
        paused_time = 1 / fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
        pause_text = font2.render("Pause", True, "white")
        continue_text = font.render("press c to continue", True, "white")
        win.blit(pause_text, (width // 2 - pause_text.get_width() // 2,
                              height // 2 - pause_text.get_height()))
        win.blit(continue_text, (width // 2 - continue_text.get_width() // 2,
                                 height // 2 - continue_text.get_height() + pause_text.get_height()))
        pygame.display.update()
    return paused_time


def main():
    run = True
# you can change the size of the first screen
    width, height = 1000, 667
# end
    screen = pygame.display.set_mode((width, height))
    full_screen = True
    clock = pygame.time.Clock()
    x = width // 2
    y = height - player_height
    x2 = x + player_width // 2 - bullet_width + 3
    y2 = y
    x3 = 0
    y3 = 0
    projectiles = []
    all_smashed_projectiles = 0
    smashed_projectile = 0
    elapsed_time = 0
# you can change the configuration down below
    bullet_velocity = 20
    projectile_velocity = 1
    time_to_add_projectile_velocity = 20
    projectile_required_to_add_bullet_velocity = 10
# end
    while run:
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
                        full_screen = False
                    else:
                        width = 1000
                        height = 667
                        screen = pygame.display.set_mode((width, height))
                        full_screen = True
                if event.key == pygame.K_p:
                    pause(screen, width, height)
                    elapsed_time -= pause(screen, width, height)
                if event.key == pygame.K_q:
                    run = False

        ship = Ship(x, y)
        bullet = Bullet(x2, y2)
        projectile = Projectile(x3, y3)

        if y3 == 0:
            for _ in range(number_of_projectiles):
                x3 = random.randint(projectile_width + player_width // 2,
                                    width - projectile_width - player_width // 2)
                projectile = Projectile(x3, y3)
                projectiles.append(projectile)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and x - player_velocity >= 0:
            x -= player_velocity
        if keys[pygame.K_RIGHT] and x + player_velocity + player_width <= width:
            x += player_velocity
        if keys[pygame.K_UP] and y - player_velocity >= 0:
            y -= player_velocity
        if keys[pygame.K_DOWN] and y + player_velocity + player_height <= height:
            y += player_velocity

        for i in projectiles:
            if ship.collide(i.x, y3):
                text = font.render(f"You lost you can restart again in {time_to_restart_the_game // 1000}s ",
                                   True, "white")
                time_spent = font.render(f"You lasted {round(elapsed_time)}s", True, "blue")
                record = font.render(f"You destroyed {all_smashed_projectiles} projectiles", True, "red")
                screen.blit(text, (width // 2 - text.get_width() // 2,
                                   height // 2 - text.get_height()))
                screen.blit(time_spent, (width // 2 - time_spent.get_width() // 2,
                                         height // 2 - time_spent.get_height() + text.get_height()))
                screen.blit(record, (width // 2 - record.get_width() // 2,
                                     height // 2 - record.get_height() + text.get_height() + time_spent.get_height()))
                pygame.display.update()
                pygame.time.delay(time_to_restart_the_game)
                elapsed_time = 0.01
                all_smashed_projectiles = 0
                smashed_projectile = 0
                y3 = 0
                x = width // 2
                y = height - player_height
            if bullet.collide_projectile(i.x, y3):
                explosion_sound.play()
                projectiles.remove(i)
                smashed_projectile += 1
                all_smashed_projectiles += 1

        if bullet.collide():
            y2 = y
            x2 = x + player_width // 2 - bullet_width + 3
            bullet_sound.play()
        if projectile.collide(height) or smashed_projectile == number_of_projectiles:
            y3 = 0
            smashed_projectile = 0
            projectiles.clear()
            for _ in range(number_of_projectiles):
                x3 = random.randint(projectile_width + player_width // 2,
                                    width - projectile_width - player_width // 2)
                projectile = Projectile(x3, y3)
                projectiles.append(projectile)
        if elapsed_time >= time_to_add_projectile_velocity:
            projectile_velocity += 0.5
            time_to_add_projectile_velocity += time_to_add_projectile_velocity
        if all_smashed_projectiles >= projectile_required_to_add_bullet_velocity:
            bullet_velocity += 2
            projectile_required_to_add_bullet_velocity += projectile_required_to_add_bullet_velocity
        y2 -= bullet_velocity
        y3 += projectile_velocity
        draw(x, y, x2, y2, y3, screen, elapsed_time, projectiles, all_smashed_projectiles, width)
    pygame.quit()


if __name__ == "__main__":
    main()
