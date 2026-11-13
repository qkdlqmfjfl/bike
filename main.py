"""NEON RIDER 실행 파일. 데스크톱과 브라우저(Pygbag)에서 사용합니다."""
import asyncio
import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from game import TrafficRiderGame


async def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = TrafficRiderGame()
    game.prepare_collisions()
    running = True

    while running:
        # 프레임 사이의 실제 경과 시간을 사용해 움직임을 일정하게 합니다.
        dt = min(clock.tick(FPS) / 1000.0, 0.04)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        keys = pygame.key.get_pressed()
        game.update(dt, keys)
        game.draw(screen, dt)
        pygame.display.flip()
        # Pygbag 브라우저 런타임에 제어권을 넘깁니다.
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
