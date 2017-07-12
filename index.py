# coding: utf-8
# Damas
# (C) 2017, Jadson Luan / UFCG, Lab. de Programação I

import pygame, sys
from pygame.locals import *

# CONSTANTS
HELP, START, QUIT = 1, 2, 3
SHOW_MENU, MATCH_RUNNING, SHOW_MANUAL, GAMEOVER = 1, 2, 3, 4
BLOCKED, FREE, BLACK, BLACK_KING, WHITE, WHITE_KING = "X", " ", "b", "B", "w", "W"
SUGGESTED, MOVEABLE, NOT_MOVEABLE, KING = "S", "M", "NM", "K"

cell_size = 60

direction = {}
direction[BLACK], direction[WHITE] = 1, -1

colors = {}
colors[BLACK] = (25,25,25)
colors[WHITE] =  (229,229,229)
colors[BLOCKED] = (255,230,128)
colors[FREE] = (79,44,29)
colors[SUGGESTED] = (0,174,49)
colors[NOT_MOVEABLE] = (255,3,0)
colors[MOVEABLE] = (0,174,49)
colors[KING] = (6,233,154)

offset_row_cell, offset_col_cell = 1, 3

# Helper functions
def is_valid_cell(row, col):
    return (row % 2 == 0 and col % 2 != 0) or (row % 2 != 0 and col % 2 == 0)

def get_opponent(player):
    return WHITE if player == BLACK else BLACK

