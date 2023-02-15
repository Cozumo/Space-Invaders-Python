import math
import pygame
import random

pygame.init()                                         # Initialize the pygame
screen = pygame.display.set_mode((800, 600))          # create the screen
background = pygame.image.load('background.png')      # Background
Txt_font = pygame.font.Font('freesansbold.ttf', 64)   # txt display Over

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Player
class Player:
    playerImg = pygame.image.load('player.png')
    playerX = 370
    playerY = 480
    playerX_change = 0
    player_health = 250
    red = (255, 54, 71)
    green = (40, 255, 0)

    def PlayerHealthBar(self):
        pygame.draw.rect(screen, (0,0,0), (27, 558, 256, 12))
        pygame.draw.rect(screen, self.red, (30, 560, 250, 8))
        pygame.draw.rect(screen, self.green, (30, 560, self.player_health, 8))
        if(self.player_health <= 0):
            for i in range(EnemyOne.num_of_enemies):
                EnemyOne.enemyY[i] = 500
            for i in range(EnemyTwo.num_of_enemiesTwo):
                EnemyTwo.enemyTwoY[i] = 500

    def PlayerMovementLimit(self):
        Player.playerX += Player.playerX_change
        if Player.playerX <= 0:
            Player.playerX = 0
        elif Player.playerX >= 736:
            Player.playerX = 736

    def Get_damage(self, amount):
        if self.current_Health > 0:
            self.current_Health -= amount

    def MovementKey(self, event):
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Player.playerX_change = -5
            if event.key == pygame.K_RIGHT:
                Player.playerX_change = 5
            # Bullet fired
            if event.key == pygame.K_SPACE:
                if Bullet.bullet_state is "ready":
                    Bullet.bulletX = Player.playerX
                    fire_bullet(Bullet.bulletX, Bullet.bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                Player.playerX_change = 0


# All enemies common functions
class EnemyBase:

    def StartEnemiesBase(self, nenemy, eX, eY, eXchange, eYchange):
        eX.append(random.randint(0, 736))
        eY.append(random.randint(50, 150))
        eXchange.append(4)
        eYchange.append(40)

    def DeleteEnemiesArrayData(self, Eimg, Ex, Ey, ExChange, EyChange):
        Eimg.clear()
        Ex.clear()
        Ey.clear()
        ExChange.clear()
        EyChange.clear()

    def enemymovebase(self, Bl, nenemy, eImg, eX, eY, eXchange, eYchange):
        for i in range(nenemy):
            # Game Over
            if eY[i] > 440:
                for j in range(nenemy):
                    eY[j] = 2000
                game_over_text()
                break

            eX[i] += eXchange[i]
            if eX[i] <= 0:
                eXchange[i] = 2
                eY[i] += eYchange[i]
            elif eX[i] >= 736:
                eXchange[i] = -2
                eY[i] += eYchange[i]

            eX[i], eY[i], eImg[i] = Bl.Collision(i, eX[i], eY[i], eImg[i])
        return eX, eY, eImg


# EnemyOne - Basic
class EnemyOne:
    enemyImg, enemyX, enemyY, enemyX_change, enemyY_change = [], [], [], [], []
    num_of_enemies = 6
    Eb = EnemyBase()

    def DeleteEOne(self):
        self.Eb.DeleteEnemiesArrayData(self.enemyImg, self.enemyX, self.enemyY,
                     self.enemyX_change, self.enemyY_change)

    def StartEnemies(self):
        for i in range(self.num_of_enemies):
            self.enemyImg.append(pygame.image.load('enemy.png'))
            self.Eb.StartEnemiesBase(self.num_of_enemies, self.enemyX, self.enemyY, self.enemyX_change, self.enemyY_change)

    def EnemyMovement(self, Bl):
        self.Eb.enemymovebase(Bl, self.num_of_enemies, self.enemyImg, self.enemyX, self.enemyY,
                     self.enemyX_change, self.enemyY_change)


# EnemyTwo - Shooting lasers
class EnemyTwo:
    enemyTwoImg, enemyTwoX, enemyTwoY, enemyTwoX_change, enemyTwoY_change = [], [], [], [], []
    num_of_enemiesTwo = 6
    bulletEnemyTwoImg ,bulletEnemyTwoX ,bulletEnemyTwoY ,bulletEnemyTwoY_change ,bullet_stateEnemyTwo= [], [], [], [], []
    BulletSpeed = -5
    numbullets = 3
    Eb = EnemyBase()

    def DeleteETwo(self):
        self.Eb.DeleteEnemiesArrayData(self.enemyTwoImg, self.enemyTwoX, self.enemyTwoY,
                                       self.enemyTwoX_change, self.enemyTwoY_change)

    def StartEnemies(self):
        for i in range(self.num_of_enemiesTwo):
            self.enemyTwoImg.append(pygame.image.load('Player.png'))
            self.Eb.StartEnemiesBase(self.num_of_enemiesTwo, self.enemyTwoX, self.enemyTwoY,
                                self.enemyTwoX_change, self.enemyTwoY_change)

    def EnemyMovement(self, Bl):
        self.Eb.enemymovebase(Bl,self.num_of_enemiesTwo,self.enemyTwoImg, self.enemyTwoX, self.enemyTwoY,
                         self.enemyTwoX_change,self.enemyTwoY_change)

    def StartenTwobullets(self):
        for i in range(self.numbullets):
            self.bulletEnemyTwoImg.append(pygame.image.load('laser.png'))
            self.bulletEnemyTwoX.append(0)
            self.bulletEnemyTwoY.append(0)
            self.bulletEnemyTwoY_change.append(self.BulletSpeed)
            self.bullet_stateEnemyTwo.append("ready")

    def DeleteETwobullets(self):
        self.Eb.DeleteEnemiesArrayData(self.bulletEnemyTwoImg, self.bulletEnemyTwoX, self.bulletEnemyTwoY,
                                       self.bulletEnemyTwoY_change, self.bullet_stateEnemyTwo)

    def EnemyBulletMovement(self):
        for i in range(self.numbullets):
            if EnemyTwo.bulletEnemyTwoY[i] >= 736:
                EnemyTwo.bulletEnemyTwoY[i] = 0
                EnemyTwo.bullet_stateEnemyTwo[i] = "ready"
            if EnemyTwo.bullet_stateEnemyTwo[i] is "fire":
                fire_bullet_EnemyTwo(EnemyTwo.bulletEnemyTwoX[i], EnemyTwo.bulletEnemyTwoY[i], i)
                EnemyTwo.bulletEnemyTwoY[i] -= EnemyTwo.bulletEnemyTwoY_change[i]

    def BulletEnemyTwoLaunch(self):
        for i in range(self.numbullets):
            lanchposnum = random.randint(0, self.num_of_enemiesTwo - 1)
            if EnemyTwo.bullet_stateEnemyTwo[i] is "ready":
                EnemyTwo.bulletEnemyTwoX[i] = self.enemyTwoX[lanchposnum]
                EnemyTwo.bulletEnemyTwoY[i] = self.enemyTwoY[lanchposnum]
                fire_bullet_EnemyTwo(EnemyTwo.bulletEnemyTwoX[i], EnemyTwo.bulletEnemyTwoY[i], i)

    def EnemyBulletCollision(self, Ex, Ey):
        # Collision
        for i in range(self.numbullets):
            collision = self.isCollision(Ex, Ey, i)
            if collision:
                EnemyTwo.bullet_stateEnemyTwo[i] = "ready"
                EnemyTwo.bulletEnemyTwoX[i] = Ex
                EnemyTwo.bulletEnemyTwoY[i] = Ey
                Player.player_health -= 40

    def isCollision(self, Ex , Ey, i):
            distance = math.sqrt(math.pow(Ex - self.bulletEnemyTwoX[i], 2) + (math.pow(Ey - self.bulletEnemyTwoY[i], 2)))
            if distance < 27:
                return True
            else:
                return False


class Level:
    # Level declaration
    level = 1
    onetime = False
    Sectime = False
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    fonttransition = pygame.font.Font(None, 32)
    textX = 10
    testY = 10

    def Levelnumber(self, num):
        self.level = num

    def LevelTransition(self):
        # Level transition text
        self.level += 1
        self.level_text(self.textX, self.testY)
            #Display level number
        should_quit = False
        while not should_quit:
            over_text = Txt_font.render(f"Level {self.level}", True, (255, 255, 255))
            screen.blit(over_text, (285, 240))
            text = self.fonttransition.render("PRESS ESCAPE TO CONTINUE.", True, (255, 255, 255))
            text_rect = (230, (600 / 2)+10)
            screen.blit(text, text_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        should_quit = True

        for i in range(EnemyOne.num_of_enemies):
            EnemyOne.enemyX[i] = random.randint(0, 736)
            EnemyOne.enemyY[i] = random.randint(50, 150)
            enemy(EnemyOne.enemyX[i], EnemyOne.enemyY[i], i, EnemyOne.enemyImg[i])

        for i in range(EnemyTwo.num_of_enemiesTwo):
            EnemyTwo.enemyTwoX[i] = random.randint(0, 736)
            EnemyTwo.enemyTwoY[i] = random.randint(50, 150)
            enemy(EnemyTwo.enemyTwoX[i], EnemyTwo.enemyTwoY[i], i, EnemyTwo.enemyTwoImg[i])

    def winOver(self, rqrScore):
        # Win mechanics
        if Level.score_value > rqrScore:
            Win_text()
            for j in range(EnemyOne.num_of_enemies):
                EnemyOne.enemyY[j] = -2000
                EnemyTwo.enemyTwoX[j] = 1800
                EnemyTwo.enemyTwoY[j] = -2000

    def level_text(self, x, y):
        leveltext = self.font.render(f"LEVEL {self.level}", True, (255, 255, 255))
        screen.blit(leveltext, (x, y + 35))

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
class Bullet:
    bulletImg = pygame.image.load('bullet.png')
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    def BulletMovement(self):
        # Bullet Movement
        if Bullet.bulletY <= 0:
            Bullet.bulletY = 480
            Bullet.bullet_state = "ready"
        if Bullet.bullet_state is "fire":
            fire_bullet(Bullet.bulletX, Bullet.bulletY)
            Bullet.bulletY -= Bullet.bulletY_change

    def Collision(self, i, Ex, Ey, Eimg):
        # Collision
        collision = self.isCollision(Ex, Ey)
        if collision:
            Bullet.bulletY = 480
            Bullet.bullet_state = "ready"
            Level.score_value += 1
            Ex = random.randint(0, 736)
            Ey = random.randint(50, 150)
            if(Player.player_health >= 240):
                Player.player_health = 250
            else:
                Player.player_health += 10
        Eimg = enemy(Ex, Ey, i, Eimg)
        return Ex, Ey, Eimg

    def isCollision(self, Ex , Ey):
        distance = math.sqrt(math.pow(Ex - self.bulletX, 2) + (math.pow(Ey - self.bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False


# Assign Objects
En, En2, Lv, Pl, Bl= EnemyOne(), EnemyTwo(), Level(), Player(), Bullet()


class Button:
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
    FONT = pygame.font.Font(None, 32)
    COLOR_INACTIVE = pygame.Color('chartreuse4')
    width = screen.get_width()
    height = screen.get_height()

    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = self.COLOR_INACTIVE

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, screen):
        text_surface = self.FONT.render(self.text, True, self.color)
        screen.blit(text_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class InputBox:
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
    FONT = pygame.font.Font(None, 32)
    COLOR_INACTIVE = pygame.Color('chartreuse4')
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)
        return self.text

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Game:
    playing = True
    running = True
    Credentials = True
    red = (255, 54, 71)
    light = (255, 255, 71)
    orange = (255, 200, 71)
    black = (0, 0, 0)
    txt = pygame.font.Font('freesansbold.ttf', 16)
    width = screen.get_width()
    height = screen.get_height()
    logname = ""

    def Login_Signin(self):
        Game.Credentials = True
        Game.playing = False
        Game.running = False

        # create rectangle
        Name_input = InputBox(100, 100, 140, 32)
        Pass_input = InputBox(100, 140, 140, 32)
        bLog = Button(100, 180, 140, 32, "LOG IN")
        sName_input = InputBox(100, 320, 180, 32)
        sPass_input = InputBox(100, 360, 190, 32)
        bSign = Button(100, 400, 140, 32, "SIGN IN")
        boxes = [Name_input, Pass_input, sName_input, sPass_input]

        while self.Credentials:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                #get text from input boxes
                Nametxt = Name_input.handle_event(event)
                Passtxt = Pass_input.handle_event(event)
                sNametxt = sName_input.handle_event(event)
                sPasstxt = sPass_input.handle_event(event)
                # get sign Click True/False
                signout = bSign.handle_event(event)
                if signout == True:
                    f = open("Name.txt", 'r')
                    info = f.read()
                    if sNametxt in info:
                        TextDisplay("This name already exists.")
                        pygame.display.update()
                    f.close()
                    if( sNametxt != "" and sPasstxt != None):
                        Name = open("Name.txt", 'a')
                        info = sNametxt + " " + sPasstxt + "\n"
                        Name.write(info)
                        Name.close()
                # get Login Click True/False
                logout = bLog.handle_event(event)
                if logout == True:
                    name, password = Nametxt, Passtxt
                    File = "Name.txt"
                    if(name != "" and password != ""):
                        if self.is_authorized(name, password, File):
                            self.logname = name
                            self.MainMenu()
                            self.Credentials = False
                        else:
                            TextDisplay("Login not matched.")
            for box in boxes:
                box.update()
            screen.fill((30, 30, 30))
            for box in boxes:
                box.draw(screen)
            bLog.draw(screen)
            bSign.draw(screen)
            pygame.display.flip()
            clock.tick(30)

    def get_existing_users(self, Name):
        with open(Name, "r") as fp:
            for line in fp.readlines():
                username, password = line.split()
                yield username, password

    def is_authorized(self, username, password, Name):
        return any((user == (username, password) for user in self.get_existing_users(Name)))

    def MainMenu(self):
        Game.playing = False
        Game.running = True
        text = self.txt.render('StartGame', True, self.red)
        Player.player_health = 250
        Level.score_value = 0
        Lv.Levelnumber(1)
        Level.onetime = False
        Level.Sectime = False
        En.DeleteEOne()
        En2.DeleteETwo()
        En2.DeleteETwobullets()
        namelog = self.txt.render("USERNAME: "+self.logname.upper(), True, (255, 255, 71))

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game.playing = False
                    Game.running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.width / 2 - 100 <= mouse[0] <= self.width / 2 + 140 and self.height / 2 - 40 <= mouse[1] <= self.height / 2 + 40:
                        self.Gameloop()
            screen.fill((120, 25, 70))
            screen.blit(namelog, (50, 120))
            mouse = pygame.mouse.get_pos()
            if self.width / 2  - 100 <= mouse[0] <= self.width / 2 + 140 and self.height / 2 - 40 <= mouse[1] <= self.height / 2 + 40:
                pygame.draw.rect(screen, self.orange, [(self.width / 2) - 100, (self.height / 2) - 30, 240, 70])
            else:
                pygame.draw.rect(screen, self.black, [(self.width / 2) - 100, (self.height / 2) - 30, 240, 70])
            screen.blit(text, (self.width / 2 - 20, (self.height / 2) - 4))
            pygame.display.update()

    def Gameloop(self):
        Game.running = False
        Game.playing = True
        self.EnemyPerLevelChanges(6, 6, 3)
        while self.playing:
            # RGB = Red, Green, Blue
            screen.fill((0, 0, 0))
            # Background Image
            screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game.playing = False
                    screen.fill((0,0,0))
                    GameTransitMenu()

                Pl.MovementKey(event)

            Bl.BulletMovement()

            Pl.PlayerMovementLimit()
            Pl.PlayerHealthBar()

            En.EnemyMovement(Bl)

            if Lv.score_value > 1:
                En2.EnemyMovement(Bl)
                En2.EnemyBulletMovement()
                En2.BulletEnemyTwoLaunch()
                En2.EnemyBulletCollision(Pl.playerX, Pl.playerY)

            # win call
            Lv.winOver(40)

            # Level 2 transition text
            if Lv.score_value > 1 and Lv.onetime == False:
                Lv.LevelTransition()
                Level.onetime = True

            # Level 3 transition text
            if Lv.score_value > 3 and Lv.Sectime == False:
                Lv.LevelTransition()
                Level.Sectime = True
                self.EnemyPerLevelChanges(2, 15, 8)

            # Score mechanics
            player(Player.playerX, Player.playerY)
            Lv.level_text(Level.textX, Level.testY)
            show_score(Level.textX, Level.testY)
            pygame.display.update()

    def EnemyPerLevelChanges(self, E1num, E2num, Bnum):
        EnemyOne.num_of_enemies = E1num
        EnemyTwo.num_of_enemiesTwo = E2num
        EnemyTwo.numbullets = Bnum
        En.StartEnemies()
        En2.StartEnemies()
        En2.StartenTwobullets()

def GameTransitMenu():
    Gm.MainMenu()

def show_score(x, y):
    score = Level.font.render("Score : " + str(Level.score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def fire_bullet_EnemyTwo(x, y, i):
    EnemyTwo.bullet_stateEnemyTwo[i] = "fire"
    screen.blit(EnemyTwo.bulletEnemyTwoImg[i], (x, y))

def game_over_text():
    over_text = Txt_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def Win_text():
    leveltext = Txt_font.render("YOU WIN!", True, (255, 255, 255))
    screen.blit(leveltext, (250, 250))

def TextDisplay(tt):
    txt = Txt_font.render(tt, True, (255, 255, 255))
    screen.blit(txt, (250, 250))

def player(x, y):
    screen.blit(Player.playerImg, (x, y))

def enemy(x, y, i, Eimg):
    screen.blit(Eimg, (x, y))
    return Eimg

def fire_bullet(x, y):
    Bullet.bullet_state = "fire"
    screen.blit(Bullet.bulletImg, (x, y))

# Declaration of functions
Gm = Game()
Gm.Login_Signin()