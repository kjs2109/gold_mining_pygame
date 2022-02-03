# 집게 발사
# 현재 위치로부터 집게를 발사하는 동작
# 화면 밖으로 나가면 집게는 다시 원위치
# 뻗을 때 속도, 돌아올 때 속도
from lib2to3.pgen2.token import RIGHTSHIFTEQUAL
import pygame
import os

# 집게 클래스
class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image # 계속 업데이트 되는 이미지, 집게는 계속 움직인다.
        self.rect = self.image.get_rect(center=position) # 이미지가 변함에 따라 rotate 함수에서 계속 업데이트 됨
        self.position = position
        self.offset = pygame.math.Vector2(default_offset_x_claw)

        self.angle = 10 # 초기 각도,  현재각도로 계속 업데이드
        self.direction = LEFT
        self.angle_speed = 2.5 # 집게의 각도 변경 폭(좌우 이동 속도)

        self.original_image = self.image # rotate 할 때, 새로운 이미지가 계속 새성되는 것이므로 원본 이미지가 필요하다. 

    def update(self, to_x): # game 루프가 돌때마다 실행되는 함수
        # angle은 계속 업데이트 된다.
        if self.direction == LEFT:
            self.angle += self.angle_speed
        elif self.direction == RIGHT:
            self.angle -= self.angle_speed

        if self.angle < 10:
            self.angle = 10
            self.set_direction(LEFT)
        elif self.angle > 170:
            self.angle = 170
            self.set_direction(RIGHT)
        
        self.offset.x += to_x

        self.rotate() # ***

    # claw 이미지가 회전하고 회전하는 offset을 적용시킨 좌표를 구해줌
    def rotate(self):
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1)

        offset_rotated = self.offset.rotate(self.angle) # 변화하하는 각도에 따라 자동으로 변화하는 (x, y) 좌표를 구해준다. Vector2에서 제공하는 함수
        
        self.rect = self.image.get_rect(center=self.position + offset_rotated) # 변화하는 claw 이미지에 따라 image의 center를 position에 고정시킨다.
        pygame.draw.rect(screen, RED, self.rect, 1)           # > 이미지가 제자리에서 회전할 수 있다.

    def set_direction(self, direction):
        self.direction = direction

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position, 3) # 중심점 표시
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5) # ***

# 보석 클래스
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

# 게임 관련 변수
to_x = 0 # x좌표 기준으로 집게 이미지를 이동시킬 값 저장 변수
move_speed = 12 #발사할 때 이동 스피드, 상황에 따라서 스피드에 변화를 주어야 하기 때문에 변수에 지정

# 방향 변수
default_offset_x_claw = (40, 0)
LEFT = -1 # 왼쪽 방향
RIGHT = 1 # 오른쪽 방향
STOP = 0

# 색 변수
RED = (255, 0, 0)
BLACK = (0, 0, 0)

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

# 집게 객체
claw_image = pygame.image.load(os.path.join(images_path, 'claw.png'))
claw = Claw(claw_image, (screen_width // 2, 110))

running = True
while running:
    clock.tick(30)  # FPS 값 30으로 고정
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN: # 마우스 버튼 누를 때 집게를 뻗음
            claw.set_direction(STOP) 
            to_x = move_speed

    screen.blit(background_image, (0, 0))
    gemstone_group.draw(screen) # 그룹내 모든 sprite를 screen에 그림
    claw.update(to_x)
    claw.draw(screen)

    pygame.display.update()

pygame.quit()
