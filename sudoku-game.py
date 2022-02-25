import sys
import pygame
import time

class Menu:
    def __init__(self, game):
        self.game = game
        self.height = 500
        self.width = 451
        self.easy = 'Easy'
        self.medium = 'Medium'
        self.hard = 'Hard'
        self.challenging = 'Challenging'
        self.running = True
        self.colors = {'white': (255, 255, 255), 'black': (0, 0, 0)}

    def menu(self):
        pygame.init()
        home = pygame.display.set_mode((self.width, self.height))
        home.fill(self.colors['white'])

        font = pygame.font.SysFont('Arial', 30)
        text = font.render("SUDOKU GAME", True, self.colors['black'])
        home.blit(text, (100, 50))

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()

            pygame.display.update()

class Sudoku:
    easy_board = [
        [0, 0, 0, 5, 0, 0, 8, 0, 0],
        [2, 5, 7, 0, 0, 0, 0, 4, 9],
        [0, 8, 0, 0, 0, 0, 0, 0, 1],
        [3, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 2, 9, 7, 0, 3, 0, 0, 0],
        [5, 0, 0, 0, 0, 8, 3, 0, 4],
        [0, 0, 2, 1, 0, 0, 0, 9, 0],
        [7, 4, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 6, 0, 8, 4, 7, 0, 3]
    ]

    def __init__(self):
        self.height = 500
        self.width = 451
        self.size = (self.width, self.height)
        self.running = True
        self.begin = True
        self.user_board = self.easy_board

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.green = (128, 255, 0)
        self.blue = (44, 130, 201)
        self.lemon_chiffon = (255, 250, 205)
    
    def start(self):
        pygame.init()
        pygame.display.set_caption('Sudoku')
        
        screen = pygame.display.set_mode(self.size)
        screen.fill(self.white)
        font = pygame.font.SysFont('Arial', 25)
        
        back_icon = pygame.image.load('media/back.png')
        back_icon = pygame.transform.smoothscale(back_icon, (50, 50))
        # pygame_logo = pygame.image.load('media/pygame-logo.png')
        # pygame_logo = pygame.transform.scale(pygame_logo, (120, 50))
        time_str = pygame.draw.rect(screen, self.white, (320, 10, 50, 40))
        time_text = font.render("Time - ", True, self.black)

        self.cubes = self.draw_board(screen, self.easy_board)

        screen.blit(back_icon, (0, 0))
        # screen.blit(pygame_logo, (150, 0))
        screen.blit(time_text, time_str)
        pygame.display.update()

        temp_x, temp_y = 0, 0
        t = Timer()
        t.start()

        while self.running:
            
            play_time = t.play_time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    temp_x, temp_y = self.mouse_click(screen, event, temp_x, temp_y)
                if event.type == pygame.KEYDOWN:
                    self.keyboard_key(screen, event, temp_x, temp_y, t, play_time)
            
            if self.begin: 
                t.timing(screen, play_time, font)
            else:
                play_time = t._stop_time
                t.timing(screen, play_time, font)

            pygame.display.update()

    
    def draw_board(self, screen, board):
        font = pygame.font.SysFont('Arial', 25)
        self.cubes = [[[] for _ in range(9)] for _ in range(9)]
        # Draw lines
        x = 0
        y = 50
        for i in range(10):
            if i % 3 == 0:
                pygame.draw.line(screen, self.black, (x, 50), (x, 500), 3)
                pygame.draw.line(screen, self.black, (0, y), (450, y), 3)
                x += 50
                y += 50
            else:
                pygame.draw.line(screen, self.black, (x, 50), (x, 500), 1)
                pygame.draw.line(screen, self.black, (0, y), (450, y), 1)
                x += 50
                y += 50

        # Fill in numbers
        r_left = 2
        r_top = 52
        for i in range(9):
            r_left = 2
            for j in range(9):
                if board[i][j] != 0:
                    position = pygame.draw.rect(screen, self.white, (r_left, r_top, 47, 47))
                    text = font.render(str(board[i][j]), True, self.black)
                    screen.blit(text, (position[0] + 15, position[1] + 8))
                else:
                    self.cubes[i][j] = Cube(47, 47, r_left, r_top, '')
                r_left += 50
            r_top += 50

        return self.cubes
        
    def mouse_click(self, screen, event, temp_x, temp_y):
        self.cubes[temp_y][temp_x].draw_cube(screen)
        current_left, current_top = event.pos[0], event.pos[1]
        x = (current_left // 50)
        y = ((current_top - 50) // 50)
        try:
            self.cubes[y][x].selected_cube(screen)
        except AttributeError:
            return 0, 0
        temp_x = x
        temp_y = y
        return temp_x, temp_y

    def keyboard_key(self, screen, event, temp_x, temp_y, timer, play_time):
        number = event.unicode
        if number in '123456789':
            self.cubes[temp_y][temp_x].value = number
            if self.is_valid(temp_y, temp_x, self.user_board, int(number)):
                self.cubes[temp_y][temp_x].update_cube_with_number(screen, number, self.lemon_chiffon)
                self.user_board[temp_y][temp_x] = int(number)
            else:
                print('wrong')
                self.cubes[temp_y][temp_x].wrong_number(screen)
        else:
            if event.key == pygame.K_BACKSPACE:
                self.cubes[temp_y][temp_x].update_cube_with_number(screen, '', self.white)
                self.user_board[temp_y][temp_x] = 0
            elif event.key == pygame.K_RETURN:
                self.begin = False
                timer.stop(play_time)
                self.solve(self.easy_board, screen)

    def is_valid(self, i, j, board, num):
        # check row
        for x in board[i]:
            if num == x:
                return False
        
        # check column
        for y in range(len(board)):
            if board[y][j] == num:
                return False
        
        # check 3x3 box
        box_x = (i // 3) * 3
        box_y = (j // 3) * 3
        for x in range(box_x, box_x + 3):
            for y in range(box_y, box_y + 3):
                if board[x][y] == num:
                    return False
        
        return True

    def findEmpty(self, board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    return i, j
        return None

    def solve(self, board, screen):
        found = self.findEmpty(board)
        if not found:
            return True
        i, j = found[0], found[1]

        for num in range(1, 10):
            if self.is_valid(i, j, board, num):
                board[i][j] = num
                self.cubes[i][j].auto_solve(screen, str(num))
                # time.sleep(0.2)
                if self.solve(board, screen):
                    return True
                board[i][j] = 0
                
        return False


class Cube:
    def __init__(self, width, height, left, top, value, color=(0, 0, 0), background_color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.value = value
        self.color = color
        self.background_color = background_color

    def draw_cube(self, screen):
        position = pygame.draw.rect(screen, self.background_color, (self.left, self.top, self.width, self.height))
        font = pygame.font.SysFont('Arial', 25)
        text = font.render(self.value, True, self.color)
        screen.blit(text, (position[0] + 15, position[1] + 8))
        pygame.display.update()

    def selected_cube(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.left + 1, self.top + 1, self.width - 2, self.height - 2), 3)
        pygame.display.update()

    def update_cube_with_number(self, screen, number, background_color):
        self.value = number
        self.color = (0, 0, 0)
        self.background_color = background_color
        position = pygame.draw.rect(screen, self.background_color, (self.left, self.top, self.width, self.height))
        font = pygame.font.SysFont('Arial', 25)
        text = font.render(number, True, self.color)
        screen.blit(text, (position[0] + 15, position[1] + 8))
        pygame.display.update()

    def wrong_number(self, screen):
        self.color = (255, 0, 0)
        position = pygame.draw.rect(screen, (255, 255, 255), (self.left, self.top, self.width, self.height))
        font = pygame.font.SysFont('Arial', 25)
        text = font.render(self.value, True, self.color)
        screen.blit(text, (position[0] + 15, position[1] + 8))
        pygame.display.update()

    def auto_solve(self, screen, number):
        self.value = number
        self.color = (0, 0, 0)
        position = pygame.draw.rect(screen, (128, 255, 0), (self.left, self.top, self.width, self.height))
        font = pygame.font.SysFont('Arial', 25)
        text = font.render(number, True, self.color)
        screen.blit(text, (position[0] + 15, position[1] + 8))
        pygame.display.update()


class Button:
    def __init__(self, name, screen, left, top, width, height):
        self.name = name
        self.screen = screen
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def build(self):
        position = pygame.draw.rect(self.screen, (255, 210, 0), (self.left, self.top, self.width, self.height))
        font = pygame.font.SysFont('Arial', 25)
        text = font.render(self.name, True, (0, 0, 0))
        self.screen.blit(text, position)
        pygame.display.update()
        

class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start the timer"""
        self._start_time = time.time()
        self._stop_time = None

    def play_time(self):
        return round(time.time() - self._start_time)

    def stop(self, current_time):
        """Stop the timer"""
        self._stop_time = current_time

    def format_time(self, t):
        second = t % 60
        minute = t // 60
        hour = minute / 60
        return " " + str(minute) + ": " + str(second)

    def timing(self, screen, play_time, font):
        position = pygame.draw.rect(screen, (255, 255, 255), (380, 10, 100, 35))
        text = font.render(self.format_time(play_time), True, (0, 0, 0))
        screen.blit(text, position)


if __name__ == "__main__":
    sudoku = Sudoku()
    sudoku.start()


    # home = Menu(Sudoku())
    # home.menu()