# Classes
class Game:
    def __init__(self):
        pygame.init()

    def start(self):
        self.create_screen()
        self.gamestate = SHOW_MENU
        self.menu_options = {}
        self.show_menu()
        self.loop()

    def create_screen(self):
        pygame.display.set_caption("Damas em Python")
        width = cell_size * 14
        height = cell_size * 10
        self.screen_size = width, height # cell size * cell per line + offset
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

    def start_match(self):
        self.checkers = Checkers(self.screen, WHITE) # the 2nd parameter is who starts

    def text_objects(self, text, color, font):
        surface = font.render(text, True, color)
        return surface, surface.get_rect()

    def display_message(self, text, location, fontname, size, color, bold=False, center=True):
        font = pygame.font.SysFont(fontname, size, bold)
        text_surface, text_rect = self.text_objects(text, color, font)
        if center:
            text_rect.center = location
            self.screen.blit(text_surface, text_rect)
            return text_surface, text_rect
        else:
            self.screen.blit(text_surface, location)

    def show_menu(self):
        screen = self.screen
        width, height = self.screen_size
        screen.fill((0,87,68))

        top_offset = 225
        self.display_message("Damas", (width/2, top_offset), "Verdana", 50, (150,150,154), True)

        top_offset += 50
        msg = self.display_message("Iniciar", (width/2, top_offset), "comic-sans", 30, (215,215,220))
        self.menu_options[START] = msg

        top_offset += 25
        msg = self.display_message("Como jogar", (width/2, top_offset), "comic-sans", 30, (215,215,220))
        self.menu_options[HELP] = msg

        top_offset += 25
        msg = self.display_message("Sair", (width/2, top_offset), "comic-sans", 30, (215,215,220))
        self.menu_options[QUIT] = msg

        self.display_message("Criado por: Jadson Luan", (width/2, height - 30), "roboto", 30, (255,215,0))

        pygame.display.flip()

    def show_help(self):
        screen = self.screen
        width, height = self.screen_size
        screen.fill((30,29,29))

        top_offset = 40
        self.display_message("Manual", (20, top_offset), "Verdana", 100, (150,150,154), True, False)

        dica1 = u"1. A pedra (peça comum) anda só para frente, uma casa de cada vez."
        dica2 = u"2. Quando a pedra atinge a oitava linha do tabuleiro ela é promovida à dama."
        dica3 = u"3. A dama anda para frente e para trás, quantas casas quiser."
        dica4 = u"4. A dama não pode saltar uma peça da mesma cor."
        dica5 = u"5. Duas ou mais peças juntas, na mesma diagonal, não podem ser capturadas."
        dica6 = u"6. A pedra e a dama podem capturar tanto para frente como para trás, uma ou mais peças."
        dica7 = u"7. Uma pedra só será coroada se no fim do turno ela estiver posicionada numa casa de coroação."
        dica8 = u"8. A captura é obrigatória."
        dica9 = u"9. A vitória é obtida se o adversário não possuir mais peças ou jogadas possíveis."

        dica10 = u"Se ao clicar em uma peça, a casa que ela está posicionada ficar vermelha, ela não pode se mover."
        dica11 = u"Motivos: Não há jogadas possíveis OU você possui tomada(s) obrigatória(s) com outra(s) peça(s)."

        hint_color, hint_size = (255,255,255), 25
        left_offset = 30
        top_offset += 130
        self.display_message(dica1, (left_offset, top_offset), "roboto", hint_size, hint_color, False, False)

        top_offset += 30
        self.display_message(dica2, (left_offset, top_offset), "roboto", hint_size, hint_color, False, False)

        top_offset += 30
        self.display_message(dica3, (left_offset, top_offset), "roboto", hint_size, hint_color, False, False)

        top_offset += 30
        self.display_message(dica4, (left_offset, top_offset), "roboto", hint_size, hint_color, False, False)

        top_offset += 30
        self.display_message(dica5, (left_offset, top_offset), "roboto", hint_size, hint_color, False, False)

        top_offset += 30
        self.display_message(dica6, (left_offset, top_offset), "roboto", hint_size, hint_color, False, False)

        top_offset += 30
        self.display_message(dica7, (left_offset, top_offset), "roboto", hint_size, hint_color, False, False)

        top_offset += 30
        self.display_message(dica8, (left_offset, top_offset), "roboto", hint_size, hint_color, False, False)

        top_offset += 30
        self.display_message(dica9, (left_offset, top_offset), "roboto", hint_size, hint_color, False, False)

        top_offset += 60
        self.display_message(dica10, (left_offset, top_offset), "roboto", hint_size, (111,200,223), False, False)

        top_offset += 30
        self.display_message(dica11, (left_offset, top_offset), "roboto", hint_size, (111,200,223), False, False)

        self.display_message(u"Pressione 'ESC' para retornar ao menu", (width/2, height - 30), "comic-sans", 30, (150,150,154), False)

        pygame.display.flip()

    def loop(self):
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and (self.gamestate == SHOW_MANUAL or self.gamestate == GAMEOVER) and event.key == K_ESCAPE:
                    self.gamestate = SHOW_MENU
                    self.show_menu()

            if self.gamestate == SHOW_MENU:
                left_click, middle_click, right_click = pygame.mouse.get_pressed()

                if left_click:
                    for key in self.menu_options:
                        option = self.menu_options[key]
                        surface, rect = option

                        if rect.collidepoint(pygame.mouse.get_pos()):
                            if key == START:
                                self.start_match()
                                self.gamestate = MATCH_RUNNING
                            elif key == HELP:
                                self.show_help()
                                self.gamestate = SHOW_MANUAL
                            elif key == QUIT:
                                sys.exit(0)
            elif self.gamestate == MATCH_RUNNING:
                current_player = self.checkers.current_player
                checkers = self.checkers

                pieces_b = len(checkers.get_pieces(BLACK))
                pieces_w = len(checkers.get_pieces(WHITE))

                moveables_b = len(checkers.get_moveable_cells(BLACK))
                moveables_w = len(checkers.get_moveable_cells(WHITE))

                if pieces_w <= 0:
                    self.gamestate = GAMEOVER
                    self.win("pretas", u"peças")
                    continue
                elif pieces_b <= 0:
                    self.gamestate = GAMEOVER
                    self.win("brancas", u"peças")
                    continue
                elif checkers.current_player == WHITE and moveables_w <= 0:
                    self.gamestate = GAMEOVER
                    self.win("pretas", u"jogadas")
                    continue
                elif checkers.current_player == BLACK and moveables_b <= 0:
                    self.gamestate = GAMEOVER
                    self.win("brancas", u"jogadas")
                    continue

                left_click, middle_click, right_click = pygame.mouse.get_pressed()

                if left_click:
                    pos = pygame.mouse.get_pos()
                    checkers = self.checkers
                    board = self.checkers.board

                    for row in range(len(board)):
                        for col in range(len(board[row])):
                            cell = board[row][col]
                            if cell.rect.collidepoint(pos):
                                if cell.has_piece():
                                    moveables_b = len(checkers.get_moveable_cells())
                                    checkers.select_cell(cell)
                                elif not cell.has_piece() and checkers.selected:
                                    if checkers.can_move(checkers.selected, cell):
                                        checkers.move(cell)
                                break
                self.render(self.screen)
                
    def render(self, screen):
        '''
        Renderiza o jogo a cada iteração do gameloop
        '''
        screen.fill((30,29,29))
        width, height = self.screen_size
        current_player = self.checkers.current_player
        checkers = self.checkers
        str_player = "pretas" if current_player == BLACK else "brancas"
        black_color, white_color = (0,174,136) , (229,247,243) 

        surf_color = (50,49,49)  	

        left_surface = pygame.Surface([offset_col_cell * cell_size, height - (2 * cell_size * offset_row_cell)])
        left_surface.fill(surf_color)
        self.screen.blit(left_surface, (0,cell_size * offset_row_cell))

        right_surface = pygame.Surface([offset_col_cell * cell_size, height - (2 * cell_size * offset_row_cell)])
        right_surface.fill(surf_color)
        self.screen.blit(right_surface, (width - offset_col_cell * cell_size, cell_size * offset_row_cell))

        player_color = white_color if current_player == WHITE else black_color
        self.display_message(u"Turno do jogador de peças %s" % str_player, (width/2, 30), "roboto", 30, player_color)
        
        self.display_message(u"Peças brancas", (10, (height/2) - cell_size/2), None, 25, white_color, True, False)
        self.display_message(u"Peças em jogo: %d" % len(checkers.get_pieces(WHITE)), (25, height/2), None, 20, white_color, False, False)
        self.display_message(u"Jogadas: %d" % checkers.white_moviments, (25, (height/2) + 20), None, 20, white_color, False, False)

        self.display_message(u"Peças pretas", (cell_size * 11 + 10, (height/2) - cell_size/2), None, 25, black_color, True, False)
        self.display_message(u"Peças em jogo: %d" % len(checkers.get_pieces(BLACK)), (cell_size * 11 + 25, height/2), None, 20, black_color, False, False)
        self.display_message(u"Jogadas: %d" % checkers.black_moviments, (cell_size * 11 + 25, (height/2) + 20), None, 20, black_color, False, False)

        self.checkers.render()
        pygame.display.flip()

    def win(self, winner, reason):
        width, height = self.screen_size
        screen = self.screen
        screen.fill((0,117,73))

        top_offset = 200
        self.display_message(u"Fim de jogo", (width/2, top_offset), "comic-sans", 80, (115,222,158))

        top_offset += 50
        self.display_message(u"O jogador de peças %s venceu!" % winner, (width/2, top_offset), "comic-sans", 30, (255,255,255))

        top_offset += 25
        self.display_message(u"O seu oponente não possui mais %s!" % reason, (width/2, top_offset), "comic-sans", 30, (255,255,255))

        self.display_message(u"Pressione 'ESC' para retornar ao menu", (width/2, height - 30), "comic-sans", 30, (150,150,154), False)

        pygame.display.flip()

