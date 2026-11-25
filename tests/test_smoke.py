"""GitHub Actions에서 실행하는 기본 게임 스모크 테스트."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import unittest

from game import TrafficRiderGame
from entities import TrafficCar


class GameSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((960, 600))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_game_can_create_and_draw_start_screen(self):
        game = TrafficRiderGame()
        game.prepare_collisions()
        surface = pygame.Surface((960, 600))
        game.draw(surface, 1 / 60)
        self.assertEqual(game.state, game.START)

    def test_enter_starts_game_and_distance_increases(self):
        game = TrafficRiderGame()
        game.prepare_collisions()
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        game.handle_event(event)
        self.assertEqual(game.state, game.PLAYING)
        game.update(0.1, pygame.key.get_pressed())
        self.assertGreater(game.distance, 0)

    def test_traffic_car_moves_toward_player(self):
        car = TrafficCar(1)
        before = car.depth
        car.update(180, 0.1)
        self.assertGreater(car.depth, before)
        self.assertGreater(car.get_rect().width, 0)

    def test_pause_and_resume(self):
        game = TrafficRiderGame()
        game.state = game.PLAYING
        game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
        self.assertEqual(game.state, game.PAUSED)
        game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
        self.assertEqual(game.state, game.PLAYING)


if __name__ == "__main__":
    unittest.main()
