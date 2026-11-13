"""플레이어 오토바이와 도로 위 차량을 그리는 코드입니다."""
import random
import pygame
from settings import *


class Motorcycle:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT - 112
        self.width = 46
        self.height = 82
        self.speed = 0

    def update(self, keys, dt):
        # 키를 누르는 동안 좌우로 이동합니다.
        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(
            keys[pygame.K_LEFT] or keys[pygame.K_a]
        )
        self.x += direction * 390 * dt
        self.x = max(ROAD_LEFT + 42, min(ROAD_RIGHT - 42, self.x))

    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        # 바퀴, 차체, 핸들, 헤드라이트를 간단한 도형으로 표현합니다.
        pygame.draw.ellipse(surface, (8, 10, 16), (x - 13, y + 30, 26, 48))
        pygame.draw.ellipse(surface, (8, 10, 16), (x - 12, y - 37, 24, 40))
        pygame.draw.polygon(surface, CYAN, [(x, y - 31), (x + 19, y + 5), (x + 12, y + 38), (x - 12, y + 38), (x - 19, y + 5)])
        pygame.draw.polygon(surface, PINK, [(x, y - 25), (x + 8, y + 7), (x, y + 25), (x - 8, y + 7)])
        pygame.draw.line(surface, WHITE, (x - 25, y - 12), (x + 25, y - 12), 5)
        pygame.draw.circle(surface, YELLOW, (x, y - 27), 6)


class TrafficCar:
    COLORS = [(245, 95, 90), (245, 185, 70), (105, 155, 245), (180, 115, 225), (230, 235, 240)]

    def __init__(self, lane, depth=0.0):
        self.lane = lane
        self.depth = depth
        self.color = random.choice(self.COLORS)

    def update(self, speed, dt):
        self.depth += speed * dt * 0.00042

    def draw(self, surface):
        # depth가 0이면 지평선 근처, 1이면 화면 아래쪽입니다.
        t = max(0.0, min(1.0, self.depth))
        road_half = 34 + t * 390
        center = WIDTH / 2
        lane_x = center + (self.lane - 1) * road_half * 0.57
        scale = 0.22 + t * 0.92
        w, h = int(34 * scale), int(58 * scale)
        y = int(HORIZON + t * (HEIGHT - HORIZON - 55))
        rect = pygame.Rect(int(lane_x - w / 2), y - h / 2, w, h)
        pygame.draw.rect(surface, (10, 12, 18), rect.inflate(5, 5), border_radius=max(2, int(6 * scale)))
        pygame.draw.rect(surface, self.color, rect, border_radius=max(2, int(6 * scale)))
        pygame.draw.rect(surface, (35, 48, 65), (rect.x + 4, rect.y + 7, max(2, w - 8), max(3, int(h * .25))), border_radius=3)
        pygame.draw.rect(surface, (255, 235, 190), (rect.x + 3, rect.bottom - 8, max(2, int(w * .22)), 4))
        pygame.draw.rect(surface, (255, 235, 190), (rect.right - max(2, int(w * .22)) - 3, rect.bottom - 8, max(2, int(w * .22)), 4))
        return rect


# 도로 가장자리의 기준 좌표. 원근감이 느껴지도록 지평선에서 좁고 아래에서 넓어집니다.
ROAD_LEFT = 480 - 390
ROAD_RIGHT = 480 + 390
