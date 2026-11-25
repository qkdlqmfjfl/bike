"""NEON RIDER의 게임 진행, 도로, HUD, 충돌과 화면을 담당합니다."""
import math
import random
import pygame
from settings import *
from entities import Motorcycle, TrafficCar


class TrafficRiderGame:
    START, PLAYING, PAUSED, GAME_OVER = "start", "playing", "paused", "game_over"

    def __init__(self):
        self.font = pygame.font.Font(None, 30)
        self.small_font = pygame.font.Font(None, 22)
        self.big_font = pygame.font.Font(None, 82)
        self.title_font = pygame.font.Font(None, 100)
        self.reset()
        self.state = self.START

    def reset(self):
        self.player = Motorcycle()
        self.cars = []
        self.particles = []
        self.distance = 0.0
        self.score = 0
        self.speed = 145.0
        self.base_speed = 145.0
        self.spawn_timer = 0.55
        self.road_offset = 0.0
        self.nitro = 100.0
        self.nitro_active = False
        self.near_miss_flash = 0.0
        self.last_near_miss = 0
        self.shake = 0.0
        self.elapsed = 0.0

    def text(self, surface, message, font, color, center, shadow=True):
        image = font.render(str(message), True, color)
        rect = image.get_rect(center=(int(center[0]), int(center[1])))
        if shadow:
            shade = font.render(str(message), True, (5, 8, 15))
            surface.blit(shade, rect.move(2, 3))
        surface.blit(image, rect)

    def panel(self, surface, rect, color=(5, 10, 22, 205), border=(65, 95, 125)):
        layer = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(layer, color, layer.get_rect(), border_radius=12)
        pygame.draw.rect(layer, (*border, 210), layer.get_rect(), 1, border_radius=12)
        surface.blit(layer, rect.topleft)

    def draw_road(self, surface, dt):
        # 하늘 그라데이션
        for i in range(20):
            t = i / 19
            color = (int(7 + 23*t), int(12 + 17*t), int(29 + 30*t))
            y = int(i * HORIZON / 20)
            pygame.draw.rect(surface, color, (0, y, WIDTH, HORIZON // 20 + 2))

        # 먼 도시와 노을빛
        pygame.draw.circle(surface, (91, 48, 83), (WIDTH//2, HORIZON-17), 61)
        pygame.draw.circle(surface, (224, 117, 105), (WIDTH//2, HORIZON-17), 34)
        pygame.draw.circle(surface, (255, 185, 125), (WIDTH//2, HORIZON-17), 19)
        pygame.draw.polygon(surface, (15, 27, 43), [
            (0, HORIZON), (65, 130), (120, HORIZON), (215, 112),
            (315, HORIZON), (430, 137), (545, HORIZON), (680, 119),
            (790, HORIZON), (870, 143), (WIDTH, HORIZON)
        ])
        for i in range(24):
            x = i * 43
            h = 10 + (i * 17) % 34
            pygame.draw.rect(surface, (19, 30, 48), (x, HORIZON-h, 27, h))
            if i % 3 == 0:
                pygame.draw.rect(surface, (245, 170, 105), (x+7, HORIZON-h+5, 3, 3))

        surface.fill((19, 62, 51), (0, HORIZON, WIDTH, HEIGHT-HORIZON))
        # 도로 바깥 어깨와 아스팔트
        pygame.draw.polygon(surface, (105, 102, 94), [
            (WIDTH//2-40, HORIZON), (WIDTH//2+40, HORIZON),
            (WIDTH//2+455, HEIGHT), (WIDTH//2-455, HEIGHT)
        ])
        pygame.draw.polygon(surface, (38, 43, 54), [
            (WIDTH//2-34, HORIZON), (WIDTH//2+34, HORIZON),
            (WIDTH//2+430, HEIGHT), (WIDTH//2-430, HEIGHT)
        ])

        # 도로 가장자리의 붉은/흰 반사 구간
        for side in (-1, 1):
            pygame.draw.line(surface, (238, 224, 190),
                             (WIDTH//2+side*34, HORIZON),
                             (WIDTH//2+side*430, HEIGHT), 4)
            for i in range(10):
                t = ((i/10) + self.road_offset/10) % 1.0
                y = int(HORIZON + t*(HEIGHT-HORIZON))
                half = 34 + t*396
                x = int(WIDTH/2 + side*(half+13))
                size = max(2, int(3+t*7))
                color = (245, 75, 90) if i % 2 else (245, 235, 205)
                pygame.draw.rect(surface, color, (x-size, y, size*2, max(3, size*2)))

        # 차선 점선과 노면 반사
        self.road_offset = (self.road_offset + self.speed*dt*0.0017) % 1.0
        for lane in (-1, 1):
            for i in range(14):
                t = ((i/14) + self.road_offset) % 1.0
                y = int(HORIZON + t*(HEIGHT-HORIZON))
                half = 34 + t*396
                x = int(WIDTH/2 + lane*half/3)
                dash_h = max(4, int(5+t*34))
                dash_w = max(2, int(2+t*6))
                pygame.draw.rect(surface, (235, 224, 180),
                                 (x-dash_w//2, y, dash_w, dash_h))
        # 노면의 속도감 있는 짧은 반사선
        for i in range(18):
            t = ((i/18) + self.road_offset*1.7) % 1.0
            y = int(HORIZON + t*(HEIGHT-HORIZON))
            half = 34 + t*396
            x = int(WIDTH/2 + ((i*7)%9-4)*half/10)
            pygame.draw.line(surface, (58, 66, 78), (x, y), (x+int(5+t*16), y),
                             max(1, int(t*2)))

        # 길가의 네온 가로등
        for side in (-1, 1):
            for i in range(6):
                t = ((i/6) + self.road_offset*0.72) % 1.0
                y = int(HORIZON + t*330)
                x = int(WIDTH/2 + side*(45+t*475))
                h = max(5, int(8+t*47))
                pygame.draw.line(surface, (80, 105, 130), (x, y), (x, y-h), max(1, int(1+t*3)))
                pygame.draw.circle(surface, (75, 220, 255), (x, y-h), max(2, int(2+t*4)))

    def draw_hud(self, surface):
        self.panel(surface, pygame.Rect(14, 12, WIDTH-28, 62))
        self.text(surface, f"SCORE  {self.score:06d}", self.font, WHITE, (120, 42))
        self.text(surface, f"DIST  {int(self.distance):,} m", self.font, CYAN, (WIDTH//2, 42))
        self.text(surface, f"{int(self.speed)} km/h", self.font, YELLOW, (WIDTH-115, 42))
        # 니트로 게이지
        self.text(surface, "N2O", self.small_font, (125, 220, 255), (55, 91))
        pygame.draw.rect(surface, (20, 29, 43), (83, 84, 150, 9), border_radius=5)
        pygame.draw.rect(surface, (55, 205, 255), (83, 84, int(150*self.nitro/100), 9), border_radius=5)

    def add_particles(self, x, y, color, count=12):
        for _ in range(count):
            angle = random.random()*math.tau
            force = random.uniform(35, 190)
            self.particles.append({
                "x": float(x), "y": float(y),
                "vx": math.cos(angle)*force, "vy": math.sin(angle)*force,
                "life": random.uniform(.25, .65), "max": .65,
                "color": color, "size": random.randint(2, 5)
            })

    def update_particles(self, dt):
        for p in self.particles[:]:
            p["life"] -= dt
            p["x"] += p["vx"]*dt
            p["y"] += p["vy"]*dt
            p["vy"] += 110*dt
            if p["life"] <= 0:
                self.particles.remove(p)

    def draw_particles(self, surface):
        for p in self.particles:
            radius = max(1, int(p["size"]*p["life"]/p["max"]))
            pygame.draw.circle(surface, p["color"], (int(p["x"]), int(p["y"])), radius)

    def update(self, dt, keys):
        self.update_particles(dt)
        if self.state != self.PLAYING:
            return

        self.elapsed += dt
        self.base_speed = min(255.0, 145.0 + self.elapsed*2.8)
        self.nitro_active = bool(keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and self.nitro > 0
        if self.nitro_active:
            self.nitro = max(0.0, self.nitro-34*dt)
            target_speed = min(330.0, self.base_speed*1.42)
        else:
            self.nitro = min(100.0, self.nitro+10*dt)
            target_speed = self.base_speed
        self.speed += (target_speed-self.speed)*min(1.0, dt*4.5)

        self.distance += self.speed*dt/3.6
        self.score = int(self.distance*2)
        self.player.update(keys, dt)
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            available = [lane for lane in range(3)
                         if not any(car.lane == lane and car.depth < .25 for car in self.cars)]
            if available:
                lane = random.choice(available)
                self.cars.append(TrafficCar(lane, 0.0))
            interval = max(.42, 1.02 - (self.speed-145)/420)
            self.spawn_timer = random.uniform(interval*.78, interval*1.18)

        player_box = pygame.Rect(int(self.player.x-17), int(self.player.y-31), 34, 64)
        for car in self.cars[:]:
            car.update(self.speed, dt)
            car_box = car.get_rect()
            if car.depth > 1.14:
                self.cars.remove(car)
                continue
            if car.depth > .69 and player_box.colliderect(car_box.inflate(-max(2, car_box.width//7),
                                                                          -max(2, car_box.height//8))):
                self.add_particles(self.player.x, self.player.y, (255, 105, 75), 28)
                self.shake = .35
                self.state = self.GAME_OVER
                break
            # 아주 가까이 지나간 차량에 근접 회피 보너스
            if .70 < car.depth < .76 and not car.near_miss and abs(car_box.centerx-player_box.centerx) < 68:
                car.near_miss = True
                self.score += 250
                self.near_miss_flash = .7
                self.add_particles(self.player.x, self.player.y-20, (80, 220, 255), 7)

        self.near_miss_flash = max(0.0, self.near_miss_flash-dt)
        self.shake = max(0.0, self.shake-dt)

    def draw_overlay(self, surface, alpha=165):
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((3, 7, 17, alpha))
        surface.blit(shade, (0, 0))

    def draw(self, surface, dt=0):
        self.draw_road(surface, dt if self.state == self.PLAYING else 0)
        if self.state == self.START:
            self.draw_overlay(surface, 90)
            self.text(surface, "NEON RIDER", self.title_font, CYAN, (WIDTH//2, 205))
            self.text(surface, "HIGH SPEED  /  NIGHT HIGHWAY", self.font, WHITE, (WIDTH//2, 270))
            self.panel(surface, pygame.Rect(WIDTH//2-205, 330, 410, 115))
            self.text(surface, "PRESS ENTER TO START", self.font, YELLOW, (WIDTH//2, 365))
            self.text(surface, "A / D  or  ARROW KEYS   :   STEER", self.small_font, WHITE, (WIDTH//2, 405))
            self.text(surface, "HOLD SHIFT   :   NITRO BOOST", self.small_font, (100, 220, 255), (WIDTH//2, 435))
            self.text(surface, "DODGE TRAFFIC  -  GET CLOSE  -  EARN BONUS", self.small_font, MUTED, (WIDTH//2, 505))
            return

        for car in sorted(self.cars, key=lambda c: c.depth):
            car.draw(surface)
        self.player.draw(surface)
        self.draw_particles(surface)

        if self.state in (self.PLAYING, self.PAUSED):
            self.draw_hud(surface)
            if self.near_miss_flash > 0:
                self.text(surface, "NEAR MISS  +250", self.font, CYAN, (WIDTH//2, 112))
            if self.state == self.PAUSED:
                self.draw_overlay(surface, 155)
                self.text(surface, "PAUSED", self.big_font, WHITE, (WIDTH//2, 250))
                self.text(surface, "PRESS P TO CONTINUE", self.font, YELLOW, (WIDTH//2, 320))
        else:
            self.draw_overlay(surface, 190)
            self.panel(surface, pygame.Rect(WIDTH//2-245, 165, 490, 290))
            self.text(surface, "RIDE OVER", self.big_font, (255, 85, 130), (WIDTH//2, 225))
            self.text(surface, f"SCORE  {self.score:06d}", self.font, WHITE, (WIDTH//2, 295))
            self.text(surface, f"DISTANCE  {int(self.distance):,} m", self.font, CYAN, (WIDTH//2, 337))
            self.text(surface, f"TOP SPEED  {int(self.speed)} km/h", self.font, YELLOW, (WIDTH//2, 378))
            self.text(surface, "PRESS R OR ENTER TO RIDE AGAIN", self.small_font, WHITE, (WIDTH//2, 420))

    def prepare_collisions(self):
        # 기존 main.py와의 호환성을 유지하는 메서드입니다.
        self._collision_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if self.state == self.START and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.reset()
            self.state = self.PLAYING
        elif self.state == self.PLAYING and event.key == pygame.K_p:
            self.state = self.PAUSED
        elif self.state == self.PAUSED and event.key in (pygame.K_p, pygame.K_ESCAPE):
            self.state = self.PLAYING
        elif self.state == self.GAME_OVER and event.key in (pygame.K_r, pygame.K_RETURN, pygame.K_SPACE):
            self.reset()
            self.state = self.PLAYING
