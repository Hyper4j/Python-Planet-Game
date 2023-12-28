import pygame
import random

pygame.init()

background = pygame.display.set_mode((960, 720))
pygame.display.set_caption("행성 피하기")

image_background = pygame.image.load("images\Galaxy.png")
image_plane = pygame.image.load("images\plane2_1.png")
image_planet1 = pygame.image.load("images\행성1.png")
image_planet2 = pygame.image.load("images\행성2.png")
image_planet3 = pygame.image.load("images\행성3.png")
image_planet4 = pygame.image.load("images\행성4.png")
image_heart = pygame.image.load("images\heart.png")

sound_background = pygame.mixer.Sound("sounds/background.wav")
sound_winner = pygame.mixer.Sound("sounds/clear.wav")
sound_shoot = pygame.mixer.Sound("sounds/shoot.wav")
sound_planet_die = pygame.mixer.Sound("sounds/planet_die.wav")
sound_boss_die = pygame.mixer.Sound("sounds/boss_die.wav")

size_bg = (background.get_size()[0], background.get_size()[1])
size_plane = (image_plane.get_rect().size[0], image_plane.get_rect().size[1])
size_planet1 = (image_planet1.get_rect().size[0], image_planet1.get_rect().size[1])
size_planet2 = (image_planet2.get_rect().size[0], image_planet2.get_rect().size[1])
size_planet3 = (image_planet3.get_rect().size[0], image_planet3.get_rect().size[1])
size_planet4 = (image_planet4.get_rect().size[0], image_planet4.get_rect().size[1])

x_pos = size_bg[0]/2 - size_plane[0]/2
y_pos = size_bg[1] - size_plane[1]

# 행성 좌표 설정
planets = []

# 레이저빔 설정
shoot=[]

# 스코어 및 타이머 설정
font = pygame.font.SysFont(None, 30)
restart_font = pygame.font.SysFont(None, 50)
ending_font = pygame.font.SysFont(None, 100)

timer = 60 
time_remain = 0
score = 0

# 시간 정보+
start_ticks = pygame.time.get_ticks()
 
# 게임 설정란
fps=100
speed=7
health=5

planet1_speed=5
planet1_health=1

planet2_speed=5
planet2_health=2

boss1_speed=1
boss1_planet_health=10

boss2_speed=10
boss2_planet_health=30

