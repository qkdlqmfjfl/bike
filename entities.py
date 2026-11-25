"""플레이어 오토바이와 도로 위 차량을 그리는 코드입니다."""
import random
import pygame
from settings import *


def rounded(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=max(1, radius))


class Motorcycle:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT - 112
        self.width = 46
        self.height = 82
        self.speed = 0

    def update(self, keys, dt):
        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(
            keys[pygame.K_LEFT] or keys[pygame.K_a]
        )
        self.x += direction * 390 * dt
        self.x = max(ROAD_LEFT + 42, min(ROAD_RIGHT - 42, self.x))

    def draw(self, surface):
        x, y = int(self.x), int(self.y)

        # 바닥 그림자와 두꺼운 타이어
        pygame.draw.ellipse(surface, (5, 8, 13), (x - 24, y - 4, 48, 88))
        rounded(surface, (7, 9, 15), (x - 13, y + 20, 26, 55), 12)
        rounded(surface, (48, 57, 70), (x - 8, y + 25, 16, 43), 7)
        pygame.draw.line(surface, (145, 158, 175), (x, y + 27), (x, y + 66), 2)

        # 리어 펜더, 차체, 연료 탱크
        pygame.draw.polygon(surface, (12, 22, 34), [
            (x - 17, y + 20), (x - 13, y - 22), (x, y - 34),
            (x + 13, y - 22), (x + 17, y + 20), (x + 10, y + 39),
            (x - 10, y + 39)
        ])
        pygame.draw.polygon(surface, (20, 185, 205), [
            (x, y - 34), (x + 17, y - 12), (x + 12, y + 23),
            (x, y + 34), (x - 12, y + 23), (x - 17, y - 12)
        ])
        pygame.draw.polygon(surface, (65, 245, 245), [
            (x, y - 31), (x + 10, y - 10), (x + 5, y + 12),
            (x, y + 20), (x - 5, y + 12), (x - 10, y - 10)
        ])
        pygame.draw.polygon(surface, (245, 55, 125), [
            (x, y - 20), (x + 6, y - 2), (x, y + 17), (x - 6, y - 2)
        ])

        # 핸들, 사이드 미러, 계기판과 헤드라이트
        pygame.draw.line(surface, (190, 205, 220), (x - 25, y - 25), (x + 25, y - 25), 5)
        pygame.draw.line(surface, (75, 90, 110), (x - 20, y - 26), (x - 27, y - 35), 3)
        pygame.draw.line(surface, (75, 90, 110), (x + 20, y - 26), (x + 27, y - 35), 3)
        pygame.draw.ellipse(surface, (15, 25, 40), (x - 8, y - 34, 16, 10))
        pygame.draw.ellipse(surface, (255, 245, 185), (x - 6, y - 31, 12, 7))
        pygame.draw.line(surface, (235, 245, 255), (x - 9, y + 34), (x + 9, y + 34), 2)


class TrafficCar:
    COLORS = [
        (220, 65, 75), (235, 150, 45), (55, 125, 220),
        (135, 85, 190), (205, 215, 225), (35, 165, 145)
    ]

    def __init__(self, lane, depth=0.0):
        self.lane = lane
        self.depth = depth
        self.color = random.choice(self.COLORS)

    def update(self, speed, dt):
        # 이전보다 약 4.3배 빠르게 다가오도록 조정했습니다.
        self.depth += speed * dt * 0.0018

    def draw(self, surface):
        # depth가 0이면 지평선 근처, 1이면 화면 아래쪽입니다.
        t = max(0.0, min(1.0, self.depth))
        road_half = 34 + t * 390
        lane_x = WIDTH / 2 + (self.lane - 1) * road_half * 0.57
        scale = 0.22 + t * 0.92
        w, h = max(8, int(38 * scale)), max(12, int(62 * scale))
        y = int(HORIZON + t * (HEIGHT - HORIZON - 55))
        rect = pygame.Rect(int(lane_x - w / 2), y - h / 2, w, h)
        radius = max(2, int(7 * scale))

        # 차체 그림자와 외곽 프레임
        shadow = rect.inflate(max(4, int(10 * scale)), max(4, int(9 * scale)))
        rounded(surface, (5, 8, 13), shadow, radius + 2)
        rounded(surface, (24, 29, 39), rect, radius)

        # 차체와 트렁크
        body = rect.inflate(-max(2, int(4 * scale)), -max(2, int(4 * scale)))
        rounded(surface, self.color, body, radius)
        pygame.draw.line(surface, (255, 255, 255), (body.left + 3, body.top + 3),
                         (body.right - 3, body.top + 3), max(1, int(1.5 * scale)))

        # 뒷유리창을 사다리꼴로 표현
        glass_top = body.top + max(2, int(7 * scale))
        glass_bottom = body.top + max(5, int(22 * scale))
        pygame.draw.polygon(surface, (22, 42, 62), [
            (body.left + max(2, int(5 * scale)), glass_bottom),
            (body.left + max(3, int(9 * scale)), glass_top),
            (body.right - max(3, int(9 * scale)), glass_top),
            (body.right - max(2, int(5 * scale)), glass_bottom)
        ])
        pygame.draw.line(surface, (105, 145, 170),
                         (body.left + 5, glass_bottom), (body.right - 5, glass_bottom),
                         max(1, int(1.5 * scale)))

        # 범퍼, 후미등, 번호판
        light_w = max(2, int(6 * scale))
        light_h = max(2, int(5 * scale))
        light_y = body.bottom - max(4, int(9 * scale))
        rounded(surface, (255, 55, 65),
                (body.left + 2, light_y, light_w, light_h), 2)
        rounded(surface, (255, 55, 65),
                (body.right - light_w - 2, light_y, light_w, light_h), 2)
        plate_w = max(3, int(w * 0.28))
        rounded(surface, (225, 225, 205),
                (int(lane_x - plate_w / 2), body.bottom - max(3, int(6 * scale)),
                 plate_w, max(2, int(3 * scale))), 1)
        pygame.draw.line(surface, (95, 105, 120),
                         (rect.left + 3, rect.bottom - 2),
                         (rect.right - 3, rect.bottom - 2), max(1, int(2 * scale)))
        return rect


# 도로 가장자리의 기준 좌표
ROAD_LEFT = 480 - 390
ROAD_RIGHT = 480 + 390
