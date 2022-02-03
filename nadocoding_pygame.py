# 충돌 처리 (mask) 이미지 편집, collide_mask()
import math
import pygame
import os

# 집게 클래스
class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image # 계속 업데이트 되는 이미지, 집게는 계속 움직인다.
        self.rect = self.image.get_rect(center=position) # 이미지가 변함에 따라 rotate 함수에서 계속 업데이트 됨
        self.position = position
        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)

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
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5) # ***

    def set_init_state(self): # 마우스를 클릭한 순간 claw의 swining이 멈췄다.다시 swing 시켜주기 위해서는 self.direction을 다시 설정해주어야 한다.
        self.offset.x = default_offset_x_claw
        self.direction = LEFT


# 보석 클래스
class Gemstone(pygame.sprite.Sprite):
    def __init__(self, image, position, price, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.price = price
        self.speed = speed

    def set_position(self, position, angle):
        r = self.rect.size[0] // 2
        rad_angle = math.radians(angle) # 숫자를 라디안 각도로 바꿔줌 
        to_x = r * math.cos(rad_angle)
        to_y = r * math.sin(rad_angle)

        self.rect.center = (position[0] + to_x, position[1] + to_y)


# gemstone_group에 Gemston() 객체를 만드는 함수
def setup_gemstone():
    small_gold_price, small_gold_speed = 100, 5
    big_gold_price, big_gold_speed = 300, 2
    stone_price, stone_speed = 10, 2
    diamond_price, diamond_speed = 600, 7

    # 작은 금
    small_gold = Gemstone(gemstone_images[0], (200, 380), small_gold_price, small_gold_speed)
    gemstone_group.add(small_gold)
    # 큰 금
    gemstone_group.add(Gemstone(gemstone_images[1], (300, 500), big_gold_price, big_gold_speed))
    # 돌
    gemstone_group.add(Gemstone(gemstone_images[2], (300, 380), stone_price, stone_speed))
    # 다이아몬드
    gemstone_group.add(Gemstone(gemstone_images[3], (900, 420), diamond_price, diamond_speed))

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Gold Mining Game')

clock = pygame.time.Clock()

# 게임 관련 변수
to_x = 0 # x좌표 기준으로 집게 이미지를 이동시킬 값 저장 변수
default_offset_x_claw = 40
caught_gemstone = None # 잡힌 보석이 있는지(보석이 잡히지 않은 상태)

move_speed = 12 #발사할 때 이동 스피드, 상황에 따라서 스피드에 변화를 주어야 하기 때문에 변수에 지정
return_speed = 20

# 방향 변수
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
    pygame.image.load(os.path.join(images_path, 'small_gold.png')).convert_alpha(),
    pygame.image.load(os.path.join(images_path, 'big_gold.png')).convert_alpha(),
    pygame.image.load(os.path.join(images_path, 'stone.png')).convert_alpha(),
    pygame.image.load(os.path.join(images_path, 'diamond.png')).convert_alpha(),
]
# 보석 그룹 객체 만들기
gemstone_group = pygame.sprite.Group()
# print(gemstone_group.__dir__())

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

    if claw.rect.left < 0 or claw.rect.bottom > screen_height or claw.rect.right > screen_width: # 화면 벽에 부딪혔을 때 
        to_x = -return_speed

    if claw.offset.x < default_offset_x_claw: # 발사되고 돌아 왔을 때
        to_x = 0
        claw.set_init_state()
        if caught_gemstone: # 잡힌 보석이 있을 때
            #update_score(caught_gemstone.price)
            gemstone_group.remove(caught_gemstone) # 그룹에서 잡힌 보석 제외
            caught_gemstone = None

    # 충돌 처리
    if not caught_gemstone: # 잡힌 보석이 없다면 충돌
        for gemstone in gemstone_group:
            # if claw.rect.colliderect(gemstone): 직사각형 기준 충돌처리
            if pygame.sprite.collide_mask(claw, gemstone): # 투명 영역은 제외하고 실제 이미지 존재하는 부분에 대해 충돌 처리
                caught_gemstone = gemstone # 잡힌 보석
                to_x = -gemstone.speed # 잡힌 보석의 속도에 -한 값을 이동속도로 설정
                break

    if caught_gemstone:
        caught_gemstone.set_position(claw.rect.center, claw.angle)

    screen.blit(background_image, (0, 0))

    gemstone_group.draw(screen) # 그룹내 모든 sprite를 screen에 그림

    claw.update(to_x) # 루프 돌때마다 업데이트

    claw.draw(screen) 

    pygame.display.update()

pygame.quit()
