import pygame
import time
import random

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("comicsans", 30)
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

player_width = 100
player_height = 60
player_velocity = 5
bullet_width = 6
bullet_height = 10
bullet_velocity = 15
projectile_width = 50
projectile_height = 50
number_of_projectiles = 4

pygame.display.set_caption("Galactica game")
img = pygame.transform.scale(pygame.image.load('resources/field.jpg'),
                             (monitor_size[0], monitor_size[1]))
ship_img = pygame.transform.scale(pygame.image.load('resources/space_ship.png'),
                                  (player_width, player_height))


class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def collide(self, x3, y3, vel):
        dis = abs(self.y + player_height // 2 - y3 - vel)
        if dis <= projectile_height and self.x - player_width // 2 <= x3 <= self.x + player_width:
            return True


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def collide(self):
        return self.y <= 0

    def collide_projectile(self, x3, y3):
        dis = abs(self.y - y3)
        if x3 <= self.x <= x3 + projectile_width and dis <= projectile_height:
            return True


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
    win.blit(img, (0, 0))
    win.blit(ship_img, (x, y))
    win.blit(time_text, (0, 0))
    win.blit(score, (width - score.get_width(), 0))
    bullet = pygame.Rect(x2, y2, bullet_width, bullet_height)
    pygame.draw.rect(win, "white", bullet)
    for projectile in projectiles:
        win.blit(projectile.projectile_img, (projectile.x, y3))
    pygame.display.update()


def main():
    run = True
    width, height = 1000, 667
    screen = pygame.display.set_mode((width, height))
    full_screen = True

    x = width // 2
    y = height - player_height
    x2 = x + player_width // 2 - bullet_width + 3
    y2 = y
    x3 = 0
    y3 = 0
    projectiles = []
    projectile_velocity = 3
    all_smashed_projectiles = 0
    smashed_projectile = 0

    clock = pygame.time.Clock()
    start_time = time.time()
    t = 10
    while run:
        clock.tick(90)
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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

        ship = Ship(x, y)
        bullet = Bullet(x2, y2)
        projectile = Projectile(x3, y3)

        if y3 == 0:
            for _ in range(number_of_projectiles):
                x3 = random.randint(projectile_width, width - projectile_width)
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

        for i in range(number_of_projectiles):
            if ship.collide(projectiles[i - smashed_projectile].x, y3, projectile_velocity):
                text = font.render(f"You lost you can restart again in 5s ", True, "white")
                time_spent = font.render(f"You lasted {round(elapsed_time)}s", True, "blue")
                record = font.render(f"You destroyed {round(all_smashed_projectiles)} projectiles", True, "red")
                screen.blit(text, (width // 2 - text.get_width() // 2,
                                   height // 2 - text.get_height()))
                screen.blit(time_spent, (width // 2 - time_spent.get_width() // 2,
                                         height // 2 - time_spent.get_height() + text.get_height()))
                screen.blit(record, (width // 2 - record.get_width() // 2,
                                     height // 2 - record.get_height() + text.get_height() + time_spent.get_height()))
                pygame.display.update()
                pygame.time.delay(5000)
                pygame.quit()
            if bullet.collide_projectile(projectiles[i - smashed_projectile].x, y3):
                projectiles.remove(projectiles[i - smashed_projectile])
                smashed_projectile += 1
                all_smashed_projectiles += 1
                if smashed_projectile == number_of_projectiles:
                    smashed_projectile = 0

        if bullet.collide():
            y2 = y
            x2 = x + player_width // 2 - bullet_width + 3
        if projectile.collide(height):
            y3 = 0
            smashed_projectile = 0
            projectiles.clear()
            for _ in range(number_of_projectiles):
                x3 = random.randint(projectile_width, width - projectile_width)
                projectile = Projectile(x3, y3)
                projectiles.append(projectile)
        if elapsed_time >= t:
            projectile_velocity += 1
            t += 10
        y2 -= bullet_velocity
        y3 += projectile_velocity
        draw(x, y, x2, y2, y3, screen, elapsed_time, projectiles, all_smashed_projectiles, width)


if __name__ == "__main__":
    main()
