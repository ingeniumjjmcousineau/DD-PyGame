import pygame
import sys
import math

# --- Init ---
pygame.init()

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

# --- Eye geometry ---
EYE_RX  = 90
EYE_RY  = 70
IRIS_R  = 42
PUPIL_R = 22
SHINE_R = 9

LEFT_EYE_X  = SCREEN_W // 2 - 160
RIGHT_EYE_X = SCREEN_W // 2 + 160
EYE_Y       = SCREEN_H // 2 + 10

# Eye state machine:
#   state   : "open" | "closing" | "held" | "opening"
#   close_frac : 0.0 (fully open) to 1.0 (fully closed)
#   held_by : finger_id or mouse button that is holding this eye shut
eyes = [
    {"cx": LEFT_EYE_X,  "cy": EYE_Y, "state": "open", "close_frac": 0.0, "held_by": None},
    {"cx": RIGHT_EYE_X, "cy": EYE_Y, "state": "open", "close_frac": 0.0, "held_by": None},
]

LID_SPEED      = 8.0  # fractions per second (0->1 or 1->0)
ANGRY_DURATION = 2.0
angry_timer    = 0.0
angry_held     = False  # True while a finger is actively pressing an eye


def draw_eyebrow(surface, cx, cy, flip=False, angry_amount=0.0):
    brow_y = cy - EYE_RY - 18
    brow_w = EYE_RX + 20
    steps  = 30

    pts = []
    for i in range(steps + 1):
        t     = i / steps
        angle = math.pi + t * math.pi
        x     = cx + brow_w * math.cos(angle)
        y     = brow_y + 22 * math.sin(angle)
        pts.append((x, y))

    # Lerp between normal and angry values based on angry_amount (0.0=calm, 1.0=angry)
    normal_tilt = 12 if not flip else -12
    tilt        = normal_tilt + (50 - normal_tilt) * angry_amount
    inner_drop  = 10 * angry_amount

    tilted = []
    for i, (x, y) in enumerate(pts):
        frac = i / steps
        if flip:
            frac = 1 - frac
        # inner end (frac=0) drops by inner_drop; outer end (frac=1) rises by tilt
        y_offset = -inner_drop + (inner_drop + tilt) * frac
        tilted.append((x, y - y_offset))

    pygame.draw.lines(surface, BROW_COLOR, False, tilted, 7)


def draw_eye(surface, eye, dt):
    cx, cy = eye["cx"], eye["cy"]
    state  = eye["state"]

    # Advance lid animation
    if state == "closing":
        eye["close_frac"] = min(1.0, eye["close_frac"] + dt * LID_SPEED)
        if eye["close_frac"] >= 1.0:
            eye["state"] = "held"

    elif state == "opening":
        eye["close_frac"] = max(0.0, eye["close_frac"] - dt * LID_SPEED)
        if eye["close_frac"] <= 0.0:
            eye["state"] = "open"

    close_frac = eye["close_frac"]

    # Eye white
    eye_rect = pygame.Rect(cx - EYE_RX, cy - EYE_RY, EYE_RX * 2, EYE_RY * 2)
    pygame.draw.ellipse(surface, WHITE, eye_rect)
    pygame.draw.ellipse(surface, BLACK, eye_rect, 3)

    # Iris and pupil
    if close_frac < 0.95:
        pygame.draw.circle(surface, IRIS_COLOR, (cx, cy), IRIS_R)
        pygame.draw.circle(surface, (40, 70, 160), (cx, cy), IRIS_R, 4)
        pygame.draw.circle(surface, PUPIL, (cx, cy), PUPIL_R)
        pygame.draw.circle(surface, SHINE, (cx - IRIS_R // 3, cy - IRIS_R // 3), SHINE_R)

    # Eyelid
    lid_height = int(EYE_RY * 2 * close_frac)
    if lid_height > 0:
        lid_surf = pygame.Surface((EYE_RX * 2 + 4, EYE_RY * 2 + 4), pygame.SRCALPHA)
        lid_surf.fill((0, 0, 0, 0))
        pygame.draw.ellipse(lid_surf, (*SKIN, 255),
                            (0, 0, EYE_RX * 2 + 4, EYE_RY * 2 + 4))
        clip_surf = lid_surf.subsurface(
            pygame.Rect(0, 0, EYE_RX * 2 + 4, lid_height + 2)
        ).copy()
        surface.blit(clip_surf, (cx - EYE_RX - 2, cy - EYE_RY - 2))

    # Eyelashes -- only when fully open
    if state == "open":
        num_lashes = 9
        for i in range(num_lashes):
            frac  = i / (num_lashes - 1)
            angle = math.pi + frac * math.pi
            bx    = cx + EYE_RX * math.cos(angle)
            by    = cy + EYE_RY * math.sin(angle)
            lash_angle = math.atan2(by - cy, bx - cx)
            lash_len   = 14 + 4 * math.sin(frac * math.pi)
            ex = bx + lash_len * math.cos(lash_angle)
            ey = by + lash_len * math.sin(lash_angle)
            pygame.draw.line(surface, LASH_COLOR,
                             (int(bx), int(by)), (int(ex), int(ey)), 2)

    pygame.draw.ellipse(surface, BLACK, eye_rect, 3)


def point_in_eye(px, py, eye):
    dx = (px - eye["cx"]) / EYE_RX
    dy = (py - eye["cy"]) / EYE_RY
    return dx * dx + dy * dy <= 1.0


# --- Main loop ---
clock = pygame.time.Clock()

while True:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # --- Press / touch down ---
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
            if event.type == pygame.FINGERDOWN:
                px, py   = int(event.x * SCREEN_W), int(event.y * SCREEN_H)
                touch_id = event.finger_id
            else:
                px, py   = event.pos
                touch_id = event.button

            for eye in eyes:
                if point_in_eye(px, py, eye) and eye["state"] in ("open", "opening"):
                    eye["state"]   = "closing"
                    eye["held_by"] = touch_id
                    angry_held     = True

        # --- Release / touch up ---
        if event.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
            if event.type == pygame.FINGERUP:
                touch_id = event.finger_id
            else:
                touch_id = event.button

            for eye in eyes:
                if eye["held_by"] == touch_id and eye["state"] in ("closing", "held"):
                    eye["state"]   = "opening"
                    eye["held_by"] = None
                    angry_held     = False
                    angry_timer    = ANGRY_DURATION

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    if angry_timer > 0:
        angry_timer = max(0.0, angry_timer - dt)

    # Full angry while held; once released the timer drives the gradual return
    angry_amount = 1.0 if angry_held else min(angry_timer, 1.0)

    screen.fill(WHITE)
    for i, eye in enumerate(eyes):
        draw_eyebrow(screen, eye["cx"], eye["cy"], flip=(i == 0), angry_amount=angry_amount)
        draw_eye(screen, eye, dt)

    pygame.display.flip()