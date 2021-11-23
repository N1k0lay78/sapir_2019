import random
import pygame

del_cheak_list = []
pygame.init()
len_x, len_y = 10, 10
bombs_count = 10
button_sound = pygame.mixer.Sound('button.wav')
images = {'0': 'empety2.bmp', '1': '1.bmp', '2': '2.bmp', '3': '3.bmp', '4': '4.bmp', '5': '5.bmp',
          '6': '6.bmp', '7': '7.bmp', '8': '8.bmp', '?': 'question.bmp', 'f': 'mark.bmp',
          'b': 'bomb.bmp', 'c': 'empty.bmp'}


class Button:
    def __init__(self, width, height, x, y, message, inactive_color=(23, 50, 58),
                 active_color=(23, 100, 58)):
        self.x = x
        self.y = y
        self.message = message
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.can_mark = 0

    def get_level(self):
        return self.can_mark

    def set_level(self, bool=True):
        if bool:
            self.can_mark += 1
        else:
            self.can_mark = 0


class Image:
    def __init__(self, filename, size, coord=(0, 0), transparent_color=(255, 255, 255)):
        self.rotate = 0
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(transparent_color)
        self.size = size
        self.coord = coord

    def draw(self):
        window.blit(self.image, self.coord)

    def get_size(self):
        return self.size

    def get_rect(self):
        return self.coord

    def set_coord(self, x, y):
        self.coord = (x, y)

    def get_coord(self):
        return self.coord


class ImageButton(Button, Image):
    def __init__(self, image, xy=None):
        self.image_b = image
        if xy is None:
            super().__init__(image.get_size()[0], image.get_size()[1], image.get_coord()[0],
                             image.get_coord()[1], '')
        else:
            super().__init__(image.get_size()[0], image.get_size()[1], xy[0], xy[1], '')

    def draw(self, target=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            if click[0] == 1 and target is not None:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(250)
                target()
        self.image_b.draw()


def check_won(level1, level2):
    global bombs_count
    col = 0
    for y in range(len_y):
        for x in range(len_x):
            if level2[y][x] in ['c', 'f', '?']:
                col += 1
    if col == bombs_count:
        won()


def won():
    global run
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        won_b.draw(play)
        btm_b.draw(main)
        pygame.display.update()
        clock.tick(60)


def open_bomb(level1, level2):
    for y in range(len_y):
        for x in range(len_x):
            if level1[y][x] == 'b':
                level2[y][x] = level1[y][x]


def lose(level1, level2):
    global run
    open_bomb(level1, level2)
    buttons = []
    for y in range(len_y):
        for x in range(len_x):
            buttons.append(ImageButton(Image(images[level2[y][x]], (60, 60), (x * 60, y * 60))))
    while run:
        for button in buttons:
            button.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        lose_b.draw(play)
        btm_b.draw(main)
        pygame.display.update()
        clock.tick(60)


def open_level(level1, level2, mouse):
    coords = [(-1, -1), (-1, 1), (-1, 0), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1)]
    open_coords = []
    for coord in coords:
        x, y = (mouse[0] + coord[0], mouse[1] + coord[1])
        # print(x, y, 0 <= x <= len_x - 1 and 0 <= y <= len_y - 1)
        if 0 <= x <= len_x - 1 and 0 <= y <= len_y - 1:
            if level1[y][x] in ['1', '2', '3', '4', '5', '6', '7', '8']:
                level2[y][x] = level1[y][x]
            elif level1[y][x] == '0' and level2[y][x] != '0':
                level2[y][x] = level1[y][x]
                open_coords.append((x, y))
    for open_coord in open_coords:
        open_level(level1, level2, open_coord)


def create_level(pos):
    global bombs, len_x, len_y, bombs_count

    unavailable_list = []
    for x in range(pos[0] - 1, pos[0] + 2):
        for y in range(pos[1] - 1, pos[1] + 2):
            unavailable_list.append((x, y))
    bombs = []
    level1 = []
    level2 = []
    for i in range(len_y):
        a = []
        b = []
        for j in range(len_x):
            a.append('0')
            b.append('c')
        level1.append(a)
        level2.append(b)

    for i in range(bombs_count):
        x, y = random.choice(range(len_x)), random.choice(range(len_y))
        while (x, y) in unavailable_list:
            x, y = random.choice(range(len_x)), random.choice(range(len_y))
        bombs.append([x, y])
        unavailable_list.append((x, y))
        level1[y][x] = 'b'
    for y in range(len_y):
        for x in range(len_x):
            if [x, y] in bombs:
                continue
            else:
                count = 0
                if [x - 1, y - 1] in bombs:
                    count += 1
                if [x, y - 1] in bombs:
                    count += 1
                if [x - 1, y] in bombs:
                    count += 1
                if [x + 1, y] in bombs:
                    count += 1
                if [x, y + 1] in bombs:
                    count += 1
                if [x + 1, y + 1] in bombs:
                    count += 1
                if [x - 1, y + 1] in bombs:
                    count += 1
                if [x + 1, y - 1] in bombs:
                    count += 1
                level1[y][x] = str(count)
    return level1, level2


