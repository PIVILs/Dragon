import pygame
import sys
import pygame.font
from pygame.sprite import Sprite
from pygame.sprite import Group



pygame.init()

screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Dragon")
#game_active = False
#f = False

class Dragon():
    """ Простая модель Дракона."""
    def __init__(self, screen):
        """ Инициализирует атрибуты ракеты."""
        self.screen = screen
        
        # Загрузка изображения корабля и получение прямоугольника.
        self.image = pygame.image.load('images/dragon-1940348_640.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Каждый новый корабль появляется у левого крана экрана.
        self.rect.left = self.screen_rect.left
        self.rect.centery = self.screen_rect.centery
        
        # Флаг перемещения
        self.moving_up = False
        self.moving_down = False
    def update(self):
        """Обновляет позицию с учетом флага"""
        if self.moving_up and self.rect.centery > 0:
            self.rect.centery -= 5
        elif self.moving_down and self.rect.centery < self.screen_rect.bottom:
            self.rect.centery += 5
        
    def blitme(self):
        # Рисует ракету в текущей позиции.
        self.screen.blit(self.image, self.rect)
        
class Bullet(Sprite):
    """ Класс для управления пулями."""
    def __init__(self, bullet_speed_factor, bullet_width,
        bullet_heigth, bullet_color, screen, new_dragon):
        """ Создает объект пули в текущей позиции корабля."""
        super(Bullet, self).__init__()
        self.screen = screen
        
        # Параметры пули
        self.bullet_speed_factor = bullet_speed_factor
        self.bullet_width = bullet_width
        self.bullet_heigth = bullet_heigth
        self.bullet_color = bullet_color
        
        # Создает пули в позиции (0,0) и назначение правильной позиции.
        self.rect = pygame.Rect(0,0, self.bullet_width, self.bullet_heigth)
        self.rect.centerx = new_dragon.rect.right
        self.rect.centery = new_dragon.rect.centery
        
        self.x = self.rect.x
        
    def update(self):
        """ Перемещает пулю вправо по экрану."""
        self.x += self.bullet_speed_factor
        # Обновление позиции прямоугольника.
        self.rect.x = self.x
    def draw_bullet(self):
        """ Вывод пули на экран."""
        pygame.draw.rect(self.screen, self.bullet_color, self.rect)

        
class Target(Sprite):
    """ Класс управления мишенью."""
    def __init__(self, target_speed_factor, target_width,
        target_heigth, target_color, screen, target_limit=3):
        """ Создает мишень в у правой границе экрана."""
        super(Target, self).__init__()
        self.screen = screen
        
        self.screen_rect = screen.get_rect()
        
        # Параметры мишени
        self.target_speed_factor = target_speed_factor
        self.target_width = target_width
        self.target_heigth = target_heigth
        self.target_color = target_color
        self.target_limit = target_limit
        
        # Создает мишень в позиции (0,0) и назначение правильной позиции.
        self.rect = pygame.Rect(0,0, self.target_width, self.target_heigth)
        self.rect.centerx = self.screen_rect.right - self.target_width
        self.rect.centery = self.screen_rect.centery
        self.y = float(self.rect.y)
        #self.game = False


    def update(self):
        """ Перемещает мишень вниз и вверх по экрану."""


        self.y += self.target_speed_factor
        self.rect.centery = self.y
        if self.rect.bottom > 800:
            self.target_speed_factor *= -1

        elif self.rect.top < 0:
            #print(self.rect.top)

            self.target_speed_factor *= -1
        
        # Вывод мишени на экран.
    def blitme(self):
        self.screen.fill(self.target_color, self.rect)


class Button():

    def __init__(self, screen, msg):
        """ Инициализирует атрибуты кнопки."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Назначение размеров и свойств кнопок.
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Построение объекта rect кнопки и выравнивание по центру экрана.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Сообщение кнопки создается только один раз.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """ Преобразует msg в прямоугольник и выравнивает текс по центру."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Отображение пустой кнопки и вывод сообщения.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class GameStats():
    """ Отслеживание статистики для игры Alien Invasion."""

    def __init__(self):
        """ Инициализирует статистику."""
        self.game_active = False

    def reset_stats(self):
        """ Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.ai_settings.ship_limit


def check_events(screen, new_dragon, bullets, play_button, stats, target):
    """ Обрабатывает нажатие клавиш и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #runGame = False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                new_dragon.moving_up = True
            if event.key == pygame.K_DOWN:
                new_dragon.moving_down = True
            if event.key == pygame.K_SPACE:
                new_bullet = Bullet(10, 30, 15, (60, 60, 60),screen, new_dragon)
                bullets.add(new_bullet)
            if event.key == pygame.K_q:
                sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                new_dragon.moving_up = False
            if event.key == pygame.K_DOWN:
                new_dragon.moving_down = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(play_button, stats, target, mouse_x, mouse_y)


def run_game():
    """ Запуск нового цикла игры."""

    new_dragon = Dragon(screen)
    # Создание кнопки Play.
    play_button = Button(screen, "Play")
    bullets = Group()
    target = Target(1, 30, 90, (200, 40, 60), screen)
    stats = GameStats()
    #play_button.draw_button()

    while True:
        #f = False
        game_over(target, stats)
        check_events(screen, new_dragon, bullets, play_button, stats, target)
        #new_dragon.update()
        #bullets.update()
        #target.update()
        
        #screen.fill((250, 250, 250))

        if stats.game_active:

            new_dragon.update()
            bullets.update()
            target.update()

        update_screen(screen, new_dragon, target, bullets, play_button, stats)




            

        # Отображенгие последнего прорисованного окна.
        pygame.display.flip()
        #print(game_active)

def check_play_button(play_button, stats, target, mouse_x, mouse_y):
    """ Запускает игру при нажатии кнопки Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        stats.game_active = True
        target.target_limit = 3
        target.target_speed_factor = 1

def collide_bullet_target(target, bullets):
    """ Коллизия пули и мишени"""
    if pygame.sprite.spritecollide(target, bullets, True):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        target.target_speed_factor *= 1.4
        target.target_limit -=1

def game_over(target, stats):
    if target.target_limit == 0:
        print("You winner!!!")
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_screen(screen, new_dragon, target, bullets, play_button, stats):
    """ Отображает изображения на экране и отображает новый экран."""
    # При каждом проходе цикла перерисовывается экран.
    screen.fill((250, 250, 250))
    # Все пули выводятся позади изображений корабля и пришельцев.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for bullet in bullets.copy():
        if bullet.rect.left > 1200:
            bullets.remove(bullet)
        # print(len(bullets))
    new_dragon.blitme()
    target.blitme()
    collide_bullet_target(target, bullets)
    # Кнопка Play отображается в том случаеб если игра неактивна.
    if not stats.game_active:
        play_button.draw_button()

run_game()