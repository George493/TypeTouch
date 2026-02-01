import pygame
import sys
import random
import time

pygame.init()

# УВЕЛИЧИВАЕМ ШИРИНУ ОКНА ЧТОБЫ ТЕКСТ НЕ ПЕРЕНОСИЛСЯ
WIDTH, HEIGHT = 1500, 800  # Было 1200, стало 1600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TypeTouch")
clock = pygame.time.Clock()

# ================ ТЕМЫ ================
LIGHT_THEME = {
    "bg": (250, 250, 250),           # Белый фон
    "text_area": (245, 245, 245),    # Слегка серый фон текста
    "keyboard_bg": (230, 230, 230),  # Светлый фон клавиатуры
    
    "key_normal": (240, 240, 240),   # Светлые клавиши
    "key_pressed": (64, 156, 255),   # Голубой при нажатии (как DeepSeek)
    "key_border": (200, 200, 200),   # Светлая граница клавиш
    
    "text_correct": (64, 156, 255),  # Голубой правильный символ
    "text_error": (255, 80, 80),     # Красный ошибка
    "text_pending": (150, 150, 150), # Серый ожидающий
    "text_white": (30, 30, 30),      # Темный текст для светлой темы
    
    "accent": (64, 156, 255),        # Основной голубой акцент
    "button": (240, 240, 240),       # Светлые кнопки
    "button_hover": (220, 220, 220), # Кнопка при наведении
    "progress_bg": (220, 220, 220),  # Фон прогресс-бара
    "progress_fill": (64, 156, 255), # Голубое заполнение
    "theme_icon": (40, 40, 40),      # Цвет иконки темы
    "cursor": (64, 156, 255)         # Цвет курсора
}

DARK_THEME = {
    "bg": (15, 15, 15),              # Темный фон
    "text_area": (25, 25, 25),       # Темный фон текста
    "keyboard_bg": (30, 30, 30),     # Темный фон клавиатуры
    
    "key_normal": (40, 40, 40),      # Темные клавиши
    "key_pressed": (255, 153, 0),    # Оранжевый при нажатии
    "key_border": (60, 60, 60),      # Темная граница клавиш
    
    "text_correct": (255, 153, 0),   # Оранжевый правильный
    "text_error": (255, 80, 80),     # Красный ошибка
    "text_pending": (100, 100, 100), # Серый ожидающий
    "text_white": (240, 240, 240),   # Белый текст для темной темы
    
    "accent": (255, 153, 0),         # Оранжевый акцент
    "button": (50, 50, 50),          # Темные кнопки
    "button_hover": (70, 70, 70),    # Кнопка при наведении
    "progress_bg": (40, 40, 40),     # Фон прогресс-бара
    "progress_fill": (255, 153, 0),  # Оранжевое заполнение
    "theme_icon": (200, 200, 200),   # Цвет иконки темы
    "cursor": (255, 153, 0)          # Цвет курсора
}

# Начинаем с темной темы
current_theme = DARK_THEME
is_dark_mode = True

# Для мигающего курсора
cursor_visible = True
cursor_blink_timer = 0
BLINK_INTERVAL = 500  # милисекунды

# Шрифты - УМЕНЬШИЛ РАЗМЕР ШРИФТА ДЛЯ ТЕКСТА ЕЩЕ БОЛЬШЕ
font_large = pygame.font.SysFont("consolas", 48)
font_normal = pygame.font.SysFont("consolas", 26)  # Было 28, стало 26
font_medium = pygame.font.SysFont("consolas", 24)  # Было 24
font_small = pygame.font.SysFont("consolas", 16)   # Было 16
# Шрифт с поддержкой эмодзи
emoji_font = pygame.font.SysFont("segoeuiemoji", 28)  # Шрифт с эмодзи
if emoji_font is None:
    emoji_font = pygame.font.SysFont("arial", 28)  # Запасной

# Раскладки клавиатуры
KEYBOARD_LAYOUT = [
    ['q','w','e','r','t','y','u','i','o','p','[',']','\\'],
    ['a','s','d','f','g','h','j','k','l',';',"'"],
    ['z','x','c','v','b','n','m',',','.','/']
]

