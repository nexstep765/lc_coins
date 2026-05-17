import random
import pygame

# Инициализация Pygame
pygame.init()
window = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Coin pvp")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Ввод уровней игроков через консоль
lvl1 = int(input('Уровень игрока 1? '))
lvl2 = int(input('Уровень игрока 2? '))

# Характеристики игроков
hp1 = 100 + lvl1
dmg1 = 10 + lvl1 / 10
sp1 = 0  # Было sp, переименовано для ясности

hp2 = 100 + lvl2
dmg2 = 10 + lvl2 / 10
sp2 = 0

turn = 1
battle_log = "Нажмите ПРОБЕЛ для столкновения монеток"

# Функция для генерации значения монеты (0 или 1) с учетом sp
def roll_coin(sp_value):
    # Шанс выпадения 1 по умолчанию 50%. sp_value добавляет/отнимает проценты.
    # Например, если sp = 45, шанс станет 50 + 45 = 95%. Если sp = -45, то 5%
    chance_for_one = 50 + sp_value
    chance_for_one = max(0, min(100, chance_for_one)) # Ограничение от 0 до 100
    if random.randint(1, 100) <= chance_for_one:
        return 1
    return 0

# Функция для сброса и генерации новых списков монет для раунда
def reset_coins():
    global coins1, coins2
    amount1 = random.randint(1, 5)
    amount2 = random.randint(1, 5)
    coins1 = [roll_coin(sp1) for _ in range(amount1)]
    coins2 = [roll_coin(sp2) for _ in range(amount2)]

# Инициализируем монеты для первого раунда
reset_coins()

# Игровой цикл
running = True
while running:
    window.fill((30, 30, 30)) # Темный фон
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and hp1 > 0 and hp2 > 0:
                # Расчет силы монет (Уровень + количество монет равных 1)
                coin_power1 = lvl1 + coins1.count(1)
                coin_power2 = lvl2 + coins2.count(1)
                
                if coin_power1 > coin_power2:
                    # Игрок 1 победил в столкновении, у Игрока 2 ломается одна монетка
                    coins2.pop(0)
                    battle_log = "Игрок 1 сильнее! Игрок 2 теряет монетку."
                    # При проигрыше монеты заново перекубируются (получают значения)
                    coins1 = [roll_coin(sp1) for _ in range(len(coins1))]
                    coins2 = [roll_coin(sp2) for _ in range(len(coins2))]
                    # Изменение sp при победе/проигрыше (опционально, можно настроить)
                    sp1 = min(45, sp1 + 5)
                    sp2 = max(-45, sp2 - 5)
                    
                elif TYPE_POWER2 := coin_power2 > coin_power1:
                    # Игрок 2 победил в столкновении, у Игрока 1 ломается одна монетка
                    coins1.pop(0)
                    battle_log = "Игрок 2 сильнее! Игрок 1 теряет монетку."
                    coins1 = [roll_coin(sp1) for _ in range(len(coins1))]
                    coins2 = [roll_coin(sp2) for _ in range(len(coins2))]
                    sp2 = min(45, sp2 + 5)
                    sp1 = max(-45, sp1 - 5)
                else:
                    # Ничья в столкновении
                    battle_log = "Ничья в столкновении! Монеты переброшены."
                    coins1 = [roll_coin(sp1) for _ in range(len(coins1))]
                    coins2 = [roll_coin(sp2) for _ in range(len(coins2))]

                # Проверка: если у кого-то кончились монеты — наносится урон и ход меняется
                if len(coins1) == 0 or len(coins2) == 0:
                    if len(coins1) == 0 and len(coins2) == 0:
                        battle_log = "У обоих кончились монеты! Никто не получил урон."
                    elif len(coins1) == 0:
                        hp1 -= dmg2
                        battle_log = f"У Игрока 1 кончились монеты! Игрок 2 наносит {dmg2} урона."
                    elif len(coins2) == 0:
                        hp2 -= dmg1
                        battle_log = f"У Игрока 2 кончились монеты! Игрок 1 наносит {dmg1} урона."
                    
                    # Начинается новый ход, монеты появляются заново
                    turn += 1
                    reset_coins()

    # --- ОТРИСОВКА ИНТЕРФЕЙСА ---
    
    # Отрисовка Хода (В середине экрана сверху)
    turn_text = font.render(f"Ход: {turn}", True, (255, 215, 0))
    window.blit(turn_text, (350 - turn_text.get_width() // 2, 20))
    
    # Лог событий по центру
    log_text = font.render(battle_log, True, (200, 200, 200))
    window.blit(log_text, (350 - log_text.get_width() // 2, 60))

    # Слева: Характеристики Игрока 1
    pygame.draw.rect(window, (50, 20, 20), (20, 100, 200, 350))
    p1_lvl = font.render(f"Игрок 1 (Lvl {lvl1})", True, (255, 255, 255))
    p1_hp = font.render(f"HP: {max(0, hp1):.1f}", True, (255, 100, 100))
    p1_sp = font.render(f"SP: {sp1}", True, (100, 100, 255))
    window.blit(p1_lvl, (30, 110))
    window.blit(p1_hp, (30, 140))
    window.blit(p1_sp, (30, 170))
    
    # Монетки Игрока 1 (Шарики с цифрами 0 или 1 над ними)
    for i, c_val in enumerate(coins1):
        x = 40 + i * 35
        y = 240
        pygame.draw.circle(window, (212, 175, 55), (x, y), 12) # Золотая монетка
        val_text = font.render(str(c_val), True, (255, 255, 255))
        window.blit(val_text, (x - val_text.get_width()//2, y - 35))

    # Справа: Характеристики Игрока 2
    pygame.draw.rect(window, (20, 20, 50), (480, 100, 200, 350))
    p2_lvl = font.render(f"Игрок 2 (Lvl {lvl2})", True, (255, 255, 255))
    p2_hp = font.render(f"HP: {max(0, hp2):.1f}", True, (255, 100, 100))
    p2_sp = font.render(f"SP: {sp2}", True, (100, 100, 255))
    window.blit(p2_lvl, (490, 110))
    window.blit(p2_hp, (490, 140))
    window.blit(p2_sp, (490, 170))
    
    # Монетки Игрока 2
    for i, c_val in enumerate(coins2):
        x = 500 + i * 35
        y = 240
        pygame.draw.circle(window, (212, 175, 55), (x, y), 12)
        val_text = font.render(str(c_val), True, (255, 255, 255))
        window.blit(val_text, (x - val_text.get_width()//2, y - 35))

    # Проверка на окончание игры
    if hp1 <= 0 or hp2 <= 0:
        win_text = "ИГРОК 1 ПОБЕДИЛ!" if hp2 <= 0 else "ИГРОК 2 ПОБЕДИЛ!"
        end_surf = font.render(win_text, True, (0, 255, 0))
        window.blit(end_surf, (350 - end_surf.get_width()//2, 400))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

