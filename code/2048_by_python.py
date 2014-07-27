# 2048_by_python.py
# self.author = "xiaxin"

import pygame
import random
from copy import deepcopy
from pygame.locals import *
from sys import exit

pygame.init()
mat = [([0] * 4)for i in range(4)]
color_dic = {
    0: (204, 192, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (236, 141, 84),
    32: (246, 124, 95),
    64: (234, 89, 55),
    128: (128, 106, 0),
    256: (241, 208, 75),
    512: (228, 192, 42),
    1024: (238, 118, 0),
    2048: (213, 165, 0)
}

score = 0
side = 80
gap = 2
screen_gap = 20
screen_right = 200
s_width = side * 4 + gap * 5 + screen_right + screen_gap
s_height = side * 4 + gap * 5 + screen_gap * 2

screen = pygame.display.set_mode((s_width, s_height), 0, 32)
pygame.display.set_caption("2048 By Python")


class Grid:

    """docstring for grid"""

    def __init__(self, num, color, left, top):
        self.num = num
        self.color = color
        self.left = left
        self.top = top

    def draw_grid(self, surface):
        pygame.draw.rect(
            surface, self.color, (self.left, self.top, side, side))
        f_size = int(side * 0.35)
        font_num = pygame.font.Font("wqmyh.ttf", f_size)
        num_surf = font_num.render(self.num, True, (88, 88, 88))
        num_rect = num_surf.get_rect()
        num_rect.center = (self.left + side / 2, self.top + side / 2)
        screen.blit(num_surf, num_rect)


def draw():
    global mat
    left = screen_gap + gap
    top = screen_gap + gap
    for i in xrange(4):
        for j in xrange(4):
            t = mat[i][j]
            if t == 0:
                num = ""
            else:
                num = str(t)
            color = color_dic[t]
            grid = Grid(num, color, left, top)
            grid.draw_grid(screen)
            top += gap + side
        left += gap + side
        top = screen_gap + gap


def draw_menu():
    font_menu = pygame.font.Font("wqmyh.ttf", 40)
    menu1_surf = font_menu.render("BEST", True, (88, 88, 88))
    menu1_rect = menu1_surf.get_rect()
    menu1_rect.center = (s_width - screen_right / 2, screen_gap + side / 2)
    screen.blit(menu1_surf, menu1_rect)
    menu2_surf = font_menu.render("SCORE", True, (88, 88, 88))
    menu2_rect = menu2_surf.get_rect()
    menu2_rect.center = (
        s_width - screen_right / 2, screen_gap + side * 2 + side / 2)
    screen.blit(menu2_surf, menu2_rect)


def draw_score():
    score_screen = screen.subsurface(
        (s_width - screen_right, screen_gap + side * 3), (screen_right, side + screen_gap))
    score_screen.fill((171, 171, 171))
    font_score = pygame.font.Font("wqmyh.ttf", 35)
    score_surf = font_score.render(str(score), True, (88, 88, 88))
    score_rect = score_surf.get_rect()
    score_rect.center = (
        screen_right / 2, (s_height - screen_gap - side * 3.5) / 2)
    score_screen.blit(score_surf, score_rect)


def draw_over():
    font_over = pygame.font.Font("wqmyh.ttf", 80)
    over_surf = font_over.render("GAME OVER", True, (88, 88, 88))
    over_rect = over_surf.get_rect()
    over_rect.center = (s_width / 2, s_height / 2)
    screen.blit(over_surf, over_rect)


def read_best():
    try:
        b = open('best.txt', 'r')
        best = int(b.read())
    except:
        best = 0
    finally:
        b.close()
        return best


def write_best(best):
    try:
        b = open('best.txt', 'w')
        b.write(str(best))
    except IOError:
        pass
    finally:
        b.close()


def draw_best():
    best_screen = screen.subsurface(
        (s_width - screen_right, screen_gap + side), (screen_right, side + screen_gap))
    best_screen.fill((171, 171, 171))
    best = read_best()
    font_best = pygame.font.Font("wqmyh.ttf", 35)
    best_surf = font_best.render(str(best), True, (88, 88, 88))
    best_rect = best_surf.get_rect()
    best_rect.center = (
        screen_right / 2, (s_height - screen_gap - side * 3.5) / 2)
    best_screen.blit(best_surf, best_rect)


def set_rand():
    pool = []
    for i in xrange(4):
        for j in xrange(4):
            if mat[i][j] == 0:
                pool.append((i, j))
    p = random.choice(pool)
    v = random.uniform(0, 1)
    if v > 0.1:
        num = 2
    else:
        num = 4
    mat[p[0]][p[1]] = num
    pool.remove(p)


def check_mat():
    for i in xrange(4):
        for j in xrange(4):
            if mat[i][j] == 0:
                return False
    return True


def swap(T):
    global score
    global mat
    m = [0] * 4
    n = []
    for i in T:
        if i != 0:
            n.append(i)
    l = len(n)
    if l == 4:
        if n[0] == n[1]:
            m[0] = n[0] * 2
            score += m[0]
            if n[2] == n[3]:
                m[1] = n[2] * 2
                score += m[1]
            else:
                m[1] = n[2]
                m[2] = n[3]
        elif n[1] == n[2]:
            m[0] = n[0]
            m[1] = n[1] * 2
            score += m[1]
            m[2] = n[3]
        elif n[2] == n[3]:
            m[0] = n[0]
            m[1] = n[1]
            m[2] = n[2] * 2
            score += n[2]
        else:
            for i in xrange(l):
                m[i] = n[i]
    elif l == 3:
        if n[0] == n[1]:
            m[0] = n[0] * 2
            score += m[0]
            m[1] = n[2]
        elif n[1] == n[2]:
            m[0] = n[0]
            m[1] = n[1] * 2
            score += m[1]
        else:
            for i in xrange(l):
                m[i] = n[i]
    elif l == 2:
        if n[0] == n[1]:
            m[0] = n[0] * 2
            score += m[0]
        else:
            for i in xrange(l):
                m[i] = n[i]
    elif l == 1:
        m[0] = n[0]
    else:
        pass
    return m


def swap_down():
    for i in xrange(4):
        m = swap(mat[i][::-1])
        for j in xrange(4):
            mat[i][3 - j] = m[j]


def swap_up():
    for i in xrange(4):
        m = swap(mat[i])
        for j in xrange(4):
            mat[i][j] = m[j]


def swap_right():
    for i in xrange(4):
        t = []
        for j in xrange(4):
            t.append(mat[3 - j][i])
        m = swap(t)
        for k in xrange(4):
            mat[3 - k][i] = m[k]


def swap_left():
    for i in xrange(4):
        t = []
        for j in xrange(4):
            t.append(mat[j][i])
        m = swap(t)
        for k in xrange(4):
            mat[k][i] = m[k]


def main():
    screen.fill((171, 171, 171))
    tempmat = deepcopy(mat)
    over = check_mat()
    for i in xrange(2):
        set_rand()

    draw_menu()
    draw_score()
    draw_best()
    draw()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            elif not over:
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        swap_up()
                    elif event.key == K_DOWN:
                        swap_down()
                    elif event.key == K_LEFT:
                        swap_left()
                    elif event.key == K_RIGHT:
                        swap_right()
                    if tempmat != mat:
                        set_rand()
                        tempmat = deepcopy(mat)
                        draw()
                        draw_score()
                    best = read_best()
                    if best < score:
                        best = score
                        write_best(best)
                        draw_best()
            else:
                draw_over()

        pygame.display.update()

if __name__ == "__main__":
    main()
