# you can change the configuration down below
def screen_size():
    return 1000, 600  # width, height


def player_conf():
    return 100, 60, 7  # width, height, velocity


def player_health():
    return 5, 5  # player 1, player 2 (for the multiplayer)


def bullet_conf():
    return 6, 20, 15   # width, height, velocity


def max_bullet():
    return 3  # max bullet that player can shoot (for the multiplayer)


def projectile_conf():
    return 60, 60, 1  # width, height, velocity


def projectile_extra_conf():
    return 5, 20, 10
    # number_of_projectiles, time_to_add_projectile_velocity, projectile_required_to_add_bullet_velocity


def fps():
    return 60


def time_to_restart_the_game():
    return 5000  # milliseconds