RUSSIAN_LAYOUT = [
    ['й','ц','у','к','е','н','г','ш','щ','з','х','ъ','\\'],
    ['ф','ы','в','а','п','р','о','л','д','ж','э'],
    ['я','ч','с','м','и','т','ь','б','ю','.']
]

# УВЕЛИЧИВАЕМ ТЕКСТЫ ЧТОБЫ ЗАПОЛНИТЬ ШИРОКОЕ ОКНО
ENGLISH_TEXTS = [
    "while moves over your system course after some even hand and then continue typing practice",
    "the quick brown fox jumps over the lazy dog programming python code development project",
    "practice typing speed accuracy keyboard computer learning software application development",
    "hello world this is typing trainer application testing for blind typing skills improvement"
]

RUSSIAN_TEXTS = [
    "съешь же ещё этих мягких французских булок да выпей чаю затем продолжай практиковаться",
    "быстрая печать помогает эффективнее работать с компьютером и повышает продуктивность",
    "тренажер слепой печати улучшает скорость и точность набора текста для программистов",
    "привет мир это программа для обучения быстрой печати текста на русском и английском"
]

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
    
    def draw(self, surface, theme):
        color = theme["button_hover"] if self.hovered else theme["button"]
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, theme["key_border"], self.rect, 1)
        
        text_surf = font_normal.render(self.text, True, theme["accent"])
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.action:
                return self.action()
        return None

class ThemeToggle:
    def __init__(self):
        # Уменьшаем размер кнопки для эмодзи
        self.rect = pygame.Rect(WIDTH - 60, HEIGHT - 60, 50, 50)
        self.hovered = False
    
    def draw(self, surface, theme):
        # Фон кнопки темы
        bg_color = theme["button_hover"] if self.hovered else theme["button"]
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, theme["key_border"], self.rect, 1, 8)
        
        # Определяем эмодзи в зависимости от темы
        # Если СВЕТЛАЯ тема - показываем 🌙 (луну) чтобы переключить на темную
        # Если ТЕМНАЯ тема - показываем 🌞 (солнце) чтобы переключить на светлую
        emoji_text = "🌙" if not is_dark_mode else "🌞"
        
        # Рендерим эмодзи
        emoji_surf = emoji_font.render(emoji_text, True, theme["accent"])
        emoji_rect = emoji_surf.get_rect(center=self.rect.center)
        surface.blit(emoji_surf, emoji_rect)
    
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                return self.toggle_theme()
        return None
    
    def toggle_theme(self):
        global is_dark_mode, current_theme
        is_dark_mode = not is_dark_mode
        current_theme = DARK_THEME if is_dark_mode else LIGHT_THEME
        return "theme_toggled"