class Checkers:
    '''
    Responsável por manipular o tabuleiro
    '''
    def __init__(self, screen, turn):
        self.screen = screen
        self.jumping = False
        self.current_player = turn
        self.black_moviments, self.white_moviments = 0, 0
        self.set_up_board()
        self.draw()

    def set_up_board(self):
        self.selected = None
        self.board = []
        board = self.board

        for row in range(8):
            board.append([])
            for col in range(8):
                board_pos = (row, col)
                cell = Cell(board_pos)
                board[row].append(cell)

        self.set_up_players(self.board)

    def set_up_players(self, board):
        for row in range(3):
            for col in range(len(board[row])):
                if is_valid_cell(row, col):
                    board[row][col].piece = Piece(BLACK)

                if is_valid_cell(row-3, col):
                    board[row-3][col].piece = Piece(WHITE)

    def render(self):
        '''
        Renders the board on the screen based on 'board' attribute (matrix)
        '''
        board = self.board
        for row in range(len(board)):
            for col in range(len(board[row])):
                cell = board[row][col]
                self.screen.blit(cell.image, cell.rect)

    def draw(self):
        '''
        Draw the board on the screen based in 'c_type' attribute from each 'Cell'
        present on 'board' attribute from this class.
        '''
        screen = self.screen
        board = self.board
        for row in range(len(board)):
            for col in range(len(board[row])):
                cell = board[row][col]
                cell.update_image()
                self.screen.blit(cell.image, cell.rect)

    def select_cell(self, cell, still_jumping=False):
        if not self.jumping or (self.jumping and still_jumping):
            self.selected = None
            board = self.board
            owns_cell = cell.piece.player == self.current_player
            if cell.has_piece():
                if owns_cell:
                    self.draw() # clean the highlighted cells
                    if cell in self.get_moveable_cells():
                        cell.highlight(True)
                        self.selected = cell

                        cells = self.get_moves(cell)

                        opponent = WHITE if self.current_player == BLACK else BLACK

                        for adj_cell in cells:
                            if not adj_cell.has_piece():
                                adj_cell.suggest()
                        return
                    else:
                        cell.highlight(False)
                        return
                else:
                    pass
                    #print "Player %s, this is not your piece." % self.current_player

            self.draw()

    def get_adjacents(self, cell):
        '''
        Takes a cell and returns the adjacents cells
        '''
        row, col = cell.board_pos
        board = self.board
        cells = []
        if cell.piece.is_king:
            # se tiver uma peça aliada na diagonal, parar de sugerir celulas apos ela
            # ja que a dama não pode pular por cima de suas proprias peças
            row_plus_col_plus = True
            row_plus_col_minus = True
            row_minus_col_plus = True
            row_minus_col_minus = True

            for i in range(1, len(board)):
                if row + i < len(board):
                    if col + i < len(board[row]) and row_plus_col_plus:
                        next_cell = board[row+i][col+i]
                        if next_cell.has_piece() and next_cell.piece.player == cell.piece.player:
                            row_plus_col_plus = False
                        else:
                            cells.append(next_cell)
                    if col - i >= 0 and row_plus_col_minus:
                        next_cell = board[row+i][col-i]
                        if next_cell.has_piece() and next_cell.piece.player == cell.piece.player:
                            row_plus_col_minus = False
                        else:
                            cells.append(next_cell)
                if row - i >= 0:
                    if col + i < len(board[row]) and row_minus_col_plus:
                        next_cell = board[row-i][col+i]
                        if next_cell.has_piece() and next_cell.piece.player == cell.piece.player:
                            row_minus_col_plus = False
                        else:
                            cells.append(next_cell)
                    if col - i >= 0 and row_minus_col_minus:
                        next_cell = board[row-i][col-i]
                        if next_cell.has_piece() and next_cell.piece.player == cell.piece.player:
                            row_minus_col_minus = False
                        else:
                            cells.append(next_cell)
        else:
            # adj_row = row + direction[cell.piece.player]
            if row + 1 < len(board):
                if col + 1 < len(board[row]):
                    cells.append(board[row+1][col+1])
                if col - 1 >= 0:
                    cells.append(board[row+1][col-1])
            if row - 1 >= 0:
                if col + 1 < len(board[row]):
                    cells.append(board[row-1][col+1])
                if col - 1 >= 0:
                    cells.append(board[row-1][col-1])

        # remove the cells that the player owners
        for i in range(len(cells) - 1, -1, -1):
            if cells[i].has_piece() and cell.piece.player == cells[i].piece.player:
                cells.pop(i)
        return cells

    def get_pieces(self, player=None):
        if player is None:
            player = self.current_player

        pieces = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                cell = self.board[row][col]
                if cell.has_piece() and cell.piece.player == player:
                    pieces.append(cell)
        return pieces

    def is_jump(self, origin, destiny):
        if origin.has_piece() and not destiny.has_piece():
            origin_row, origin_col = origin.board_pos
            destiny_row, destiny_col = destiny.board_pos
            distance = abs(destiny_row - origin_row)

            if distance >= 2:
                if origin.piece.is_king:
                    row_dir = 1 if destiny_row - origin_row >= 0 else -1
                    col_dir = 1 if destiny_col - origin_col >= 0 else -1

                    enemies_between = 0
                    for n in range(1, distance):
                        middle_row = origin_row + n * row_dir
                        middle_col = origin_col + n * col_dir
                        middle_cell = self.board[middle_row][middle_col]

                        # Se houver uma peça entre a origem e o destino
                        if middle_cell.has_piece():
                            # E a peça for do oponente, incrementa um no número de inimigos entre a origem e o destino
                            if middle_cell.piece.player == get_opponent(self.current_player):
                                enemies_between += 1
                            # Se a peça for aliada, o pulo não é possível
                            else:
                                return False
                    # Só é um pulo se o número de inimigos entre a origem e o destino for igual a 1
                    return enemies_between == 1
                else:
                    return distance == 2

        return False

    def has_jumpable_cell(self, pieces):
        for piece in pieces:
            moves = self.get_moves(piece)
            origin_row, origin_col = piece.board_pos
            for move in moves:
                destiny_row, destiny_col = move.board_pos
                if self.is_jump(piece, move):
                    return True
        return False

    def get_jumpable_cells(self, pieces, player=None):
        if player is None:
            player = self.current_player

        jumpable = []
        if self.has_jumpable_cell(pieces):
            for piece in pieces:
                moves = self.get_moves(piece, player)
                origin_row, origin_col = piece.board_pos
                for move in moves:
                    destiny_row, destiny_col = move.board_pos
                    if self.is_jump(piece, move):
                        jumpable.append(piece)
                        break

        return jumpable

    def get_moveable_cells(self, player=None):
        if player is None:
            player = self.current_player

        pieces = self.get_pieces(player)
        moveable = []

        jumpables_cells = self.get_jumpable_cells(pieces, player)

        if jumpables_cells == []:
            for piece in pieces:
                moves = self.get_moves(piece, player)

                if moves == []:
                    continue

                moveable.append(piece)
        else:
            moveable = jumpables_cells

        return moveable

    def can_jump(self, origin, target):
        '''
        Analisa se é possível realizar um "pulo" (ou comer) a celula 'target'
        partindo da celula 'origin'
        '''
        board = self.board
        if origin.has_piece() and target.has_piece():
            if origin.piece.is_king:
                origin_r, origin_c = origin.board_pos
                target_r, target_c = target.board_pos

                distance = abs(origin_r - target_r)
                dir_r = -1 if target_r - origin_r < 0 else 1
                dir_c = -1 if target_c - origin_c < 0 else 1

                for i in range(1, distance):
                    middle_r = origin_r + dir_r * i
                    middle_c = origin_c + dir_c * i
                    middle_cell = board[middle_r][middle_c]

                    if middle_cell.has_piece():
                        return False

                next_r = origin_r + dir_r * (distance + 1)
                next_c = origin_c + dir_c * (distance + 1)
                row_onboard = next_r >= 0 and next_r < len(board)
                col_onboard = next_c >= 0 and next_c  < len(board[0])

                if row_onboard and col_onboard:
                    next_cell = board[next_r][next_c]
                    return not next_cell.has_piece()
            else:
                origin_r, origin_c = origin.board_pos
                target_r, target_c = target.board_pos

                if abs(origin_r - target_r) == 1:
                    dir_r = target_r - origin_r
                    dir_c = target_c - origin_c

                    next_r = origin_r + dir_r * 2
                    next_c = origin_c + dir_c * 2

                    row_onboard = next_r >= 0 and next_r < len(board)
                    col_onboard = next_c >= 0 and next_c < len(board[0])
                    distance = abs(origin_r - next_r)

                    if row_onboard and col_onboard and distance == 2:
                        next_cell = board[next_r][next_c]
                        return not next_cell.has_piece()

        return False

    def can_go_to(self, origin, destiny):
        '''
        Se é possível  da cell 'origin' para a cell 'destiny'
        '''
        destiny_row, destiny_col = destiny.board_pos
        origin_row, origin_col = origin.board_pos
        # Não permitir pulos que deêm a volta no tabuleiro
        distance = abs(destiny_row - origin_row)
        dir_col = 1 if destiny_col - origin_col >= 0 else -1
        dir_row = 1 if destiny_row - origin_row >= 0 else -1

        if origin.piece.is_king:
            num_opponents_between = 0
            for i in range(distance):
                cell = self.board[origin_row + dir_row * i][origin_col + dir_col * i]
                player = origin.piece.player
                if cell.has_piece() and get_opponent(player) == cell.piece.player:
                    num_opponents_between += 1

            if num_opponents_between <= 1:
                return True
        else:
            if direction[origin.piece.player] == dir_row:
                if distance == 2:
                    jumped_row = (origin_row + destiny_row) / 2
                    jumped_col = (origin_col + destiny_col) / 2
                    jumped_cell = self.board[jumped_row][jumped_col]

                    if self.can_jump(origin, jumped_cell):
                        return True
                    else:
                        return False
                elif distance == 1:
                    return not destiny.has_piece()

        return False

    def get_moves(self, origin, player=None):
        '''
        Retorna uma lista com as celulas que a celula 'origin' pode se mover.
        '''
        if player is None:
            player = self.current_player

        board = self.board
        opponent = get_opponent(player)
        movements = []

        if origin.has_piece():
            cells = self.get_adjacents(origin)
            has_jump_movement = False

            for cell in cells:
                if cell.has_piece() and cell.piece.player == opponent and self.can_jump(origin, cell):
                    has_jump_movement = True

            if has_jump_movement:
                if origin.piece.is_king:
                    for cell in cells:
                        if self.can_jump(origin, cell):
                            destiny_row, destiny_col = cell.board_pos
                            origin_row, origin_col = origin.board_pos

                            row_direction = 1 if destiny_row - origin_row >= 0 else -1
                            col_direction = 1 if destiny_col - origin_col >= 0 else -1

                            for i in range(1, 8):
                                next_row = destiny_row + row_direction * i
                                next_col = destiny_col + col_direction * i

                                on_rows = next_row >= 0 and next_row < len(board)
                                on_cols = next_col >= 0 and next_col < len(board[0])

                                if on_rows and on_cols:
                                    next_cell = board[next_row][next_col]

                                    if next_cell.has_piece():
                                        break

                                    movements.append(next_cell)

                else:
                    for cell in cells:
                        if self.can_jump(origin, cell):
                            destiny_row, destiny_col = cell.board_pos
                            origin_row, origin_col = origin.board_pos

                            row_direction = 1 if destiny_row - origin_row >= 0 else -1
                            col_direction = 1 if destiny_col - origin_col >= 0 else -1

                            next_row = origin_row + row_direction * 2
                            next_col = origin_col + col_direction * 2

                            next_cell = board[next_row][next_col]
                            movements.append(next_cell)
            else:
                for i in range(len(cells) - 1, -1, -1):
                    if self.can_go_to(origin, cells[i]):
                        movements.append(cells[i])

        return movements

    def can_move(self, origin, destiny):
        return destiny in self.get_moves(origin)

    def move(self, destiny):
        '''
        Realiza um movimento da peça selecionada (self.selected) para a celula parâmetro 'destiny'
        '''
        selected = self.selected
        current_row, current_col = self.selected.board_pos
        destiny_row, destiny_col = destiny.board_pos
        jumped = False

        distance = abs(current_row - destiny_row)
        if distance >= 2:
            # only for non-king pieces
            if not selected.piece.is_king:
                jumped_row = (current_row + destiny_row) / 2
                jumped_col = (current_col + destiny_col) / 2
                jumped_cell = self.board[jumped_row][jumped_col]

                if self.can_jump(selected, jumped_cell):
                    jumped_cell.piece = None
                    jumped = True
                    self.jumping = True
                else:
                    print "Esse pulo não é possível!"
                    return
            # for kings
            else:
                if self.can_go_to(selected, destiny):
                    for i in range(distance):
                        dir_row = 1 if destiny_row - current_row >= 0 else -1
                        dir_col = 1 if destiny_col - current_col >= 0 else -1
                        jumped_row = current_row + dir_row * i
                        jumped_col = current_col + dir_col * i
                        jumped_cell = self.board[jumped_row][jumped_col]
                        player = selected.piece.player
                        if jumped_cell.has_piece() and get_opponent(player) == jumped_cell.piece.player:
                            if self.can_jump(selected, jumped_cell):
                                jumped_cell.piece = None
                                jumped = True
                                self.jumping = True
                            else:
                                print "Esse pulo não é possível!"
                                return

        onboard = destiny_row in [0, len(self.board) - 1]
        is_not_king = not selected.piece.is_king

        if direction[selected.piece.player] == -1:
            is_crowned_row = destiny_row == 0
        else:
            is_crowned_row = destiny_row == 7

        destiny.piece = selected.piece
        selected.piece = None
        selected = destiny
        self.draw()

        still_have_jump = self.has_jumpable_cell([selected])

        if still_have_jump:
            if jumped:
                self.select_cell(selected, True)
                return
            
        if is_crowned_row:
            selected.piece.is_king = True

        if self.current_player == WHITE:
            self.white_moviments += 1
        else:
            self.black_moviments += 1

        self.jumping = False
        self.current_player = WHITE if self.current_player == BLACK else BLACK

