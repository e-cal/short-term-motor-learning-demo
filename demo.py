import sys
import time
import matplotlib.pyplot as plt
import pygame
from pygame.locals import *  # type: ignore


WIDTH = 1900
HEIGHT = 1200

MID = (WIDTH // 2, HEIGHT // 2)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)

history = {
    "indv": [],
    "avg": [],
}

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont(None, 48)  # type: ignore


def terminate():
    plt.plot(history["indv"], "bo-")  # type: ignore
    plt.title("Trial Average Target Time")
    plt.xlabel("Trial")
    plt.ylabel("Target Time (s)")
    plt.savefig(f"final.png")
    plt.clf()

    plt.plot(range(10, len(history["avg"]) * 10 + 1, 10), history["avg"], "mo-")
    plt.title("Overall Average Target Time")
    plt.xlabel("Trial")
    plt.ylabel("Target Time (s)")
    plt.savefig(f"avg_final.png")

    pygame.quit()
    sys.exit()


def drawText(text, x, y, color=RED):
    textObject = FONT.render(text, 1, color)  # type: ignore
    textRect = textObject.get_rect()
    textRect.topleft = (x, y)
    window.blit(textObject, textRect)


def main():
    w, h = 240, 100
    start_button = pygame.Rect(MID[0] - (w // 2), MID[1] - (h // 2), w, h)

    iter = 1
    while True:
        window.fill(BLACK)
        pygame.draw.rect(
            window,
            RED,
            start_button,
        )

        drawText(f"Trial: {iter}", MID[0] - 50, MID[1] + h, RED)
        drawText("start", MID[0] - 40, MID[1] - 20, BLACK)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
            if event.type == MOUSEBUTTONDOWN:
                if start_button.collidepoint(pygame.mouse.get_pos()):
                    demo(iter)
                    iter += 1

        pygame.display.update()


def demo(iter):
    mouseX = MID[0]
    mouseY = MID[1]
    start = time.time()

    targets = [
        pygame.Rect(565, 160, 40, 40),
        pygame.Rect(305, 498, 40, 40),
        pygame.Rect(1464, 1055, 40, 40),
        pygame.Rect(112, 612, 40, 40),
        pygame.Rect(1267, 1025, 40, 40),
    ]
    target_times = []

    target_start = time.time()
    last_off = time.time()
    while targets:
        window.fill(BLACK)
        pygame.draw.circle(
            window, RED, (targets[0].right - 20, targets[0].bottom - 20), 20
        )

        time_on = time.time() - last_off

        if (
            mouseX > targets[0].topleft[0]
            and mouseX < targets[0].bottomright[0]
            and mouseY > targets[0].topleft[1]
            and mouseY < targets[0].bottomright[1]
        ):
            pass
        else:
            last_off = time.time()

        if time_on >= 0.2:
            targets.pop(0)
            target_times.append(time.time() - target_start)
            target_start = time.time()
            last_off = time.time()

        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

        pygame.display.update()

    total_time = time.time() - start
    avg = sum(target_times) / len(target_times)

    history["indv"].append(avg)

    drawText(
        f"total time: {total_time:.2f}s",
        MID[0] - 180,
        MID[1],
    )
    drawText(
        f"avg target time: {avg:.2f}s",
        MID[0] - 225,
        MID[1] + 50,
    )
    pygame.display.update()

    plt.plot(history["indv"], "bo")  # type: ignore
    plt.title("Trial Average Target Time")
    plt.xlabel("Trial")
    plt.ylabel("Target Time (s)")
    plt.savefig(f"trial{iter}.png")
    plt.clf()

    if iter % 10 == 0:
        history["avg"].append(sum(history["indv"]) / len(history["indv"]))
        plt.plot(range(10, len(history["avg"]) * 10 + 1, 10), history["avg"], "mo")
        plt.title("Overall Average Target Time")
        plt.xlabel("Trial")
        plt.ylabel("Target Time (s)")
        plt.savefig(f"avg_trial{iter}.png")
        plt.clf()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == MOUSEBUTTONDOWN:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()


main()
