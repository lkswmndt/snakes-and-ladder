import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
BOARD_SIZE = 10  # 10x10 board (100 squares)
SQUARE_SIZE = 60
BOARD_X = 50
BOARD_Y = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
DARK_GREEN = (0, 150, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Game setup
pygame.display.set_caption("Snakes & Ladders")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class SnakesAndLadders:
    def __init__(self):
        self.player_pos = 1
        self.animation_pos = 1
        self.target_pos = 1

        self.turns = 0
        self.state = "idle"   # idle, rolling, moving
        self.roll_timer = 0
        self.dice_roll = 1

        self.game_over = False

        self.ladders = {4: 14, 9: 31, 21: 42, 28: 84, 72: 91}
        self.snakes = {
            17: 7, 54: 34, 62: 19, 64: 60,
            87: 24, 93: 73, 95: 75, 98: 79
        }

    def roll_dice(self):
        return random.randint(1, 6)

    def start_roll(self):
        if self.state == "idle":
            self.state = "rolling"
            self.roll_timer = 20

    def get_position_coords(self, pos):
        if pos == 0:
            return BOARD_X + SQUARE_SIZE//2, BOARD_Y + 9*SQUARE_SIZE + SQUARE_SIZE//2

        row = (100 - pos) // 10
        col = (pos - 1) % 10

        if row % 2 == 0:
            col = 9 - col

        x = BOARD_X + col * SQUARE_SIZE + SQUARE_SIZE//2
        y = BOARD_Y + row * SQUARE_SIZE + SQUARE_SIZE//2
        return x, y
    
    def draw_board(self):
        # Draw squares
        for row in range(10):
            for col in range(10):
                x = BOARD_X + col * SQUARE_SIZE
                y = BOARD_Y + row * SQUARE_SIZE

                # Checker pattern
                color = WHITE if (row + col) % 2 == 0 else (220, 220, 220)
                pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

                pygame.draw.rect(screen, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE), 2)

        # Draw numbers (1–100)
        for pos in range(1, 101):
            x, y = self.get_position_coords(pos)
            text = small_font.render(str(pos), True, BLACK)
            screen.blit(text, (x - 10, y - 10))

        # Draw ladders
        for start, end in self.ladders.items():
            start_x, start_y = self.get_position_coords(start)
            end_x, end_y = self.get_position_coords(end)

            pygame.draw.line(screen, GREEN, (start_x, start_y), (end_x, end_y), 6)

        # Draw snakes (curvy)
        for start, end in self.snakes.items():
            start_x, start_y = self.get_position_coords(start)
            end_x, end_y = self.get_position_coords(end)

            points = []
            segments = 20
            for i in range(segments + 1):
                t = i / segments
                x = start_x + t * (end_x - start_x)
                y = start_y + t * (end_y - start_y) + 10 * math.sin(t * math.pi * 3)
                points.append((x, y))

            pygame.draw.lines(screen, RED, False, points, 6)
            pygame.draw.circle(screen, RED, (int(end_x), int(end_y)), 6)

    def draw_dice(self, x, y, roll=None):
        # Show random faces while rolling
        if self.state == "rolling":
            roll = random.randint(1, 6)

        # Dice background
        pygame.draw.rect(screen, WHITE, (x-40, y-40, 80, 80), border_radius=10)
        pygame.draw.rect(screen, BLACK, (x-40, y-40, 80, 80), 3, border_radius=10)

        # Dot positions
        dots = {
            1: [(x, y)],
            2: [(x-15, y-15), (x+15, y+15)],
            3: [(x-15, y-15), (x, y), (x+15, y+15)],
            4: [(x-15, y-15), (x-15, y+15), (x+15, y-15), (x+15, y+15)],
            5: [(x-15, y-15), (x-15, y+15), (x, y), (x+15, y-15), (x+15, y+15)],
            6: [(x-20, y-15), (x-20, y), (x-20, y+15),
                (x+20, y-15), (x+20, y), (x+20, y+15)]
        }

        # Draw dots
        if roll is not None:
            for dot in dots[roll]:
                pygame.draw.circle(screen, BLACK, dot, 6)

    def draw(self):
        print("DRAWING FRAME")
        screen.fill(DARK_GREEN)
        
        self.draw_board()

        # Draw player
        px, py = self.get_position_coords(self.animation_pos)
        pygame.draw.circle(screen, YELLOW, (int(px), int(py)), 20)
        pygame.draw.circle(screen, ORANGE, (int(px), int(py)), 20, 4)

        # Draw dice
        # 🎯 Only show UI when not moving
        if self.state != "moving":
            # 🎲 Dice box
            box_x = SCREEN_WIDTH // 2 - 100
            box_y = 400
            box_w = 200
            box_h = 150

            pygame.draw.rect(screen, (240, 240, 240), (box_x, box_y, box_w, box_h), border_radius=12)
            pygame.draw.rect(screen, BLACK, (box_x, box_y, box_w, box_h), 3, border_radius=12)

            # 🎲 Dice
            self.draw_dice(
                SCREEN_WIDTH // 2,
                box_y + box_h // 2 - 10,
                self.dice_roll if self.state != "rolling" else None
            )

            # 📝 Text
            if not self.game_over:
                instr1 = font.render("Click the dice to roll!", True, WHITE)
                instr2 = small_font.render(
                    f"Turn: {self.turns} | Position: {self.player_pos}", True, WHITE
                )

                screen.blit(instr1, (SCREEN_WIDTH//2 - instr1.get_width()//2, 550))
                screen.blit(instr2, (SCREEN_WIDTH//2 - instr2.get_width()//2, 600))

            else:
                win_text = font.render("🎉 YOU WON! 🎉", True, YELLOW)
                turns_text = small_font.render(
                    f"Completed in {self.turns} turns!", True, WHITE
                )

                screen.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, 300))
                screen.blit(turns_text, (SCREEN_WIDTH//2 - turns_text.get_width()//2, 350))

        pygame.display.flip()

    def update(self):
        if self.game_over:
            return

        # 🎲 Rolling phase
        if self.state == "rolling":
            self.roll_timer -= 1

            if self.roll_timer <= 0:
                self.dice_roll = self.roll_dice()
                self.target_pos = self.player_pos + self.dice_roll

                if self.target_pos > 100:
                    self.target_pos = self.player_pos

                self.animation_pos = self.player_pos
                self.state = "moving"

        # 🚶 Moving phase
        elif self.state == "moving":
            if self.animation_pos < self.target_pos:
                self.animation_pos += 1

            else:
                # Check snakes or ladders
                if self.animation_pos in self.ladders:
                    self.animation_pos = self.ladders[self.animation_pos]
                elif self.animation_pos in self.snakes:
                    self.animation_pos = self.snakes[self.animation_pos]

                self.player_pos = self.animation_pos
                self.turns += 1

                if self.player_pos == 100:
                    self.game_over = True

                self.state = "idle"

    def handle_click(self, pos):
        if self.game_over:
            self.__init__()
            return

        x, y = pos

        # Click dice
        if abs(x - SCREEN_WIDTH//2) < 80 and abs(y - 450) < 80:
            self.start_roll()

def main():
    game = SnakesAndLadders()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
        
        game.update()
        game.draw()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()