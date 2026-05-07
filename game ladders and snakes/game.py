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



QUESTIONS = [
    ("Ibukota Jepang?", "tokyo"),
    ("Planet terbesar?", "jupiter"),
    ("5*5=?", "25"),
    ("Siapa penemu lampu? (nama lengkap)", "thomas alva edison"),
    ("Sungai terpanjang di dunia?", "sungai nil")
]

class SnakesAndLadders:
    def __init__(self):
        self.players = [1, 1]
        self.current_player = 0
        self.animation_pos = 1
        self.target_pos = 1
        self.question_active = False
        self.current_question = None
        self.winner = None
        self.correct_answer = ""
        self.user_answer = ""
        self.question_tiles = [5, 12, 18, 26, 33, 41, 48, 57, 69, 76, 85]

        self.turns = 0
        self.state = "idle"   # idle, rolling, moving
        self.roll_timer = 0
        self.dice_roll = 1

        self.extra_turn = False
        self.extra_roll = False
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

        # Draw question tiles
        for pos in self.question_tiles:
            x, y = self.get_position_coords(pos)

            pygame.draw.circle(screen, PURPLE, (int(x), int(y)), 12)

            q_mark = small_font.render("?", True, WHITE)
            screen.blit(q_mark, (x - 5, y - 10))

        # Draw ladders
        for start, end in self.ladders.items():
            start_x, start_y = self.get_position_coords(start)
            end_x, end_y = self.get_position_coords(end)

            dx = end_x - start_x
            dy = end_y - start_y
            length = math.hypot(dx, dy)

            # arah tegak lurus
            offset_x = -dy / length * 10
            offset_y = dx / length * 10

            # sisi kiri tangga
            left_start = (start_x + offset_x, start_y + offset_y)
            left_end = (end_x + offset_x, end_y + offset_y)

            # sisi kanan tangga
            right_start = (start_x - offset_x, start_y - offset_y)
            right_end = (end_x - offset_x, end_y - offset_y)

            # rel tangga
            pygame.draw.line(screen, (139,69,19), left_start, left_end, 4)
            pygame.draw.line(screen, (139,69,19), right_start, right_end, 4)

            # anak tangga
            steps = 6
            for i in range(steps + 1):
                t = i / steps

                lx = left_start[0] + t * (left_end[0] - left_start[0])
                ly = left_start[1] + t * (left_end[1] - left_start[1])

                rx = right_start[0] + t * (right_end[0] - right_start[0])
                ry = right_start[1] + t * (right_end[1] - right_start[1])

                pygame.draw.line(screen, (160,82,45), (lx, ly), (rx, ry), 3)

        # Draw snakes
        for start, end in self.snakes.items():
            start_x, start_y = self.get_position_coords(start)
            end_x, end_y = self.get_position_coords(end)

            points = []
            segments = 30

            for i in range(segments + 1):
                t = i / segments

                x = start_x + t * (end_x - start_x)

                wave = math.sin(t * math.pi * 6) * 15
                y = start_y + t * (end_y - start_y) + wave

                points.append((x, y))

            # badan ular
            pygame.draw.lines(screen, (0,180,0), False, points, 10)

            # outline
            pygame.draw.lines(screen, BLACK, False, points, 2)

            # kepala ular
            head_x, head_y = points[0]

            pygame.draw.circle(screen, (0,220,0), (int(head_x), int(head_y)), 14)

            # mata
            pygame.draw.circle(screen, WHITE, (int(head_x - 4), int(head_y - 3)), 3)
            pygame.draw.circle(screen, WHITE, (int(head_x + 4), int(head_y - 3)), 3)

            pygame.draw.circle(screen, BLACK, (int(head_x - 4), int(head_y - 3)), 1)
            pygame.draw.circle(screen, BLACK, (int(head_x + 4), int(head_y - 3)), 1)

            # lidah
            pygame.draw.line(
                screen,
                RED,
                (head_x, head_y + 10),
                (head_x - 5, head_y + 18),
                2
            )

            pygame.draw.line(
                screen,
                RED,
                (head_x, head_y + 10),
                (head_x + 5, head_y + 18),
                2
            )

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

    def check_answer(self):
        if self.user_answer.lower() == self.correct_answer:
            # ✅ benar → boleh roll lagi
            self.extra_roll = True
        else:
            # ❌ salah → mundur
            penalty = random.randint(1, 6)
            self.players[self.current_player] = max(
                1,
                self.players[self.current_player] - penalty
            )
            self.extra_roll = False
            # ganti player
            self.current_player = 1 - self.current_player

        # tutup soal
        self.question_active = False
        self.user_answer = ""

        self.state = "idle"

    def draw(self):
        print("DRAWING FRAME")
        screen.fill(DARK_GREEN)
        
        self.draw_board()

        # Draw player
        for i, pos in enumerate(self.players):
            x, y = self.get_position_coords(pos)
            if i == 0:
                color = YELLOW 
            else: 
                color = BLUE
            pygame.draw.circle(screen, color, (int(x), int(y)), 15)

        # Draw dice
        # 🎯 Only show UI when not moving
        # 🎯 GAME OVER SCREEN

        if self.game_over:
            box_x = SCREEN_WIDTH // 2 - 180
            box_y = 250
            box_w = 360
            box_h = 200

            # Box
            pygame.draw.rect(screen, (30, 30, 30), (box_x, box_y, box_w, box_h), border_radius=15)
            pygame.draw.rect(screen, YELLOW, (box_x, box_y, box_w, box_h), 4, border_radius=15)

            # Text
            if self.winner == 0:
                win_text = font.render("Player 1 Menang!", True, YELLOW)
            else:
                win_text = font.render("Player 2 Menang!", True, BLUE)

            turns_text = small_font.render(
                f"Selesai dalam {self.turns} putaran!", True, WHITE
            )
            restart_text = small_font.render("Klik apapun untuk mengulang", True, WHITE)

            screen.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, box_y + 40))
            screen.blit(turns_text, (SCREEN_WIDTH//2 - turns_text.get_width()//2, box_y + 90))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, box_y + 130))

            pygame.display.flip()
            return
        
        elif self.question_active:
            box_x = SCREEN_WIDTH // 2 - 200
            box_y = 200
            box_w = 400
            box_h = 200

            pygame.draw.rect(screen, (20,20,20), (box_x, box_y, box_w, box_h), border_radius=15)
            pygame.draw.rect(screen, WHITE, (box_x, box_y, box_w, box_h), 3, border_radius=15)

            q_text = small_font.render(self.current_question, True, WHITE)
            a_text = small_font.render(self.user_answer, True, YELLOW)

            screen.blit(q_text, (box_x + 20, box_y + 40))
            screen.blit(a_text, (box_x + 20, box_y + 100))


        # 🎲 NORMAL UI (only when not moving AND not game over)
        elif self.state != "moving" and not self.question_active:

            box_x = SCREEN_WIDTH // 2 - 140
            box_y = 380
            box_w = 280
            box_h = 180

            pygame.draw.rect(screen, (30, 30, 30), (box_x, box_y, box_w, box_h), border_radius=15)
            pygame.draw.rect(screen, WHITE, (box_x, box_y, box_w, box_h), 3, border_radius=15)

            # Dice
            self.draw_dice(
                SCREEN_WIDTH // 2,
                box_y + 70,
                self.dice_roll if self.state != "rolling" else None
            )

            # Text
            instr1 = font.render("Klik untuk putar dadu", True, WHITE)
            instr2 = small_font.render(
                f"Giliran: {self.turns} P{self.current_player+1}:{self.players[self.current_player]}", True, WHITE)
            credit_text = font.render("Dibuat oleh Kelompok ", True, WHITE)

            screen.blit(instr1, (SCREEN_WIDTH//2 - instr1.get_width()//2, box_y + 110))
            screen.blit(instr2, (SCREEN_WIDTH//2 - instr2.get_width()//2, box_y + 140))
            screen.blit(credit_text, (SCREEN_WIDTH//2 - credit_text.get_width()//2, 650))

        pygame.display.flip()

    def update(self):
        if self.game_over:
            return

        # 🎲 Rolling phase
        if self.state == "rolling":
            self.roll_timer -= 1

            if self.roll_timer <= 0:
                self.dice_roll = self.roll_dice()
                self.target_pos = self.players[self.current_player] + self.dice_roll

                if self.target_pos > 100:
                    self.target_pos = self.players[self.current_player]

                self.animation_pos = self.players[self.current_player]
                self.state = "moving"

        # 🚶 Moving phase
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

                # simpan posisi player
                self.players[self.current_player] = self.animation_pos

                # ✅ CEK MENANG DULU
                if self.players[self.current_player] >= 100:
                    self.players[self.current_player] = 100

                    self.game_over = True
                    self.winner = self.current_player

                    # hentikan semua state
                    self.state = "idle"
                    self.question_active = False
                    self.extra_roll = False

                    return

                # =========================
                # kalau belum menang
                # =========================

                # kalau jawaban benar sebelumnya
                if self.extra_roll:
                    self.extra_roll = False
                    self.state = "idle"

                else:
                    # cek apakah injak question tile
                    if self.players[self.current_player] in self.question_tiles:

                        self.question_active = True
                        self.current_question, self.correct_answer = random.choice(QUESTIONS)

                    else:
                        # langsung ganti player kalau bukan question tile
                        self.current_player = 1 - self.current_player

                    self.turns += 1
                    self.state = "idle"

    def handle_click(self, pos):
        if self.game_over:
            self.__init__()
            return
        
        if self.question_active:
            return

        x, y = pos

        # Click dice
        box_x = SCREEN_WIDTH // 2 - 140
        box_y = 380
        box_w = 280
        box_h = 180

        if (box_x < x < box_x + box_w and box_y < y < box_y + box_h):
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
            elif event.type == pygame.KEYDOWN:
                if game.question_active:
                    if event.key == pygame.K_RETURN:
                        game.check_answer()
                    elif event.key ==pygame.K_BACKSPACE:
                        game.user_answer = game.user_answer[:-1]
                    else:
                        game.user_answer += event.unicode
        
        game.update()
        game.draw()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()