razrehenie = (len_x * 60, len_y * 60)
window = pygame.display.set_mode(razrehenie)
pygame.display.set_caption('Сапёр')
pygame.display.set_icon(pygame.image.load('icon.bmp'))
clock = pygame.time.Clock()


def play(*args):
    level1, level2 = create_level(pygame.mouse.get_pressed())
    f = False
    create = False
    while True:
        window.fill((255, 255, 255))
        buttons = []
        for x in range(len_x):
            for y in range(len_y):
                buttons.append(ImageButton(Image(images[level2[y][x]], (60, 60), (x * 60, y * 60))))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        for button in buttons:
            button.draw()
        pygame.display.update()
        click = pygame.mouse.get_pressed()
        mouse = (pygame.mouse.get_pos()[0] // 60, pygame.mouse.get_pos()[1] // 60)
        check_won(level1, level2)
        if click[0] == 1:
            if not create:
                # print('create')
                level1, level2 = create_level(mouse)
                create = True
            if level2[mouse[1]][mouse[0]] in ['f', '?']:
                level2[mouse[1]][mouse[0]] = 'c'
                pygame.time.delay(100)
            elif level1[mouse[1]][mouse[0]] == 'b':
                pygame.time.delay(100)
                lose(level1, level2)
            elif level2[mouse[1]][mouse[0]] == 'c':
                if level1[mouse[1]][mouse[0]] == '0':
                    level2[mouse[1]][mouse[0]] = level1[mouse[1]][mouse[0]]
                    open_level(level1, level2, mouse)
                else:
                    level2[mouse[1]][mouse[0]] = level1[mouse[1]][mouse[0]]
                pygame.time.delay(100)
        if click[2] == 1:
            # print(mouse[0])
            if level2[mouse[1]][mouse[0]] == 'c':
                level2[mouse[1]][mouse[0]] = 'f'
                pygame.time.delay(100)
            elif level2[mouse[1]][mouse[0]] == 'f':
                level2[mouse[1]][mouse[0]] = '?'
                pygame.time.delay(100)
        clock.tick(60)


def mode(*args):
    level, _ = create_level((1, 1))
    global run
    while run:
        window.fill((255, 255, 255))
        buttons = []
        for x in range(len(level[0])):
            for y in range(len(level)):
                buttons.append(ImageButton(Image(images[level[y][x]], (60, 60), (x * 60, y * 60))))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for button in buttons:
            button.draw()

        easy_b.draw(easy)
        normal_b.draw(normal)
        hard_b.draw(hard)
        extrahard_b.draw(extra_hard)
        back_b.draw(main)
        pygame.display.update()
        clock.tick(60)


btm_b = ImageButton(Image('btm_b1.bmp', (248, 63), (268, 10)))
won_b = ImageButton(Image('won.bmp', (248, 63), (10, 10)))
lose_b = ImageButton(Image('lose.bmp', (248, 63), (10, 10)))
easy_b = ImageButton(Image('easy.bmp', (500, 64), (50, 50)))
normal_b = ImageButton(Image('normal.bmp', (500, 64), (50, 150)))
hard_b = ImageButton(Image('hard.bmp', (500, 64), (50, 250)))
extrahard_b = ImageButton(Image('extrahard.bmp', (500, 64), (50, 350)))
start_b = ImageButton(Image('play.bmp', (500, 64), (50, 250)))
mode_b = ImageButton(Image('mods.bmp', (500, 64), (50, 350)))
exit_b = ImageButton(Image('exit.bmp', (500, 64), (50, 450)))
back_b = ImageButton(Image('back_b.bmp', (500, 64), (50, 450)))
run = True


def easy(*args):
    global bombs_count, len_x, len_y, window
    len_x, len_y = 10, 10
    window = pygame.display.set_mode((len_x * 60, len_y * 60))
    bombs_count = 10
    play()


def normal(*args):
    global bombs_count, len_x, len_y, window
    len_x, len_y = 15, 12
    window = pygame.display.set_mode((len_x * 60, len_y * 60))
    bombs_count = 40
    play()


def hard(*args):
    global bombs_count, len_x, len_y, window
    len_x, len_y = 20, 15
    window = pygame.display.set_mode((len_x * 60, len_y * 60))
    bombs_count = 60
    play()


def extra_hard(*args):
    global bombs_count, len_x, len_y, window
    len_x, len_y = 25, 15
    window = pygame.display.set_mode((len_x * 60, len_y * 60))
    bombs_count = 90
    play()


def not_run(*args):
    quit()


def main(*args):
    level, _ = create_level((0, 0))
    buttons = []
    for x in range(len(level[0])):
        for y in range(len(level)):
            buttons.append(ImageButton(Image(images[level[y][x]], (60, 60), (x * 60, y * 60))))
    global run
    while run:
        window.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for button in buttons:
            button.draw()

        start_b.draw(play)
        mode_b.draw(mode)
        exit_b.draw(not_run)
        pygame.display.update()
        clock.tick(60)


main()
