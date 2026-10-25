import pygame, random, sys
pygame.init()
W, H = 800, 400
scr = pygame.display.set_mode((W, H))
pygame.display.set_caption("Geometry Dash Mini")
clk = pygame.time.Clock()
G, J_F = 0.8, -12
class Cube:
    def __init__(self):
        self.r = pygame.Rect(100, H-90, 40, 40)
        self.v = 0
        self.on_g = True
        self.ang = 0
    def jump(self):
        if self.on_g:
            self.v = J_F
            self.on_g = False
    def update(self):
        self.v += G
        self.r.y += self.v
        if self.r.bottom >= H-50:
            self.r.bottom = H-50
            self.v = 0
            self.on_g = True
        if not self.on_g:
            self.ang = (self.ang - 5) % 360
        else:
            self.ang = round(self.ang / 90) * 90
class Spike:
    def __init__(self, spd):
        self.x = W
        self.spd = spd
        self.w, self.h = 30, 40
    def update(self):
        self.x -= self.spd
    def draw(self):
        p1 = (self.x, H-50)
        p2 = (self.x + self.w, H-50)
        p3 = (self.x + self.w//2, H-50 - self.h)
        pygame.draw.polygon(scr, (220, 50, 50), [p1, p2, p3])
    def g_r(self):
        return pygame.Rect(self.x, H-50-self.h, self.w, self.h)
c = Cube()
spks = []
spk_t = 0
sc, h_sc = 0, 0
spd = 6
g_ovr = False
font = pygame.font.SysFont("Arial", 24, bold=True)
while True:
    scr.fill((20, 20, 30))
    pygame.draw.rect(scr, (40, 40, 60), (0, H-50, W, 50))
    pygame.draw.line(scr, (255, 255, 255), (0, H-50), (W, H-50), 3)
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
            if (e.key == pygame.K_SPACE or e.key == pygame.K_UP) and not g_ovr: c.jump()
            if e.key == pygame.K_r and g_ovr:
                c, spks, sc, spd, g_ovr = Cube(), [], 0, 6, False
    if not g_ovr:
        c.update()
        spk_t += 1
        if spk_t > random.randint(60, 120):
            spks.append(Spike(spd))
            spk_t = 0
        for s in spks[:]:
            s.update()
            if s.x < -30:
                spks.remove(s)
                sc += 1
                if sc % 5 == 0: spd += 0.5
            if c.r.colliderect(s.g_r()):
                g_ovr = True
                if sc > h_sc: h_sc = sc
    s_surf = pygame.Surface((c.r.w, c.r.h), pygame.SRCALPHA)
    pygame.draw.rect(s_surf, (0, 255, 255), (0, 0, c.r.w, c.r.h))
    pygame.draw.rect(s_surf, (0, 150, 150), (5, 5, c.r.w-10, c.r.h-10))
    r_surf = pygame.transform.rotate(s_surf, c.ang)
    r_rect = r_surf.get_rect(center=c.r.center)
    scr.blit(r_surf, r_rect.topleft)
    for s in spks: s.draw()
    scr.blit(font.render(f"SCORE: {sc}", True, (255,255,255)), (20, 20))
    scr.blit(font.render(f"BEST: {h_sc}", True, (255,255,0)), (20, 50))
    if g_ovr:
        t1 = font.render("GAME OVER", True, (220, 50, 50))
        t2 = font.render("An 'R' de choi lai", True, (255, 255, 255))
        scr.blit(t1, (W//2 - t1.get_width()//2, H//2 - 30))
        scr.blit(t2, (W//2 - t2.get_width()//2, H//2 + 10))
    pygame.display.flip()
    clk.tick(60)
