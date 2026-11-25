"""게임 화면, 원근 도로, 점수와 충돌 판정을 담당합니다."""
import random
import pygame
from settings import *
from entities import Motorcycle, TrafficCar


class TrafficRiderGame:
    START, PLAYING, GAME_OVER = "start", "playing", "game_over"

    def __init__(self):
        self.state = self.START
        self.font = pygame.font.Font(None, 34)
        self.big_font = pygame.font.Font(None, 76)
        self.small_font = pygame.font.Font(None, 24)
        self.reset()

    def reset(self):
        self.player = Motorcycle()
        self.cars = []
        self.distance = 0.0
        self.score = 0
        self.speed = 120
        self.spawn_timer = 0.0
        self.road_offset = 0.0

    def text(self, surface, message, font, color, center):
        image = font.render(message, True, color)
        surface.blit(image, image.get_rect(center=center))

    def draw_road(self, surface, dt):
        # 노을빛이 도는 네온 야간 도로 배경
        for i in range(18):
            t = i / 17
            color = (
                int(9 + 39 * t),
                int(16 + 20 * t),
                int(35 + 28 * t)
            )
            y = int(i * HORIZON / 18)
            pygame.draw.rect(surface, color, (0, y, WIDTH, HORIZON // 18 + 2))

        # 지평선의 빛나는 노을
        pygame.draw.circle(surface, (92, 62, 85), (WIDTH // 2, HORIZON - 20), 48)
        pygame.draw.circle(surface, (225, 135, 105), (WIDTH // 2, HORIZON - 20), 25)

        # 좌우 잔디와 원근감이 있는 도로 갓길
        surface.fill((20, 65, 52), (0, HORIZON, WIDTH, HEIGHT - HORIZON))
        pygame.draw.polygon(surface, (105, 105, 95), [
            (WIDTH/2-40, HORIZON), (WIDTH/2+40, HORIZON),
            (WIDTH/2+445, HEIGHT), (WIDTH/2-445, HEIGHT)
        ])
        pygame.draw.polygon(surface, (43, 47, 58), [
            (WIDTH/2-34, HORIZON), (WIDTH/2+34, HORIZON),
            (WIDTH/2+430, HEIGHT), (WIDTH/2-430, HEIGHT)
        ])

        # 도로 양쪽 경계선
        pygame.draw.line(surface, (245, 225, 185), (WIDTH/2-34, HORIZON), (WIDTH/2-430, HEIGHT), 4)
        pygame.draw.line(surface, (245, 225, 185), (WIDTH/2+34, HORIZON), (WIDTH/2+430, HEIGHT), 4)

        # 아스팔트의 은은한 질감
        for i in range(28):
            t = ((i / 28) + self.road_offset / 7) % 1.0
            y = int(HORIZON + t * (HEIGHT - HORIZON))
            half = 34 + t * 396
            x = int(WIDTH / 2 + ((i % 3) - 1) * half * 0.42)
            pygame.draw.circle(surface, (57, 62, 73), (x, y), max(1, int(1 + t * 2)))

        # 차선 점선: 멀리서는 짧고 가까이서는 길고 굵게 표시
        self.road_offset = (self.road_offset + self.speed * dt * 0.9) % 1.0
        for lane in (-1, 1):
            for i in range(12):
                t = ((i / 12) + self.road_offset / 12) % 1.0
                y = int(HORIZON + t * (HEIGHT - HORIZON))
                half = 34 + t * 396
                x = int(WIDTH/2 + lane * half / 3)
                dash_h = max(3, int(5 + t * 30))
                dash_w = max(2, int(2 + t * 5))
                pygame.draw.rect(surface, (235, 220, 165),
                                 (x-dash_w//2, y, dash_w, dash_h))

        # 멀리 보이는 산 실루엣
        pygame.draw.polygon(surface, (20, 31, 48), [
            (0,HORIZON),(90,125),(170,HORIZON),(280,112),
            (390,HORIZON),(520,135),(650,HORIZON),(790,120),
            (900,HORIZON),(WIDTH,HORIZON)
        ])

        # 도로 옆 반사 표지판이 뒤로 흘러가며 속도감을 줍니다.
        for side in (-1, 1):
            for i in range(7):
                t = ((i / 7) + self.road_offset / 7) % 1.0
                y = int(HORIZON + t * 350)
                x = int(WIDTH/2 + side * (42 + t * 445))
                size = max(2, int(3 + t * 5))
                pygame.draw.line(surface, (165, 185, 195),
                                 (x, y), (x, y-size*5), max(1, size//2))
                pygame.draw.circle(surface, (255, 205, 110), (x, y-size*5), size)

    def draw_hud(self, surface):
        panel = pygame.Surface((WIDTH, 68), pygame.SRCALPHA)
        panel.fill((5, 10, 20, 190))
        surface.blit(panel, (0, 0))
        self.text(surface, f"SCORE  {self.score}", self.font, WHITE, (120, 34))
        self.text(surface, f"DISTANCE  {int(self.distance)} m", self.font, CYAN, (WIDTH/2, 34))
        self.text(surface, f"SPEED  {int(self.speed)} km/h", self.font, YELLOW, (WIDTH-145, 34))

    def update(self, dt, keys):
        if self.state != self.PLAYING:
            return
        self.speed = min(280, self.speed + 8 * dt)
        self.distance += self.speed * dt / 3.6
        self.score = int(self.distance * 2)
        self.player.update(keys, dt)

        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            lane = random.randrange(3)
            # 너무 가까운 곳에 같은 차선 차량이 겹치지 않도록 생성합니다.
            if not any(car.lane == lane and car.depth < 0.22 for car in self.cars):
                self.cars.append(TrafficCar(lane, 0.0))
            self.spawn_timer = max(0.48, 1.15 - self.speed / 420)

        player_box = pygame.Rect(int(self.player.x-17), int(self.player.y-31), 34, 64)
        for car in self.cars[:]:
            car.update(self.speed, dt)
            car_box = car.draw(self._collision_surface)
            if car.depth > 1.12:
                self.cars.remove(car)
            elif car.depth > 0.72 and player_box.colliderect(car_box.inflate(-5, -5)):
                self.state = self.GAME_OVER

    def draw(self, surface, dt=0):
        self.draw_road(surface, dt)
        if self.state == self.START:
            self.text(surface, "NEON RIDER", self.big_font, CYAN, (WIDTH/2, 220))
            self.text(surface, "A PERSPECTIVE MOTORBIKE RUSH", self.font, WHITE, (WIDTH/2, 275))
            self.text(surface, "Press ENTER to start", self.font, YELLOW, (WIDTH/2, 370))
            self.text(surface, "Move: A / D or LEFT / RIGHT", self.small_font, MUTED, (WIDTH/2, 420))
            self.text(surface, "Avoid traffic and ride as far as you can!", self.small_font, MUTED, (WIDTH/2, 452))
        elif self.state == self.PLAYING:
            for car in sorted(self.cars, key=lambda c: c.depth):
                car.draw(surface)
            self.player.draw(surface)
            self.draw_hud(surface)
        else:
            for car in self.cars:
                car.draw(surface)
            self.player.draw(surface)
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((4, 7, 15, 185))
            surface.blit(shade, (0,0))
            self.text(surface, "GAME OVER", self.big_font, PINK, (WIDTH/2, 220))
            self.text(surface, f"SCORE  {self.score}     DISTANCE  {int(self.distance)} m", self.font, WHITE, (WIDTH/2, 300))
            self.text(surface, f"TOP SPEED  {int(self.speed)} km/h", self.font, YELLOW, (WIDTH/2, 345))
            self.text(surface, "Press R or ENTER to ride again", self.font, CYAN, (WIDTH/2, 420))

    def prepare_collisions(self):
        # 충돌 판정용 투명 surface는 실제 화면에 표시하지 않습니다.
        self._collision_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == self.START and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.reset()
                self.state = self.PLAYING
            elif self.state == self.GAME_OVER and event.key in (pygame.K_r, pygame.K_RETURN, pygame.K_SPACE):
                self.reset()
                self.state = self.PLAYING