play = True
winner = False
restart = False
onClickResetButton = False
sound_background.play(-1)
while play:  
    deltaTime = pygame.time.Clock().tick(fps)

    # 행성 생성 이벤트
    onPlanetSummon = random.randint(1, 100)
    if time_remain <= timer:
        if onPlanetSummon <= 20:
            # (행성종류, x좌표, y좌표, 체력)a 
            # 행성종류 0 -> 일반1, 1 -> 일반2, 2 -> 보스1, 3-> 보스2
            planets.append((0, random.randint(0, size_bg[0] - size_planet1[0]), 0, planet1_health))
    if time_remain <= (timer-10):
        if onPlanetSummon <= 5:
            planets.append((1, random.randint(0, size_bg[0] - size_planet2[0]), 0, planet2_health))
    if time_remain <= (timer-30):
        if onPlanetSummon <= 2:
            planets.append((2, random.randint(0, size_bg[0] - size_planet3[0]), 0, boss1_planet_health))
    if time_remain <= (timer-40):
        if onPlanetSummon <= 2:
            planets.append((3, random.randint(0, size_bg[0] - size_planet4[0]), 0, boss2_planet_health))
    
    # 키 이벤트
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if restart == True or winner == True:
                    
                    # 마우스 왼쪽 클릭( 재시작 부분 )
                    x=event.pos[0]
                    y=event.pos[1]

                    pos = (300, 370)
                    size = (370, 120)
                    if (x >= pos[0] and x <= pos[0]+size[0]):
                        if (y >= pos[1] and y <= pos[1]+size[1]):
                            # 초기화를 이용하여 재시작한다.
                            sound_shoot.play()
                            onClickResetButton=True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sound_shoot.play()
                shoot.append((x_pos+(size_plane[0]//2), y_pos))

    # 승리했을때 화면출력
    if winner == True:
        background.blit(image_background, (0, 0))
        pygame.draw.rect(background, (255, 255, 0), (300, 370, 370, 120))
        text = ending_font.render("Congratulation!", True, (255, 255, 255))
        text2 = ending_font.render("Total Score: "+str(score), True, (255, 255, 255))
        background.blit(text, (200, 300))
        background.blit(text2, (230, 200))

        button_text = ending_font.render("RESTART", True, (0, 0, 0))
        background.blit(button_text, (330, 400))

        pygame.display.update()
        # 변수 초기화 후 다시 시작
        if onClickResetButton == True:
            x_pos = size_bg[0]/2 - size_plane[0]/2
            y_pos = size_bg[1] - size_plane[1]

            planets = []

            shoot=[]

            timer = 60
            time_remain = 0
            score = 0

            health=5

            sound_background.play(-1)

            start_ticks = pygame.time.get_ticks()
            winner = False
            onClickResetButton = False
            restart=False
            play=True
        if play == False:
            break
        continue

    # 죽었을때 화면 출력
    if restart == True:
        background.blit(image_background, (0, 0))
        pygame.draw.rect(background, (255, 255, 255), (100, 250, 760, 300))
        pygame.draw.rect(background, (255, 255, 0), (300, 370, 370, 120))

        text = restart_font.render("Are you sure you want to restart the game?", True, (0, 0, 0))
        button_text = ending_font.render("RESTART", True, (0, 0, 0))
        background.blit(text, (125, 300))
        background.blit(button_text, (330, 400))
        pygame.display.update()
        # 변수 초기화 후 다시 시작
        if onClickResetButton == True:
            x_pos = size_bg[0]/2 - size_plane[0]/2
            y_pos = size_bg[1] - size_plane[1]

            planets = []

            shoot=[]

            timer = 60
            time_remain = 0
            score = 0

            health=5

            sound_background.play(-1)

            start_ticks = pygame.time.get_ticks()
            winner = False
            onClickResetButton = False
            restart=False
            play=True
        if play == False:
            break
        continue


    keys = pygame.key.get_pressed()
    # 방향키 코드
    x_pos += (keys[pygame.K_d] - keys[pygame.K_a]) * speed
    y_pos += (keys[pygame.K_s] - keys[pygame.K_w]) * speed

    # 우주선이 맵 밖으로 나가지않도록 하는 코드
    if x_pos <= 0:
        x_pos = 0
    elif x_pos >= size_bg[0]-size_plane[0]:
        x_pos = size_bg[0]-size_plane[0]
    
    if y_pos <= 0:
        y_pos = 0
    elif y_pos >= size_bg[1]-size_plane[1]:
        y_pos = size_bg[1]-size_plane[1]
    
    # 배경 채우기
    background.blit(image_background, (0, 0))
    
    planet_rect = []

    # 행성 튜플들을 불러와 행성 이미지 불러오기
    for p in planets:
        a=(0,0,0,0)
        index=planets.index(p)
        if(p[0] == 0):
            a=(p[0], p[1], p[2]+planet1_speed, p[3])
            background.blit(image_planet1, (p[1], p[2]))
            planet_rect.append((index, background.blit(image_planet1, (p[1], p[2]))))
        elif(p[0] == 1):
            a=(p[0], p[1], p[2]+planet2_speed, p[3])
            background.blit(image_planet2, (p[1], p[2]))
            planet_rect.append((index, background.blit(image_planet2, (p[1], p[2]))))
        elif(p[0] == 2):
            a=(p[0], p[1], p[2]+boss1_speed, p[3])
            background.blit(image_planet3, (p[1], p[2]))
            planet_rect.append((index, background.blit(image_planet3, (p[1], p[2]))))
        elif(p[0] == 3):
            a=(p[0], p[1], p[2]+boss2_speed, p[3])
            background.blit(image_planet4, (p[1], p[2]))
            planet_rect.append((index, background.blit(image_planet4, (p[1], p[2]))))
        
        planets[index]=a
        if(a[2] >= size_bg[1]):
            # 행성이 맵밖으로 나가면 메모리 관리를 위해 삭제
            planets.remove(a)
    
    # 발사된 총알의 좌표를 불러와 총알 그리기
    for i in shoot:
        index=shoot.index(i)
        a=(i[0], i[1]-20)
        line_rect = pygame.draw.line(background, (255, 255, 0), a, (i[0], i[1]), 15)
   
        isReach=False  
        # 행성과 총알이 닿았을때 구문
        for p in planet_rect: 
            if p[1].colliderect(line_rect):
                isReach = True
                try:
                    planets[p[0]] = (planets[p[0]][0], planets[p[0]][1], planets[p[0]][2], planets[p[0]][3] - 1)
                    if planets[p[0]][3]==0:
                        # 행성이 체력이 없어서 삭제되는 구문
                        if(planets[p[0]][0] >= 2):
                            sound_boss_die.set_volume(10)
                            sound_boss_die.play()
                        else:
                            sound_planet_die.set_volume(10)
                            sound_planet_die.play() 

                        # 행성 종류마다의 체력만큼 스코어를 올린다.
                        b=(planet1_health, planet2_health, boss1_planet_health, boss2_planet_health)
                        score = score + b[planets[p[0]][0]]
                        planets.remove(planets[p[0]])
                except:
                    print("오류 발생")
        if isReach == False:
            pygame.draw.line(background, (255, 255, 0), a, (i[0], i[1]), 15)
        else:
            shoot.remove(i)
            continue
        shoot[index]=a
        if(a[1] < 0):
            # 총알이 맵밖으로 나가면 메모리 관리를 위해 삭제
            shoot.remove(a)
    
    planeRect = background.blit(image_plane, (x_pos, y_pos))

    # 우주선과 행성이 닿았을때 구문
    for p in planet_rect:
        if p[1].colliderect(planeRect):
            try:
                health = health - 1
                score = score - planets[p[0]][3]
                planets.remove(planets[p[0]])
            except:
                print("오류 발생2")
    
    # 우주선 체력 표시
    x_0=10
    for i in range(0, health):
        x_0 = 10+(i*30)
        background.blit(image_heart, (x_0, 70))
    

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

    time_remain = int(timer - elapsed_time)

    # 타이머
    timerRect = font.render(str(time_remain)+"sec", True, (255,255,255))

    # 스코어
    scoreRect = font.render(str("Score: ")+str(score), True, (255, 255, 0))

    #경과 시간 표시
    background.blit(timerRect, (10, 10))

    #스코어 표시
    background.blit(scoreRect, (10, 40))

    # 끝까지 다 버텼다면
    if time_remain <= 0:
        sound_background.stop()
        sound_winner.play()
        print("최종 스코어 : ", score)
        winner = True
    
    # 체력이 0이라면
    if(health <= 0):
        print("남은 시간 : ", int(time_remain))
        print("최종 스코어 : ", score)
        sound_background.stop()
        sound_boss_die.play()
        restart = True

    pygame.display.update()
sound_background.stop()
if winner == True:
    sound_winner.play()

pygame.quit()