import pygame, random
gcn = lambda i, j: [[x, y] for x in [i - 1, i, i + 1] for y in [j - 1, j, j + 1] if 0 <= x < col and 0 <= y < row]
click = lambda i: event.type == pygame.MOUSEBUTTONDOWN and event.button == i
press = lambda k: event.type == pygame.KEYDOWN and event.key == k
right = lambda x, y: {'#': '?', '?': ' ', ' ': '#'}.get(show[x][y], show[x][y])
def update(i, j):
    if j in [0, 3]: return 0
    for i in range(3):
        try: var[i] = int(e_str[i])
        except: return 0
    if i in [0, 1] and var[i] > (j - 3) * 9 and var[i] > 9: return 1
    elif i == 2 and var[2] > 1 + (j - 4) * 9 and var[2] < var[0] * var[1] + (j - 3) * 9: return 1
    return 0
def pydraw(rect, i, j, k):
    pygame.draw.rect(screen, i, rect)
    pygame.draw.rect(screen, j, rect, k)
def getrect(i, rect, bg, j):
    pydraw(rect, bg, COLOR[8], j)
    if i not in text: text[i] = font.render(i, 1, COLOR[8])
    screen.blit(text[i], text[i].get_rect(center = rect.center))
def header(i):
    screen.fill(COLOR[10])
    if i not in text: text[i] = font.render(i, 1, COLOR[8])
    screen.blit(text[i], text[i].get_rect(center = (screen.get_width() // 2, screen.get_height() // 2)))
    pygame.display.flip()
def check(cols, rows):
    stack1, stack2 = [], []
    for x, y in gcn(cols, rows): 
        if show[x][y] in ' #?': stack1.append([x, y])
        if show[x][y] == ' ': stack2.append([x, y])
    return stack1, stack2
def left(gx, gy):
    global mine, timer
    if mode[0]:
        safe = [[x, y] for x in range(col) for y in range(row) if [x, y] not in gcn(gx, gy)]
        mine, mode[0] = random.sample(safe, minenum), 0
    if show[gx][gy] == ' ': stack = [[gx, gy]]
    else: stack = [[x, y] for x, y in gcn(gx, gy) if show[x][y] == ' ']
    while stack:
        i, j = stack.pop()
        show[i][j] = str(sum(x in mine for x in gcn(i, j)))
        if [i, j] in mine:
            mode[0], timer = 2, now
            for mx, my in mine: show[mx][my] = '!'
            break
        if show[i][j] == '0':
            for nx, ny in gcn(i, j):
                if [nx, ny] not in stack and show[nx][ny] == ' ': stack.append([nx, ny])
    if not mode[0] and minenum == sum(c in ' #?' for r in show for c in r): mode[0], timer = 3, now
def tips():
    checklist = [(i, j) for i in range(col) for j in range(row)]
    while not mode[0] and len(checklist):
        i, j = checklist.pop(random.randrange(len(checklist)))
        if show[i][j] not in '12345678': continue
        stack = check(i, j)
        if len(stack[0]) == int(show[i][j]) and len(stack[1]):
            x, y = stack[1][random.randrange(len(stack[1]))]
            show[x][y] = right(x, y)
COLOR = [(255, 255, 255), (0, 255, 0), (30, 144, 255), (255, 127, 0), (0, 0, 255),
          (255, 0, 0), (139, 69, 19), (128, 128, 128), (0, 0, 0), (100, 150, 200), (192, 192, 192)]
ALPHABETS= 'abcdefghijklmnopqrstuvwxyz'
var, mode = [10, 10, 10], [0, 0, 0]
kind, name = ['columns', 'rows', 'mine numbers'], [' ', '+10', '+1', ' ', '-1', '-10']
pygame.init()
time = pygame.time.Clock()
pygame.display.set_caption('掃雷3.1')
pygame.key.stop_text_input()
try: font = pygame.font.Font("C:/Windows/Fonts/simhei.ttf", 20)
except: font = pygame.font.Font(None, 20)
phase, btn, cell, run, timer, text = 'prepare', {}, {}, 1, 0, {'確定?': font.render('確定?', 1, COLOR[8])}
for i in range(3):
    for j in [': ', ' invalid']: text[str(i) + j] = font.render(kind[i] + j, 1, COLOR[8])
    for j in range(6): btn[i, j] = pygame.Rect(45 + j * 100, 45 + i * 45, 80, 40)
for i in range(4): text['L' + ' .' * i] = font.render('loading' + ' .' * i, 1, COLOR[8])
title = [font.render(i, 1, COLOR[8]) for i in ['Can you solve it?', 'You lose!', 'You win!']]
ync_rect = [pygame.Rect(i) for i in [(250, 145, 60, 30), (330, 145, 60, 30), (445, 180, 80, 40)]]
overlay = pygame.Surface((640, 280), pygame.SRCALPHA)
overlay.fill((200, 200, 200, 180))
while run:
    if phase == 'prepare':
        screen = pygame.display.set_mode((640, 280))
        mode[0], active, phase, e_str = 1, None, 'main', [str(i) for i in var]
    time.tick(30)
    pos, now = pygame.mouse.get_pos(), pygame.time.get_ticks()
    for event in pygame.event.get():
        if phase == 'ask':
            if event.type == pygame.QUIT or press(pygame.K_n): run = 0
            if press(pygame.K_y): phase = 'prepare'
        if event.type == pygame.QUIT: phase = 'ask'
        if phase == 'main':
            if click(1):
                active = next((i for i in range(3) if btn[i, 3].collidepoint(pos)), None)
                if ync_rect[2].collidepoint(pos) and update(0, 1): phase = 'confirm'
                for (i, j), rect in btn.items():
                    if rect.collidepoint(pos) and update(i, j):
                        var[i] += int(name[j])
                        e_str[i] = str(var[i])
            if press(pygame.K_RETURN) and update(0, 1): phase = 'confirm'
            if event.type == pygame.KEYDOWN and active is not None:
                i = active
                if event.key == pygame.K_BACKSPACE: e_str[i] = e_str[i][:-1]
                elif event.unicode.isdigit() and len(e_str[i]) < 7: e_str[i] += event.unicode
                try: var[i] = int(e_str[i])
                except: var[i] = 0
        elif phase == 'confirm':
            if press(pygame.K_RETURN) or click(1) and ync_rect[0].collidepoint(pos):
                phase, show_error = 'processing', []
                errors = [i for i in range(2) if var[i] < 10]
                for i in errors: var[i] = 10
                if var[2] > var[0] * var[1] - 9 or var[2] < 1: 
                    errors.append(2)
                    var[2] = var[0] +var[1] - 1
                col, row, minenum = var
                show = [[' '] * row for _ in range(col)]
                for i in range(col):
                    for j in range(row): cell[i, j] = pygame.Rect(i * 20, 40 + j * 20, 20, 20)
            elif click(1) and ync_rect[1].collidepoint(pos): phase = 'main'
        elif phase == 'done': 
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                gx, gy = x // 20, y  // 20 - 2
                if mode[0] > 1 or not (0 <= gx < col and 0 <= gy < row): continue
            if event.type == pygame.KEYDOWN and event.unicode in ALPHABETS: tips()
            if click(1): left(gx, gy)
            if click(3): show[gx][gy] = right(x, y)
    screen.fill(COLOR[10 if phase == 'done' else 0])
    if phase == 'main':
        for i in range(3):
            screen.blit(text['%d: ' % i], text['%d: ' % i].get_rect(center = btn[i, 0].center))
            for j in [1, 2, 4, 5]:
                btnCOLOR = COLOR[9] if update(i, j) else (180, 180, 180)
                getrect(name[j], btn[i, j], btnCOLOR, 1)
            getrect(e_str[i], btn[i, 3], (255, 255, 200 if active == i else 255), 2)
        getrect('確定', ync_rect[2], COLOR[9], 2)
    elif phase == 'confirm':
        screen.blit(overlay, (0, 0))
        pydraw((220, 90, 200, 100), COLOR[0], COLOR[8], 2)
        screen.blit(text['確定?'], (300, 105))
        for i in [0, 1]: getrect(['是', '否'][i], ync_rect[i], (200, 200, 200), 2)
    elif phase == 'processing':
        if show_error and now - timer < 200: pass
        elif len(show_error) <= len(errors):
            timer = now
            if len(show_error) < len(errors):
                i = errors[len(show_error)]
                show_error.append('%d invalid' % i)
                var[i] = 10
            else: show_error.append('L')
        elif now - timer < 800: show_error[len(show_error) - 1] = 'L' + ' .' * ((now - timer) // 200)
        else: 
            phase = 'done'
            screen = pygame.display.set_mode((col * 20, row * 20 + 40))
        for i, j in enumerate(show_error): screen.blit(text[j], (50, 50 + i * 30))
    elif phase == 'done': 
        screen.blit(title[mode[0] - 1 if mode[0] else 0], (10, 10))
        for (i, j), rect in cell.items():
            if show[i][j] in ' #?': fill = [2, COLOR[8],  (211, 211, 211)]
            elif show[i][j] == '!': fill = [1, COLOR[5], (255, 204, 204)]
            else: fill = [1,  COLOR[int(show[i][j])], COLOR[0]]
            pydraw(rect, fill[2], COLOR[7], fill[0])
            if show[i][j] != ' ':
                surf = font.render(show[i][j], 1, fill[1])
                screen.blit(surf, surf.get_rect(center = rect.center))
        if mode[0] > 1 and now - timer > 3000: phase = 'ask'
    elif phase == 'ask': header('Play again? (Y/N)')
    pygame.display.flip()
font = pygame.font.Font(None, 15)
header('THANK YOU FOR PLAYING THIS GAME!')
pygame.time.wait(2000)
pygame.quit()
