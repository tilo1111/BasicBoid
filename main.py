from boid import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))

boid_list = pygame.sprite.Group()
display_list = pygame.sprite.LayeredDirty()

for i in range(40):
    boid = Boid(random.randint(1, WIDTH), random.randint(1, HEIGHT), max_v, fov, "boid1.png")
    boid_list.add(boid)
    display_list.add(boid)

clock = pygame.time.Clock()
running = True

display_list.clear(screen, background)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    text = "Boids Simulation by F.Jaszczyk & K.Kozieł"
    pygame.display.set_caption(text)

    for boid in boid_list:
        neighbours = []
        for boid2 in boid_list:
            if boid2 == boid:
                continue
            if boid.dist(boid2) < boid.fov:
                neighbours.append(boid2)

        boid.cohesion(neighbours)
        boid.alignment(neighbours)
        boid.separation(neighbours, min_dist)
        boid.update()

    tmp = display_list.draw(screen)
    pygame.display.update(tmp)
    clock.tick(60)

pygame.quit()
