"""플레이어 오토바이와 교통 차량의 움직임 및 그림을 담당합니다."""
import math
import random
import pygame
from settings import *


def rounded(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=max(1, int(radius)))


class Motorcycle:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT - 112
        self.width = 50
        self.height = 88
        self.direction = 0
        self.wheel_spin = 0.0

    def update(self, keys, dt):
        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(
            keys[pygame.K_LEFT] or keys[pygame.K_a]
        )
        self.direction += (direction-self.direction)*min(1.0, dt*10)
        self.x += direction*430*dt
        self.x = max(ROAD_LEFT+43, min(ROAD_RIGHT-43, self.x))
        self.wheel_spin = (self.wheel_spin + dt*18) % math.tau

    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        # 바닥 그림자와 뒷바퀴
        pygame.draw.ellipse(surface, (5, 7, 13), (x-27, y+8, 54, 83))
        rounded(surface, (7, 9, 15), (x-12, y+21, 24, 57), 11)
        pygame.draw.line(surface, (105, 119, 139), (x, y+27), (x, y+70), 3)
        # 타이어 홈
        for offset in (-1, 1):
            yy = y+34+int((self.wheel_spin*5) % 20)
            pygame.draw.line(surface, (65, 75, 89), (x-9, yy+offset*3), (x+9, yy+offset*3), 1)

        # 배기구와 프레임
        pygame.draw.line(surface, (125, 143, 162), (x-13, y+37), (x+13, y+37), 4)
        pygame.draw.line(surface, (80, 96, 116), (x-14, y+51), (x+14, y+51), 3)

        # 차체 외곽과 연료 탱크
        lean = int(self.direction*5)
        pygame.draw.polygon(surface, (8, 17, 29), [
            (x-18+lean, y+24), (x-15+lean, y-21), (x, y-39),
            (x+15+lean, y-21), (x+19+lean, y+24), (x+10, y+43), (x-10, y+43)
        ])
        pygame.draw.polygon(surface, (12, 145, 174), [
            (x+lean, y-39), (x+18+lean, y-13), (x+13+lean, y+20),
            (x, y+34), (x-13+lean, y+20), (x-18+lean, y-13)
        ])
        pygame.draw.polygon(surface, (48, 225, 235), [
            (x+lean, y-34), (x+10+lean, y-11), (x+7, y+12),
            (x, y+21), (x-7, y+12), (x-10+lean, y-11)
        ])
        pygame.draw.polygon(surface, (238, 50, 125), [
            (x+lean, y-22), (x+7+lean, y-2), (x, y+17), (x-7+lean, y-2)
        ])
        # 운전자 헬멧
        pygame.draw.ellipse(surface, (17, 24, 39), (x-12+lean, y-51, 24, 25))
        pygame.draw.arc(surface, (85, 225, 245), (x-10+lean, y-49, 20, 21), 0.2, 2.8, 3)
        pygame.draw.line(surface, (155, 235, 245), (x-7+lean, y-31), (x+7+lean, y-31), 2)

        # 핸들, 거울, 헤드라이트
        pygame.draw.line(surface, (170, 190, 210), (x-26+lean, y-24), (x+26+lean, y-24), 5)
        pygame.draw.line(surface, (75, 92, 112), (x-20+lean, y-26), (x-27+lean, y-36), 3)
        pygame.draw.line(surface, (75, 92, 112), (x+20+lean, y-26), (x+27+lean, y-36), 3)
        pygame.draw.ellipse(surface, (255, 242, 170), (x-7+lean, y-29, 14, 9))
        pygame.draw.line(surface, (255, 75, 105), (x-8, y+37), (x+8, y+37), 3)