class TypingTrainer:
    def __init__(self):
        self.language = "eng"
        self.started = False
        self.start_time = None
        self.end_time = None
        self.total_time = 0
        self.typed_chars = 0
        self.correct_chars = 0
        self.current_text = ""
        self.text_chars = []
        self.current_pos = 0
        self.active_key = None
        self.key_animation_time = 0
        self.wpm = 0
        self.accuracy = 100
        self.finished = False
        self.show_stats = False
        
        # Для курсора
        self.cursor_visible = True
        self.cursor_blink_timer = 0
        
        # Границы областей (ПОДСТРАИВАЕМ ПОД НОВУЮ ШИРИНУ)
        self.text_area_rect = pygame.Rect(100, 100, WIDTH - 200, 200)  # ШИРЕ
        self.keyboard_area_rect = pygame.Rect(100, 420, WIDTH - 200, 250)  # ШИРЕ
        
        # Тогглер темы
        self.theme_toggle = ThemeToggle()
        
        self.create_buttons()
        self.generate_new_text()
    
    def create_buttons(self):
        button_height = 45
        start_y = HEIGHT - 60
        
        # СДВИГАЕМ КНОПКИ ПРАВЕЕ ИЗ-ЗА УВЕЛИЧЕННОЙ ШИРИНЫ
        # Рестарт
        self.reset_btn = Button(100, start_y, 160, button_height, "РЕСТАРТ", self.restart)
        
        # Язык
        self.lang_btn = Button(290, start_y, 120, button_height,  # СДВИНУТ ПРАВЕЕ
                              "ENG" if self.language == "eng" else "РУС", self.toggle_language)
        
        # НОВЫЙ ТЕКСТ - ШИРЕ И СДВИНУТ ДАЛЬШЕ
        self.new_btn = Button(440, start_y, 220, button_height, "НОВЫЙ ТЕКСТ", self.generate_new_text)
        
        self.buttons = [self.reset_btn, self.lang_btn, self.new_btn]
    
    def generate_new_text(self):
        self.finished = False
        self.show_stats = False
        
        if self.language == "eng":
            self.current_text = random.choice(ENGLISH_TEXTS)
        else:
            self.current_text = random.choice(RUSSIAN_TEXTS)
        
        self.text_chars = []
        for char in self.current_text:
            self.text_chars.append({
                "char": char,
                "state": "pending",
                "typed": None
            })
        
        self.current_pos = 0
        self.start_time = None
        self.end_time = None
        self.total_time = 0
        self.started = False
        self.typed_chars = 0
        self.correct_chars = 0
        self.wpm = 0
        self.accuracy = 100
        
        self.lang_btn.text = "ENG" if self.language == "eng" else "РУС"
        
        return "new_text"
    
    def toggle_language(self):
        self.language = "rus" if self.language == "eng" else "eng"
        self.lang_btn.text = "ENG" if self.language == "eng" else "РУС"
        self.generate_new_text()
        return "language_toggled"
    
    def restart(self):
        self.finished = False
        self.show_stats = False
        self.started = False
        self.start_time = None
        self.end_time = None
        self.total_time = 0
        self.current_pos = 0
        self.typed_chars = 0
        self.correct_chars = 0
        self.wpm = 0
        self.accuracy = 100
        
        for char in self.text_chars:
            char["state"] = "pending"
            char["typed"] = None
        
        return "restart"
    
    def handle_input(self, key_char):
        if self.finished:
            return
            
        if not self.started:
            self.started = True
            self.start_time = time.time()
        
        if self.current_pos < len(self.text_chars):
            current_char = self.text_chars[self.current_pos]
            
            if key_char.lower() == current_char["char"].lower():
                current_char["state"] = "correct"
                current_char["typed"] = key_char
                self.correct_chars += 1
            else:
                current_char["state"] = "error"
                current_char["typed"] = key_char
            
            self.typed_chars += 1
            self.current_pos += 1
            
            # Сбрасываем таймер курсора при каждом вводе
            self.cursor_blink_timer = pygame.time.get_ticks()
            self.cursor_visible = True
            
            if self.current_pos >= len(self.text_chars):
                self.end_time = time.time()
                self.total_time = self.end_time - self.start_time
                self.finished = True
                self.show_stats = True
                
                if self.total_time > 0:
                    self.wpm = int((self.correct_chars / 5) / (self.total_time / 60))
                    if self.typed_chars > 0:
                        self.accuracy = int((self.correct_chars / self.typed_chars) * 100)
                    else:
                        self.accuracy = 100
    
    def update_cursor(self):
        """Обновляет состояние мигающего курсора"""
        current_time = pygame.time.get_ticks()
        if current_time - self.cursor_blink_timer > BLINK_INTERVAL:
            self.cursor_visible = not self.cursor_visible
            self.cursor_blink_timer = current_time
    
    def set_active_key(self, key):
        self.active_key = key.lower()
        self.key_animation_time = time.time()

# Функции отрисовки
def draw_background():
    screen.fill(current_theme["bg"])

def draw_header():
    title = font_large.render("TYPETOUCH", True, current_theme["accent"])
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