class Cell(pygame.sprite.Sprite):
    '''
    Modelo para a celula
    '''
    def __init__(self, board_pos, piece=None):
        pygame.sprite.Sprite.__init__(self)
        self.board_pos = board_pos
        self.piece = piece
        self.update_image()
        row, col = board_pos
        location = cell_size * (col + offset_col_cell), cell_size * (row + offset_row_cell)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location

    def draw_cell(self):
        row, col = self.board_pos

        if (col % 2 == 0 and row % 2 == 0) or (col % 2 != 0 and row % 2 != 0):
            color = colors[BLOCKED]
        else:
            color = colors[FREE]

        self.image = pygame.Surface([cell_size, cell_size])
        self.image.fill(color)

    def draw_piece(self):
        if self.has_piece():
            color = colors[self.piece.player]
            pygame.draw.circle(self.image, color, (cell_size / 2, cell_size / 2), cell_size / 3)

            if self.piece.is_king:
                pygame.draw.circle(self.image, colors[KING] , (cell_size / 2, cell_size / 2), cell_size/6, 3)

    def update_image(self):
        self.draw_cell()
        self.draw_piece()

    def highlight(self, moveable):
        color = MOVEABLE if moveable else NOT_MOVEABLE
        self.image = pygame.Surface([cell_size, cell_size])
        self.image.fill(colors[color])
        self.draw_piece()

    def suggest(self):
        self.image = pygame.Surface([cell_size, cell_size])
        self.image.fill(colors[SUGGESTED])

    def update_position(self, position):
        self.rect.x, self.rect.y = position

    def has_piece(self):
        return self.piece is not None

class Piece:
    def __init__(self, player, is_king=False):
        self.player = player
        self.is_king = is_king

if __name__ == "__main__":
   game = Game()
   game.start()
