import pygame
class AnimatedSprite(pygame.sprite.Sprite):
 
    def __init__(self, position):
        super(AnimatedSprite, self).__init__()
 
        size = (680, 472)
 
        # 여러장의 이미지를 리스트로 저장한다. 이미지 경로는 자신들의 경로를 사용한다.
        images = []
        images.append(pygame.image.load('/Users/joon/Desktop/Python Game Contest/ㅎㅇㅂ대지 1.png'))
        images.append(pygame.image.load('/Users/joon/Desktop/Python Game Contest/ㅎㅇㅂ대지 1_1.png'))
        images.append(pygame.image.load('/Users/joon/Desktop/Python Game Contest/ㅎㅇㅂ대지 1_2.png'))
        images.append(pygame.image.load('/Users/joon/Desktop/Python Game Contest/ㅎㅇㅂ대지 1_3.png'))
        images.append(pygame.image.load('/Users/joon/Desktop/Python Game Contest/ㅎㅇㅂ대지 1_2.png'))
        images.append(pygame.image.load('/Users/joon/Desktop/Python Game Contest/ㅎㅇㅂ대지 1_1.png'))
 
        # rect 만들기
        self.rect = pygame.Rect(position, size)

        # Rect 크기와 Image 크기 맞추기. pygame.transform.scale
        self.images = [pygame.transform.scale(image, size) for image in images]
 
        # 캐릭터의 첫번째 이미지
        self.index = 0
        self.image = images[self.index]  # 'image' is the current image of the animation.

    def update(self):
        # update를 통해 캐릭터의 이미지가 계속 반복해서 나타나도록 한다.
        self.index += 1
 
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]