def draw_text_area(trainer):
    pygame.draw.rect(screen, current_theme["text_area"], trainer.text_area_rect)
    
    # УМЕНЬШАЕМ МЕЖБУКВЕННОЕ РАССТОЯНИЕ ЕЩЕ БОЛЬШЕ
    char_spacing = 16  # Было 18, стало 16
    x_start = trainer.text_area_rect.x + 15  # Меньше отступ от края
    y_start = trainer.text_area_rect.y + 85  # Центрируем по вертикали
    
    # Проверяем, помещается ли весь текст
    total_width_needed = len(trainer.text_chars) * char_spacing
    max_width = trainer.text_area_rect.width - 30  # 15 отступ слева + 15 справа
    
    # Если текст не помещается, уменьшаем еще больше
    if total_width_needed > max_width:
        # Рассчитываем необходимый шаг
        needed_char_spacing = max_width / len(trainer.text_chars)
        char_spacing = max(needed_char_spacing, 12)  # Минимум 12 пикселей
    
    # ВСЕ СИМВОЛЫ В ОДНОЙ СТРОКЕ - НЕ РАЗБИВАЕМ НА СТРОКИ
    # Просто рисуем все символы подряд
    for char_idx, char_info in enumerate(trainer.text_chars):
        if char_info["state"] == "pending":
            color = current_theme["text_pending"]
        elif char_info["state"] == "correct":
            color = current_theme["text_correct"]
        elif char_info["state"] == "error":
            color = current_theme["text_error"]
        else:
            color = current_theme["text_pending"]
        
        # Рисуем символ с УМЕНЬШЕННЫМ ШРИФТОМ (font_normal теперь 26)
        char_surface = font_normal.render(char_info["char"], True, color)
        screen.blit(char_surface, (x_start + char_idx * char_spacing, y_start))
    
    # Рисуем мигающий курсор
    if not trainer.finished and trainer.cursor_visible:
        cursor_height = font_normal.get_height()
        cursor_x = x_start + trainer.current_pos * char_spacing
        
        # Если курсор в конце текста
        if trainer.current_pos == len(trainer.text_chars):
            cursor_x = x_start + len(trainer.text_chars) * char_spacing
        
        cursor_rect = pygame.Rect(cursor_x, y_start, 2, cursor_height)
        pygame.draw.rect(screen, current_theme["cursor"], cursor_rect)

def draw_progress_bar(trainer):
    # УВЕЛИЧИВАЕМ ПРОГРЕСС-БАР
    progress_bar_rect = pygame.Rect(100, 350, WIDTH - 200, 8)
    
    pygame.draw.rect(screen, current_theme["progress_bg"], progress_bar_rect)
    
    if len(trainer.text_chars) > 0:
        progress = trainer.current_pos / len(trainer.text_chars)
        fill_width = int(progress * progress_bar_rect.width)
        
        if fill_width > 0:
            fill_rect = pygame.Rect(progress_bar_rect.x, progress_bar_rect.y, 
                                  fill_width, progress_bar_rect.height)
            pygame.draw.rect(screen, current_theme["progress_fill"], fill_rect)

def draw_keyboard(trainer):
    if trainer.show_stats:
        return
    
    pygame.draw.rect(screen, current_theme["keyboard_bg"], trainer.keyboard_area_rect)
    
    layout = KEYBOARD_LAYOUT if trainer.language == "eng" else RUSSIAN_LAYOUT
    
    key_width, key_height = 55, 55
    key_margin = 5
    
    max_keys_in_row = max(len(row) for row in layout)
    keyboard_width = max_keys_in_row * (key_width + key_margin) - key_margin
    start_x = trainer.keyboard_area_rect.x + (trainer.keyboard_area_rect.width - keyboard_width) // 2
    start_y = trainer.keyboard_area_rect.y + 30
    
    for row_idx, row in enumerate(layout):
        row_start_x = start_x
        if row_idx == 1:
            row_start_x += (key_width + key_margin) // 2
        elif row_idx == 2:
            row_start_x += (key_width + key_margin)
        
        for col_idx, key in enumerate(row):
            x = row_start_x + col_idx * (key_width + key_margin)
            y = start_y + row_idx * (key_height + key_margin)
            
            if trainer.active_key == key and time.time() - trainer.key_animation_time < 0.1:
                key_color = current_theme["key_pressed"]
            else:
                key_color = current_theme["key_normal"]
            
            key_rect = pygame.Rect(x, y, key_width, key_height)
            pygame.draw.rect(screen, key_color, key_rect)
            pygame.draw.rect(screen, current_theme["key_border"], key_rect, 1)
            
            key_text = font_small.render(key.upper(), True, current_theme["text_white"])
            text_x = x + (key_width - key_text.get_width()) // 2
            text_y = y + (key_height - key_text.get_height()) // 2
            screen.blit(key_text, (text_x, text_y))

