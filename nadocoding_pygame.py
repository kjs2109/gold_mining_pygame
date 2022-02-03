# 보석 그룹핑 하기 -> 파이썬에서 제공하는 sprite의 Group()을 사용하면 한번에 draw 해줄수 있다.
from email.mime import image
import pygame
import os

class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)

# gemstone_group에 Gemston() 객체를 만드는 함수
def setup_gemstone():
    # 작은 금
    small_gold = Gemstone(gemstone_images[0], (200, 380))
    gemstone_group.add(small_gold)
    # 큰 금
    gemstone_group.add(Gemstone(gemstone_images[1], (300, 500)))
    # 돌
    gemstone_group.add(Gemstone(gemstone_images[2], (300, 380)))
    # 다이아몬드
    gemstone_group.add(Gemstone(gemstone_images[3], (900, 420)))

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Gold Mining Game')

clock = pygame.time.Clock()

# 현재, 이미지 경로
# 이렇게 해주면 게임의 파일 위치가 바껴도 현재위치를 계속 불러올 수 있다.
current_path = os.path.dirname(__file__)
images_path = os.path.join(current_path, 'images')

# 배경 이미지
background_image = pygame.image.load(os.path.join(images_path, 'background.png'))

# 4개 보석 이미지 (작은 금, 큰 금, 돌, 다이아몬드)
gemstone_images = [
    pygame.image.load(os.path.join(images_path, 'small_gold.png')),
    pygame.image.load(os.path.join(images_path, 'big_gold.png')),
    pygame.image.load(os.path.join(images_path, 'stone.png')),
    pygame.image.load(os.path.join(images_path, 'diamond.png')),
]

# 보석 그룹 객체 만들기
gemstone_group = pygame.sprite.Group()

setup_gemstone()


running = True
while running:
    clock.tick(30)  # FPS 값 30으로 고정
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_image, (0, 0))
    gemstone_group.draw(screen) # 그룹내 모든 sprite를 screen에 그림

    pygame.display.update()

pygame.quit()
