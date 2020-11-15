import pygame

class Camera(object):
    def __init__(self, lvl_width, lvl_height, win_width, win_height):
        self.state = pygame.Rect(0, 0, lvl_width, lvl_height)
        self.lvl_width = lvl_width
        self.lvl_height = lvl_height
        self.win_width = win_width
        self.win_height = win_height

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def camera_func(self, camera, target_rect):
        # we want to center target_rect
        x = -target_rect.center[0] + self.win_width/2
        y = -target_rect.center[1] + self.win_height/2
        # move the camera. Let's use some vectors so we can easily substract/multiply
        camera.topleft += (pygame.Vector2((x, y)) - pygame.Vector2(camera.topleft))  # add some smoothness coolnes
        # set max/min x/y so we don't see stuff outside the world
        camera.x = max(-(camera.width-self.win_width), min(0, camera.x))
        camera.y = max(-(camera.height-self.win_height), min(0, camera.y))

        return camera

#    def camera_func(self, state, rect):
#        l, t, _, _ = rect # l = left,  t = top
#        _, _, w, h = state      # w = width, h = height
#        return pygame.Rect(-l+self.win_width//2, -t+self.win_height//2, w, h)