def draw_stats(trainer):
    if not trainer.show_stats:
        return
    
    stats_bg = pygame.Rect(100, 350, WIDTH - 200, 250)  # ШИРЕ
    pygame.draw.rect(screen, current_theme["text_area"], stats_bg)
    pygame.draw.rect(screen, current_theme["key_border"], stats_bg, 2)
    
    stats_title = font_normal.render("РЕЗУЛЬТАТЫ", True, current_theme["accent"])
    screen.blit(stats_title, (WIDTH // 2 - stats_title.get_width() // 2, 370))
    
    stats_y = 420
    line_height = 40
    
    time_text = f"Время: {trainer.total_time:.1f} секунд"
    time_surf = font_normal.render(time_text, True, current_theme["text_white"])
    screen.blit(time_surf, (WIDTH // 2 - time_surf.get_width() // 2, stats_y))
    
    wpm_text = f"Скорость: {trainer.wpm} зн/мин"
    wpm_surf = font_normal.render(wpm_text, True, current_theme["text_white"])
    screen.blit(wpm_surf, (WIDTH // 2 - wpm_surf.get_width() // 2, stats_y + line_height))
    
    acc_text = f"Точность: {trainer.accuracy}%"
    acc_color = current_theme["text_correct"] if trainer.accuracy > 90 else current_theme["text_error"]
    acc_surf = font_normal.render(acc_text, True, acc_color)
    screen.blit(acc_surf, (WIDTH // 2 - acc_surf.get_width() // 2, stats_y + line_height * 2))
    
    chars_text = f"Символов: {trainer.correct_chars}/{trainer.typed_chars}"
    chars_surf = font_normal.render(chars_text, True, current_theme["text_white"])
    screen.blit(chars_surf, (WIDTH // 2 - chars_surf.get_width() // 2, stats_y + line_height * 3))
    
    lang_text = f"Язык: {'ENG' if trainer.language == 'eng' else 'РУС'}"
    lang_surf = font_medium.render(lang_text, True, current_theme["text_pending"])
    screen.blit(lang_surf, (WIDTH // 2 - lang_surf.get_width() // 2, stats_y + line_height * 4))
    
    hint = font_medium.render("Нажмите 'РЕСТАРТ' чтобы попробовать снова", True, current_theme["text_pending"])
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, stats_y + line_height * 5))

def draw_instruction(trainer):
    if trainer.started or trainer.finished:
        return
    
    instruction = font_normal.render("Начните печатать чтобы начать тест...", 
                                   True, current_theme["text_pending"])
    screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, 320))

def draw_buttons(trainer):
    for button in trainer.buttons:
        button.draw(screen, current_theme)

def main():
    trainer = TypingTrainer()
    running = True
    
    print("\n" + "="*50)
    print("TYPETOUCH - Тренажер слепой печати")
    print(f"Размер окна: {WIDTH}x{HEIGHT}")
    print(f"Текущая тема: {'Темная' if is_dark_mode else 'Светлая'}")
    print("Нажмите на эмодзи в правом нижнем углу для смены темы")
    print("="*50 + "\n")
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                elif event.key == pygame.K_SPACE:
                    if not trainer.show_stats:
                        trainer.handle_input(' ')
                        trainer.set_active_key('space')
                
                elif event.unicode and event.unicode != '':
                    if not trainer.show_stats:
                        key_char = event.unicode
                        trainer.handle_input(key_char)
                        
                        if len(key_char) == 1 and key_char.isalpha():
                            trainer.set_active_key(key_char.lower())
            
            # Обработка кнопок
            for button in trainer.buttons:
                button.check_hover(mouse_pos)
                button.handle_event(event)
            
            # Обработка переключения темы
            trainer.theme_toggle.check_hover(mouse_pos)
            result = trainer.theme_toggle.handle_event(event)
            if result == "theme_toggled":
                print(f"[Тема] Переключена на: {'Темную' if is_dark_mode else 'Светлую'}")
        
        # Обновляем мигание курсора
        trainer.update_cursor()
        
        # Отрисовка
        draw_background()
        draw_header()
        draw_text_area(trainer)
        
        if not trainer.started and not trainer.finished:
            draw_instruction(trainer)
        
        draw_progress_bar(trainer)
        
        if trainer.show_stats:
            draw_stats(trainer)
        else:
            draw_keyboard(trainer)
        
        draw_buttons(trainer)
        trainer.theme_toggle.draw(screen, current_theme)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()