class TrafficCar:
    COLORS = [
        (220, 65, 75), (235, 150, 45), (55, 125, 220),
        (135, 85, 190), (205, 215, 225), (35, 165, 145),
        (225, 205, 150), (55, 65, 82)
    ]

    def __init__(self, lane, depth=0.0):
        self.lane = lane
        self.depth = depth
        self.color = random.choice(self.COLORS)
        self.variant = random.choice(("sedan", "sport", "van"))
        self.near_miss = False

    def update(self, speed, dt):
        # 화면 아래쪽으로 다가오는 속도. 고속 주행일수록 빠르게 접근합니다.
        self.depth += speed*dt*0.0026

    def get_rect(self):
        t = max(0.0, min(1.15, self.depth))
        road_half = 34+t*390
        lane_x = WIDTH/2+(self.lane-1)*road_half*0.57
        scale = 0.22+t*0.92
        width_factor = 1.22 if self.variant == "van" else (0.88 if self.variant == "sport" else 1.0)
        height_factor = 1.08 if self.variant == "van" else 1.0
        w = max(8, int(38*scale*width_factor))
        h = max(12, int(62*scale*height_factor))
        y = int(HORIZON+t*(HEIGHT-HORIZON-55))
        return pygame.Rect(int(lane_x-w/2), y-h//2, w, h)

    def draw(self, surface):
        rect = self.get_rect()
        t = max(0.0, min(1.0, self.depth))
        scale = 0.22+t*0.92
        radius = max(2, int(7*scale))
        # 그림자와 타이어
        shadow = rect.inflate(max(4, int(10*scale)), max(4, int(9*scale)))
        rounded(surface, (5, 7, 12), shadow, radius+2)
        tire_w = max(2, int(5*scale))
        rounded(surface, (8, 10, 15),
                (rect.left-tire_w//2, rect.top+rect.height//5, tire_w, rect.height*3//5), 2)
        rounded(surface, (8, 10, 15),
                (rect.right-tire_w//2, rect.top+rect.height//5, tire_w, rect.height*3//5), 2)

        # 차체 하이라이트와 입체적인 후면
        rounded(surface, (19, 24, 34), rect, radius+2)
        body = rect.inflate(-max(2, int(4*scale)), -max(2, int(4*scale)))
        rounded(surface, self.color, body, radius)
        pygame.draw.line(surface, tuple(min(255, c+55) for c in self.color),
                         (body.left+3, body.top+3), (body.right-3, body.top+3),
                         max(1, int(2*scale)))

        # 후면 유리와 트렁크
        glass_top = body.top+max(2, int(7*scale))
        glass_bottom = body.top+max(5, int(23*scale))
        inset = max(3, int(9*scale))
        pygame.draw.polygon(surface, (17, 38, 58), [
            (body.left+inset//2, glass_bottom),
            (body.left+inset, glass_top),
            (body.right-inset, glass_top),
            (body.right-inset//2, glass_bottom)
        ])
        pygame.draw.line(surface, (105, 160, 185),
                         (body.left+5, glass_bottom), (body.right-5, glass_bottom),
                         max(1, int(1.5*scale)))
        # 후미등과 번호판
        light_w = max(2, int(6*scale))
        light_h = max(2, int(5*scale))
        light_y = body.bottom-max(4, int(9*scale))
        for lx in (body.left+2, body.right-light_w-2):
            rounded(surface, (255, 55, 65), (lx, light_y, light_w, light_h), 2)
            if scale > .55:
                pygame.draw.line(surface, (255, 125, 125), (lx, light_y), (lx+light_w, light_y), 1)
        plate_w = max(3, int(rect.width*.28))
        rounded(surface, (225, 225, 205),
                (rect.centerx-plate_w//2, body.bottom-max(3, int(6*scale)),
                 plate_w, max(2, int(3*scale))), 1)
        pygame.draw.line(surface, (95, 105, 120),
                         (rect.left+3, rect.bottom-2), (rect.right-3, rect.bottom-2),
                         max(1, int(2*scale)))
        return rect


# 도로 아래쪽에서 플레이어가 달릴 수 있는 범위
ROAD_LEFT = 480-390
ROAD_RIGHT = 480+390
