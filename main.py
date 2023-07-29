import pygame
pygame.init()

screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Polyrhythm")

BLACK = (0, 0, 0)
YELLOW = (219, 172, 52)
WHITE = (255, 255, 255)

lines = []
line_spacing = 80
num_lines = 8
for i in range(num_lines):
    y_position = 100 + i * line_spacing
    lines.append((100, y_position, 1180, y_position))

circles = []
line_count = 0
for line in lines:
    line_count += 1
    x_center = line[0]
    y_center = line[1]
    circles.append([x_center, y_center, line_count * 75, 1])

pygame.mixer.init()
piano_sound = pygame.mixer.Sound('piano.wav')

clock = pygame.time.Clock()
running = True
paused = False
last_frame_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
                current_time = pygame.time.get_ticks()
                last_frame_time = current_time

    if paused:
        continue

    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - last_frame_time) / 1000.0
    last_frame_time = current_time

    screen.fill((0, 0, 0))

    for line in lines:
        pygame.draw.line(screen, WHITE, line[:2], line[2:], 2)
        pygame.draw.circle(screen, WHITE, line[:2], 5)
        pygame.draw.circle(screen, WHITE, line[2:], 5)

    for circle in circles:
        x, y, speed, direction = circle
        distance = speed * direction * elapsed_time
        x += distance
        if x <= lines[0][0] or x >= lines[0][2]:
            direction *= -1
            piano_sound.play()
            x = max(lines[0][0], min(x, lines[0][2]))  # Clamp x to the line endpoints
        circle[0] = x
        circle[3] = direction

        pygame.draw.circle(screen, YELLOW, (int(x), int(y)), 8)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()