import pygame
import sys
import math

# --- Init ---
pygame.init()

# Raspberry Pi: use fullscreen or a fixed size
SCREEN_W, SCREEN_H = 800, 480
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Blink Eyes")

# --- Colors ---
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0)
SKIN       = (255, 220, 177)
IRIS_COLOR = (60,  100, 200)
PUPIL      = (20,  20,  20)
SHINE      = (255, 255, 255)
BROW_COLOR = (80,  50,  20)
LASH_COLOR = (30,  30,  30)

# --- Eye geometry parameters ---
EYE_RX   = 90   # horizontal radius of eye white (ellipse)
EYE_RY   = 70   # vertical radius
IRIS_R   = 42   # iris circle radius
PUPIL_R  = 22   # pupil radius
SHINE_R  = 9    # shine dot radius

# Eye centres
LEFT_EYE_X  = SCREEN_W // 2 - 160
RIGHT_EYE_X = SCREEN_W // 2 + 160
EYE_Y       = SCREEN_H // 2 + 10

eyes = [
    {"cx": LEFT_EYE_X,  "cy": EYE_Y, "blinking": False, "blink_t": 0.0},
    {"cx": RIGHT_EYE_X, "cy": EYE_Y, "blinking": False, "blink_t": 0.0},
]

BLINK_SPEED = 4.0   # full blink cycles per second (open→closed→open)


def draw_eyebrow(surface, cx, cy, flip=False):
    """Draw an arched eyebrow above the eye using a thick arc approximated by lines."""
    brow_y = cy - EYE_RY - 18
    brow_w = EYE_RX + 20
    pts = []
    steps = 30
    for i in range(steps + 1):
        t = i / steps          # 0..1
        angle = math.pi + t * math.pi  # 180° → 360° (bottom half of ellipse = arch)
        x = cx + brow_w * math.cos(angle)
        y = brow_y + 22 * math.sin(angle)
        pts.append((x, y))

    # Slight tilt: raise outer end, lower inner end (or flip for left)
    tilt = 12 if not flip else -12
    tilted = []
    for i, (x, y) in enumerate(pts):
        frac = i / steps  # 0 = inner, 1 = outer
        tilted.append((x, y - frac * tilt))

    pygame.draw.lines(surface, BROW_COLOR, False, tilted, 7)


def draw_eye(surface, eye, dt):
    cx, cy = eye["cx"], eye["cy"]

    # Advance blink animation
    if eye["blinking"]:
        eye["blink_t"] += dt * BLINK_SPEED
        if eye["blink_t"] >= 1.0:
            eye["blinking"] = False
            eye["blink_t"] = 0.0

    # blink_t: 0→0.5 closing, 0.5→1.0 opening
    t = eye["blink_t"]
    if t < 0.5:
        close_frac = t / 0.5        # 0 → 1  (eyelid descends)
    else:
        close_frac = (1.0 - t) / 0.5  # 1 → 0  (eyelid lifts)

    # --- Eye white ---
    eye_rect = pygame.Rect(cx - EYE_RX, cy - EYE_RY, EYE_RX * 2, EYE_RY * 2)
    pygame.draw.ellipse(surface, WHITE, eye_rect)
    pygame.draw.ellipse(surface, BLACK, eye_rect, 3)

    # --- Iris & pupil (only visible when not fully closed) ---
    if close_frac < 0.95:
        pygame.draw.circle(surface, IRIS_COLOR, (cx, cy), IRIS_R)
        # Subtle iris ring
        pygame.draw.circle(surface, (40, 70, 160), (cx, cy), IRIS_R, 4)
        pygame.draw.circle(surface, PUPIL, (cx, cy), PUPIL_R)
        # Shine highlight
        sx = cx - IRIS_R // 3
        sy = cy - IRIS_R // 3
        pygame.draw.circle(surface, SHINE, (sx, sy), SHINE_R)

    # --- Eyelid (top lid sweeps down) ---
    lid_height = int(EYE_RY * 2 * close_frac)
    if lid_height > 0:
        lid_rect = pygame.Rect(cx - EYE_RX - 2, cy - EYE_RY - 2,
                               EYE_RX * 2 + 4, lid_height + 2)
        # Clip to eye shape by drawing a filled ellipse the same size as the white
        # but only the top portion — we use a Surface with per-pixel alpha.
        lid_surf = pygame.Surface((EYE_RX * 2 + 4, EYE_RY * 2 + 4), pygame.SRCALPHA)
        lid_surf.fill((0, 0, 0, 0))
        pygame.draw.ellipse(lid_surf, (*SKIN, 255),
                            (0, 0, EYE_RX * 2 + 4, EYE_RY * 2 + 4))
        # Mask: keep only the top `lid_height` rows
        mask_rect = pygame.Rect(0, 0, EYE_RX * 2 + 4, lid_height + 2)
        clip_surf = lid_surf.subsurface(mask_rect).copy()
        surface.blit(clip_surf, (cx - EYE_RX - 2, cy - EYE_RY - 2))

    # --- Eyelashes (top) ---
    num_lashes = 9
    for i in range(num_lashes):
        frac = i / (num_lashes - 1)   # 0..1
        angle = math.pi + frac * math.pi  # 180°..360° = top arc
        # Base point on the ellipse
        bx = cx + EYE_RX * math.cos(angle)
        by = cy + EYE_RY * math.sin(angle)
        # Lash tip: slightly outward + curve with lid
        lash_len = 14 + 4 * math.sin(frac * math.pi)
        lash_angle = angle - math.pi / 2 - .85#0.15  # point slightly outward
        ex = bx + lash_len * math.cos(lash_angle)
        ey = by + lash_len * math.sin(lash_angle)
        # Droop lashes with lid
        droop = lid_height * 0.6
        pygame.draw.line(surface, LASH_COLOR, (int(bx), int(by + droop)),
                         (int(ex), int(ey + droop)), 2)

    # Redraw outline over lid/lashes
    pygame.draw.ellipse(surface, BLACK, eye_rect, 3)


def point_in_eye(px, py, eye):
    """Check if (px, py) is inside the eye ellipse."""
    dx = (px - eye["cx"]) / EYE_RX
    dy = (py - eye["cy"]) / EYE_RY
    return dx * dx + dy * dy <= 1.0


# --- Main loop ---
clock = pygame.time.Clock()

while True:
    dt = clock.tick(60) / 1000.0  # seconds since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Support both mouse clicks (dev) and finger touches (Pi touchscreen)
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
            if event.type == pygame.FINGERDOWN:
                # Finger coords are 0..1 normalised
                px = int(event.x * SCREEN_W)
                py = int(event.y * SCREEN_H)
            else:
                px, py = event.pos

            for eye in eyes:
                if point_in_eye(px, py, eye) and not eye["blinking"]:
                    eye["blinking"] = True
                    eye["blink_t"] = 0.0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    # --- Draw ---
    screen.fill(WHITE)

    for i, eye in enumerate(eyes):
        # Eyebrow: left eye flips tilt, right eye normal
        draw_eyebrow(screen, eye["cx"], eye["cy"], flip=(i == 0))
        draw_eye(screen, eye, dt)

    pygame.display.flip()
