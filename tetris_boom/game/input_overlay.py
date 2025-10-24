import pygame
from game.data import GRAY
from game.globals import set_player_name

def get_player_name(screen, renderer):
    """
    Displays an input overlay for entering the player's name,
    while showing the game board in the background.
    """
    font = pygame.font.SysFont("Calibri", 30, True)
    small_font = pygame.font.SysFont("Calibri", 20, False)

    input_box = pygame.Rect(screen.get_width() // 2 - 150, screen.get_height() // 2, 300, 50)
    text = ""
    cursor_visible = True
    cursor_timer = 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                set_player_name("Player")
                return "Player"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    name = text.strip() or "Player"
                    set_player_name(name)
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < 15:
                        text += event.unicode

        # Draw background (game board)
        screen.fill((255, 255, 255))
        renderer._draw_game_board()

        # Draw translucent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        screen.blit(overlay, (0, 0))

        # Prompt
        prompt = font.render("Enter your name:", True, (0, 0, 0))
        screen.blit(prompt, (screen.get_width() // 2 - prompt.get_width() // 2, screen.get_height() // 2 - 80))

        # Input text and blinking cursor
        cursor_timer += 1
        if cursor_timer >= 30:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        display_text = text + ("|" if cursor_visible else "")
        txt_surface = font.render(display_text, True, (0, 0, 0))
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))

        pygame.draw.rect(screen, GRAY, input_box, 2)
        info_text = small_font.render("Press Enter to confirm", True, (50, 50, 50))
        screen.blit(info_text, (screen.get_width() // 2 - info_text.get_width() // 2, input_box.y + 60))

        pygame.display.flip()
        clock.tick(30)
