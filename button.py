import pygame
import os


class Button:
    def __init__(self, surf, button_path_normal, button_path_clicked, image_transform_scale, tooltip,
                 action, height_offset=None, pos=None):
        self.surf = surf
        self.height_offset = height_offset
        self.pos = pos
        self.action = action
        self.is_clicked = False
        self.normal = pygame.transform.scale(pygame.image.load(button_path_normal), image_transform_scale)
        self.clicked = pygame.transform.scale(pygame.image.load(button_path_clicked), image_transform_scale)
        font = pygame.font.Font(os.path.join("assets", "fonts", "8BitOperatorPlus-Bold.ttf"), 20)
        self.tooltip_text = font.render(tooltip, True, "#C05377")
        self.tooltip_surf = pygame.Surface((self.tooltip_text.get_rect().w + 10, self.tooltip_text.get_rect().h + 10))
        self.tooltip_surf.fill("#D1EEDC")
        self.hover = False
        if self.height_offset:
            self.button_pos = (
                (self.surf.get_rect().w - self.normal.get_rect().w) // 2,
                self.surf.get_rect().h // 2 + self.height_offset)
        else:
            self.button_pos = self.pos

    def draw(self):
        self.surf.blit(self.normal if not self.is_clicked else self.clicked, self.button_pos)
        if self.hover:
            self.surf.blit(self.tooltip_surf, (pygame.mouse.get_pos()[0] + 15, pygame.mouse.get_pos()[1]))
            self.surf.blit(self.tooltip_text, (pygame.mouse.get_pos()[0] + 20, pygame.mouse.get_pos()[1] + 5))

    def on_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if pygame.Rect((self.button_pos[0],
                            self.button_pos[1], self.normal.get_rect().w, self.normal.get_rect().h)).collidepoint(
                event.pos):
                self.hover = True
            else:
                self.hover = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect((self.button_pos[0],
                            self.button_pos[1], self.normal.get_rect().w, self.normal.get_rect().h)).collidepoint(
                event.pos):
                self.is_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_clicked:
                self.is_clicked = False
                self.action()
