import pygame, random
clock = pygame.time.Clock()
pygame.init()




WHITE = (255,255,255)
BLACK = (0,0,0)

fps = 30
font1 = pygame.font.SysFont(None, 50)
font2 = pygame.font.SysFont(None, 25)

displayWidth = 800
displayHieght = 600

gameDisplay = pygame.display.set_mode((displayWidth,displayHieght))

pygame.display.set_caption('pong')

def text_objects(text, color, font):
	textSurface = font.render(text, True, color)
	return textSurface,  textSurface.get_rect()


def centeredMessage(msg, color, font, Y):
	textSurf, textRect = text_objects(msg, color, font)
	textRect.center = (displayWidth/2), (Y)
	gameDisplay.blit(textSurf, textRect)


def messageToScreen(msg, color, font, xcor, ycor):
	screenText = font.render(msg, True, color)
	gameDisplay.blit(screenText, [xcor, ycor])

def rect(gameDisplay, color, xcor, ycor, sizex, sizey):
	pygame.draw.rect(gameDisplay, color, [xcor, ycor, sizex, sizey])

class PlayerPaddle():
	def __init__(self):	
		self.w = 50
		self.h = 200
		self.x = displayWidth - self.w - 20
		self.y = displayHieght/2 - self.h
		self.score = 0

	def draw(self):
		rect(gameDisplay, WHITE, self.x, self.y, self.w, self.h)

	def update(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		self.mouse = pygame.mouse.get_pos()
		self.my = self.mouse[1]
		self.y = self.my - self.h/2

class Ball():
	def __init__(self):
		self.x = displayWidth/2
		self.y = displayHieght/2
		self.r = 10
		while True:
			self.yv = random.randint(-15, 15)
			self.xv = 15
			if self.yv > 5 or self.yv < -5:
				break
			if self.xv > 5 or self.xv < -5:
				break


	def draw(self):
		pygame.draw.circle(gameDisplay, WHITE, [self.x, self.y], self.r, 0)

	def update(self, paddleR, paddleL):
		if self.y >= displayHieght-self.r or self.y <= self.r:
			self.yv = -self.yv
		if self.x >= paddleR.x - self.r and self.y >= paddleR.y - self.r and self.y <= paddleR.y + paddleR.h + self.r or self.x <= paddleL.x + paddleL.w + self.r and self.y >= paddleL.y - self.r and self.y <= paddleL.y + paddleL.h + self.r :
			self.xv = -self.xv 
		
		self.y += self.yv
		self.x += self.xv
		

		self.x = int(self.x)
		self.y = int(self.y)

	def checkScore(self):
		if self.x > displayWidth - self.r:
			return 1
		elif self.x < self.r:
			return 2
		else:
			return None

	def reset(self):
		self.y = displayHieght/2
		self.x = displayWidth/2
		while True:
			self.yv = random.randint(-15, 15)
			self.xv = -15
			if self.yv > 5 or self.yv < -5:
				break
			if self.xv > 5 or self.xv < -5:
				break


class ComputerPaddle():
	def __init__(self):
		self.w = 50
		self.h = 200
		self.x = 20
		self.y = displayHieght/2 - self.h
		self.diff = 5
		self.score = 0

	def update(self, ball):
		if self.y + self.h * 1/2 > ball.y and self.y + self.diff >= 0:
			self.y -= self.diff
		elif self.y + self.h * 1/2 < ball.y and self.y + self.diff <= displayHieght:
			self.y += self.diff
		

	def draw(self):
		rect(gameDisplay, WHITE, self.x, self.y, self.w, self.h)


def game():
	c = ComputerPaddle()
	p = PlayerPaddle()
	b = Ball()
	while True:
		gameDisplay.fill(BLACK)
		p.update()
		c.update(b)
		b.update(p, c)
		p.draw()
		c.draw()
		b.draw()
		score = b.checkScore()
		if score == 1:
			p.score += 1
			b.reset()
		elif score == 2:
			c.score += 1
			b.reset()
		if p.score == 5:
			win = 1
			break
		elif c.score == 5:
			win = 2
			break
		
		messageToScreen(str(c.score), WHITE, font2, 600, 100)
		messageToScreen(str(p.score), WHITE, font2, 200, 100)
		pygame.display.update()

	gameDisplay.fill(BLACK)
	if win == 1:
		centeredMessage('You Lose', WHITE, font1, displayHieght/2)
	else:
		centeredMessage('You Win', WHITE, font1, displayHieght/2)
	centeredMessage('Press C to return to play again and q to quit', WHITE, font2, displayHieght/2 + 40)
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					game()
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()	
game()
