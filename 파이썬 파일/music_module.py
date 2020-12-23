import os
import pygame
import threading

class music_module :
    def pygame_init(self):
        freq = 21500
        bitsize = -16
        channels = 1
        buffer = 2048

        pygame.mixer.init(freq, bitsize, channels, buffer)

    def pygame_play(self, num):
        # default : pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        if num == 1 :
            filename = "warrior_position.mp3"
        elif num == 2:
            filename = "neck_stretch.mp3"
        elif num == 3:
            filename = "shoulder_stretch.mp3"
        elif num == 4:
            filename = "leg_stretch.mp3"
        elif num == 5:
            filename = "lower_body.mp3"

        if num == 6:
            filename = "fighting.mp3"
        elif num == 7:
            filename = "good.mp3"
        elif num == 8:
            filename = "good_stance.mp3"
        elif num == 9:
            filename = "your_best.mp3"
        elif num == 10:
            filename = "fighting.mp3"

        if num == 11:
            filename = "thankyou.mp3"

        pygame.mixer.music.load("C:\\Users\\Choi CheolWoo\\Documents\\GOMRecorder\\"+filename)
        pygame.mixer.music.play()

        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(30)
        pygame.mixer.quit()

if __name__== '__main__':
    music_file = "C:\\Users\\Choi CheolWoo\\Documents\\GOMRecorder\\5-(1).mp3"
    mm = music_module()
    mm.pygame_init()
    th = threading.Thread(target=mm.pygame_play, args=(11,))
    th.start()
    #mm.pygame_play(music_file)







