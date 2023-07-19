import pygame

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("ariel", 50)
font2 = pygame.font.SysFont("ariel", 100)
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
img = pygame.transform.scale(pygame.image.load('resources/field.png'),
                             (monitor_size[0], monitor_size[1]))


def draw(x, y, x2, y2, y3, win, elapsed_time, projectiles, all_smashed_projectiles, width, player_width, player_height,
         bullet_width, bullet_height):
    ship_img = pygame.transform.scale(pygame.image.load('resources/space_ship.png'),
                                      (player_width, player_height))
    bullet_img = pygame.transform.scale(pygame.image.load('resources/laser_bullet.png'),
                                        (bullet_width, bullet_height))
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
    win.blit(bullet_img, (x2, y2))
    for projectile in projectiles:
        win.blit(projectile.projectile_img, (projectile.x, y3))
    pygame.display.update()


def draw2(win, x1, x2, y1, y2, player1_bullets, player2_bullets, health1, health2, width, player_width, player_height,
          bullet_width, bullet_height):
    ship_img = pygame.transform.scale(pygame.image.load('resources/space_ship.png'),
                                      (player_width, player_height))
    ship_img1 = pygame.transform.rotate(ship_img, 90)
    ship_img2 = pygame.transform.rotate(ship_img, 270)
    bullet_img = pygame.transform.scale(pygame.image.load('resources/laser_bullet.png'),
                                        (bullet_width, bullet_height))
    bullet_img1 = pygame.transform.rotate(bullet_img, 90)
    bullet_img2 = pygame.transform.rotate(bullet_img, 270)
    health1_text = font.render(f"Player 1 Health: {health1}", True, "red")
    health2_text = font.render(f"Player 2 Health: {health2}", True, "red")
    win.blit(img, (0, 0))
    win.blit(ship_img1, (x1, y1))
    win.blit(ship_img2, (x2, y2))
    for bullet in player1_bullets:
        win.blit(bullet_img1, (bullet.x, bullet.y))
    for bullet in player2_bullets:
        win.blit(bullet_img2, (bullet.x, bullet.y))
    win.blit(health2_text, (0, 0))
    win.blit(health1_text, (width - health2_text.get_width(), 0))
    pygame.display.update()


def start(win, player_width, player_height, bullet_width, bullet_height):
    run = True
    full_screen = True
    single_player = True
    width, height = 1000, 600
    player_x, player_y = width // 2 - player_width // 2, height - player_height
    bullet_x, bullet_y = player_x + player_width // 2 - bullet_width // 2,\
        player_y - bullet_height
    player1_x, player1_y = width - player_height, height // 2 - player_width // 2
    player2_x, player2_y = 0, height // 2 - player_width // 2
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if full_screen:
                        width = monitor_size[0]
                        height = monitor_size[1]
                        win = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                        player_x, player_y = width // 2 - player_width // 2, height - player_height
                        bullet_x, bullet_y = player_x + player_width // 2 - bullet_width // 2, \
                            player_y - bullet_height
                        player1_x, player1_y = width - player_height, height // 2 - player_width // 2
                        player2_x, player2_y = 0, height // 2 - player_width // 2
                        full_screen = False
                    else:
                        width, height = 1000, 600
                        win = pygame.display.set_mode((width, height))
                        player_x, player_y = width // 2 - player_width // 2, height - player_height
                        bullet_x, bullet_y = player_x + player_width // 2 - bullet_width // 2, \
                            player_y - bullet_height
                        player1_x, player1_y = width - player_height, height // 2 - player_width // 2
                        player2_x, player2_y = 0, height // 2 - player_width // 2
                        full_screen = True
                if event.key == pygame.K_q:
                    pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            break
        if keys[pygame.K_m]:
            single_player = False
            break
        start_text = font2.render("Start", True, "white")
        single_text = font.render("press s to play", True, "green")
        multiplayer_text = font.render("press m to play multiplayer", True, 'red')
        win.blit(img, (0, 0))
        win.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 3 - start_text.get_height() // 2))
        win.blit(single_text, (width // 2 - single_text.get_width() // 2,
                               height // 3 - single_text.get_height() // 2 + start_text.get_height()))
        win.blit(multiplayer_text, (width // 2 - multiplayer_text.get_width() // 2,
                                    height // 3 - multiplayer_text.get_height() // 2 + single_text.get_height() +
                                    start_text.get_height()))
        pygame.display.update()
    return width, height, win, full_screen, single_player, player_x, player_y,\
        player1_x, player1_y, player2_x, player2_y, bullet_x, bullet_y


def pause(win, width, height, fps):
    paused = True
    paused_time = 0
    pygame.mixer.music.pause()
    while paused:
        paused_time = 1 / fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:
            pygame.mixer.music.unpause()
            break
        pause_text = font2.render("Pause", True, "white")
        continue_text = font.render("press c to continue", True, "white")
        win.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - pause_text.get_height()))
        win.blit(continue_text, (width // 2 - continue_text.get_width() // 2,
                                 height // 2 - continue_text.get_height() + pause_text.get_height()))
        pygame.display.update()
    return paused_time


def restart(win, width, height, elapsed_time, all_smashed_projectiles, time_to_restart_the_game):
    text = font.render(f"You lost you can restart again in {time_to_restart_the_game // 1000}s ", True, "white")
    time_spent = font.render(f"You lasted {round(elapsed_time)}s", True, "blue")
    record = font.render(f"You destroyed {all_smashed_projectiles} projectiles", True, "red")
    win.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height()))
    win.blit(time_spent, (width // 2 - time_spent.get_width() // 2,
                          height // 2 - time_spent.get_height() + text.get_height()))
    win.blit(record, (width // 2 - record.get_width() // 2,
                      height // 2 - record.get_height() + text.get_height() + time_spent.get_height()))
    pygame.display.update()


def restart2(win, width, height, time_to_restart_the_game, winner):
    winner_text = font2.render(f"The winner is {winner}", True, "green")
    text = font.render(f"You can restart again in {time_to_restart_the_game // 1000}s ", True, "white")
    win.blit(winner_text, (width // 2 - winner_text.get_width() // 2, height // 2 - winner_text.get_height()))
    win.blit(text, (width // 2 - text.get_width() // 2,
                    height // 2 - text.get_height() + winner_text.get_height()))
    pygame.display.update()
