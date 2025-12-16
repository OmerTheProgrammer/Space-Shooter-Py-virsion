import pygame
import random
from enum import Enum

class colors(Enum):
    # צבעים ב rgb
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    light_gray = (90, 100, 110)
    dark_gray = (233, 236, 239)
    light_blue = (142, 202, 230)
    blue_green = (33, 158, 188)
    dark_blue = (2, 48, 71)
    yellow = (255, 183, 3)
    orange = (251, 133, 0)

pygame.init()  # activates pygame
window_width = 1550  # משתנה קבוע לרוחב החלון
window_height = 800  # משתנה קבוע לגובה החלון
window = pygame.display.set_mode((window_width, window_height))  # פותח חלון בגודל שקבענו
pygame.display.set_caption("Space Shooter")  # מכניס את הכותרת לחלון
pygame.display.set_icon(pygame.image.load("Assets/icon.png"))  # puts the logo
pygame.mixer.init()  # פותח את מנגן המוזיקה
background_music = pygame.mixer.Sound("Assets/battle_music.ogg")  # טוען מוזיקת רקע
background_music.set_volume(0.1)  # קובע את עוצמת מוזיקת הרקע
background_music.play(loops=-1)  # מפעיל את מוזיקת הרקע לנצח
backround_image = pygame.image.load("Assets/Backgrounds/blue.png")  # טוען את התמונת רקע לתפריט הראשי
backround_y = 0  # גובה הרקע, משתנה כדי לגרום לרקע לזוז
num_repetition_x = window_width // backround_image.get_width() + 1  # מחשב כמה פעמים למתוח את התמונה על ציר הx
num_repetition_y = window_height // backround_image.get_height() + 1  # מחשב כמה פעמים למתוח את התמונה על ציר הy
background_surface = pygame.Surface((window_width, window_height * 2))  # יוצר משטח בגודל המסך
for x in range(num_repetition_x):  # takes the photo and straches it moving for num_repetition
    for y in range(num_repetition_y * 2):  # how slow the stars scrol up, bigger number slower scrool.
        # straches the photo to the size of the screen, and moves it.
        background_surface.blit(backround_image, (x * backround_image.get_width(), y * backround_image.get_height()))

digit_pngs = []  # התמונות של הספרות
x_sign = pygame.transform.scale(pygame.image.load("Assets/UI/X_sign.png"), (24, 24))  # סימן של x טעון
for i in range(10):  # טעינת כל הספרות באותו גודל לרשימה
    digit_pngs.append(pygame.transform.scale(pygame.image.load(f"Assets/UI/digit_{i}.png"), (24, 24)))

power_up_dropper  = []  #
power_up_Xs = [] #
power_up_Ys = []  #
power_up_sound = pygame.mixer.Sound("Assets/PowerUp.mp3")  # צליל לקבלת יכולת מיוחדת
# התמונות הטעונות של היכולות המיוחדות
power_up_list = [
                pygame.image.load("Assets/Power-ups/bolt_gold.png"),
                pygame.image.load("Assets/Power-ups/star_gold.png"),
                pygame.image.load("Assets/Power-ups/pill_red.png"),
                pygame.image.load("Assets/Power-ups/shield_silver.png"),
                ]

shield_duration = 10  #
shield_life = 3  #
shield_active = False  #
shield_frame_index = 0  #
shield_farmes = [pygame.image.load("Assets/Effects/shield1.png"), pygame.image.load("Assets/Effects/shield2.png"),
                 pygame.image.load("Assets/Effects/shield3.png")]  # תמונות טעונות של השיריון בכל הרמות
shield_sounds = [pygame.mixer.Sound("Assets/sfx_shieldUp.ogg"),
                 pygame.mixer.Sound("Assets/sfx_shieldDown.ogg")]  # צליל קבלת השיריון, וצליל איבוד השיריון

laser_sound = pygame.mixer.Sound("Assets/laser_sound.ogg")  # טוען את הצליל ללייזרים
lasers = []  # שומר את כל הלייזרים על המסך
lasers_x = []  # שומר את שיעורי הx של כל הלייזרים במסך
lasers_y = []  # שומר את שיעורי הy של כל הלייזרים במסך
laser_speed = 10  # מהירות כל לייזר

explosion_frames = []  # רשימת פריימים טעונים
for i in range(1, 64):
    frame = pygame.image.load(f"Assets/explosion/explosion{i}.png")  # טוען את כל התמונות של הפיצוץ
    frame = pygame.transform.scale(frame, (320, 320))  # מסדר את גודל התמונות
    explosion_frames.append(frame)  # מוסיף את הפריימים לרשימה

explosion_effect = []  #
explosion_index = []  #
explosion_x = []  #
explosion_y = []  #
explosion_sound = pygame.mixer.Sound("Assets/explosion_sound.flac")  # טוען את הצליל פיצוץ

class Movement:
    def __init__(self,x ,y ,dx=0, dy=0):
        self.x = x
        self.y = y
        self.dx = dx #שינוי מיקום בציר הx,
        self.dy = dy # שינוי מיקום בציר הy

class Laser:
    def __init__(self,pic,movement=Movement(0, 0, 0, 8)):
        self.pic = pic
        self.movement = movement #לשנות את זה בקריאה אם רוצים לייזר מהיר יותר

class Player:
    avatar = pygame.image.load("Assets/player.png")  # loads the ship's image
    laser_red_pic = pygame.image.load("Assets/laserRed.png") # טוען את תמונה הלייזר של השחקן

    def og_place(self):
        self.movement = Movement((window_width - Player.avatar.get_rect().width) / 2,
                     window_height - (Player.avatar.get_rect().height + 30))

    def got_hit(self):
        self.life -= 1  # יורד לו חיים
        self.og_place()# מחזיר את החללית למיקום המקורי

    def __init__(self):
        self.movement = Movement(0,0,0,0)
        self.og_place()
        self.is_died = False  # הספינה לא מתה
        self.destroyed_time = 0  # הספינה לא בילתה זמן מושמדת
        self.life = 3  # יש לספינה 3 חיים
        self.lasers_count = 1  # כמה לייזרים הספינה יורה
        self.collosion = Player.avatar.get_rect(topleft=(self.movement.x, self.movement.y))

player = Player()

enemies = []
class Enemy:
    laser_pic = pygame.image.load("Assets/laserGreen.png")  # טוען תמונת לייזר אויב
    green_enemy_pic = pygame.image.load("Assets/enemyShip.png")
    enemies_destroyed = 0  #
    num_enemies_per_wave = 1  #

    def __init__(self,pic,movement,start_y,last_shoot,cooldown):
        self.pic = pic
        self.movement = movement
        self.start_y = start_y
        self.shoot_cooldown = cooldown
        self.last_shoot = last_shoot

        self.lasers = []

class Boss:
    green_boss_pic = pygame.image.load("Assets/boss.png")
    max_hp = 100
    def __init__(self, pic, movement, hp, shoot_cooldown, lasers_cooldown, last_time_laser, last_time_shoot, text_time):
        self.pic = pic
        self.movement = movement
        self.hp = hp
        self.hit = False
        self.shoot_cooldown = shoot_cooldown
        self.lasers_cooldown = lasers_cooldown
        self.last_time_laser = last_time_laser
        self.last_time_shoot = last_time_shoot
        self.text_time = text_time
        self.collosion = Boss.green_boss_pic.get_rect(topleft=(self.movement.x, self.movement.y))

        self.lasers = []

boss = Boss(Boss.green_boss_pic, Movement(window_width / 2 - Boss.green_boss_pic.get_width() / 2, -Boss.green_boss_pic.get_height() - 100, 2, 2),
            100, 4000, 150, pygame.time.get_ticks(), pygame.time.get_ticks(), 0)

text_i = 0  # מאפשר לטקסט סיום להופיע רק פעם אחת בלולאה
boss_text_i = 0 # מאפשר לטקסט בוס להופיע רק פעם אחת בלולאה
is_boss_text_on = False #מאפשר לשלוט בהיעלמות השחקן לטקסט הבוס
has_kamikazed = False  # מאפשר להתפוצץ על הבוס
life_to_score_sound = pygame.mixer.Sound("Assets\Albéniz - Rumores de la caleta.ogg")
wave_font = pygame.font.Font("Assets/UI/FreeSansBold.ttf", 190)  # טעינת פונט לגלים ולמסך סיום
info_font = pygame.font.Font("Assets/UI/kenvector_future.ttf", 50)
FPS = 60  # the amount of frames we want to run in a sec
clock = pygame.time.Clock()  # crates a clock
score = 0  # the score

# משתנים עבור הגלים
class wave:
    counter = 1 #
    time_between_waves = 2000 #
    ending_time = pygame.time.get_ticks()  #
    finished = True  #
    max_wave = 4  #

menu_running = True  # ?האם התפריט מופעל

def Main_menu():
    global running, menu_running, backround_y, displaing_scores
    menu_running = True  # מוודא שהדגל מופעל
    displaing_scores = False  # ?האם הציונים מוצגים

    start_btn_image = pygame.image.load("Assets/Main_menu/Start_BTN.png")  # טוען את התמונה של הכפתור התחלה
    exit_btn_image = pygame.image.load("Assets/Main_menu/Exit_BTN.png")  # טוען את התמונה של הכפתור יציאה

    # טוען את הבאנר ומסדר את הגודל
    header_image = pygame.transform.scale(pygame.image.load("Assets/Main_menu/Header.png"), (window_width // 2 + 200, 300))
    # טוען את תמונת הכפתור לדף המידע ומסדר את הגודל
    info_btn_image = pygame.transform.scale(pygame.image.load("Assets/Main_menu/Info_BTN.png"), (120, 120))
    # טוען את תמונת הכפתור לדף ההגדרות ומסדר את הגודל
    settings_btn_image = pygame.transform.scale(pygame.image.load("Assets/Main_menu/Settings_BTN.png"), (120, 120))
    # טוען את תמונת הכפתור לדף הדירוגים ומסדר את הגודל

    raiting_btn_image = pygame.transform.scale(pygame.image.load("Assets/Main_menu/Rating_BTN.png"), (120, 120))

    # יצירת ריבוע התגובה של הבאנר
    header_rect = header_image.get_rect(center=(window_width // 2, 200))
    # יצירת ריבוע התגובה של כפתור הפתיחה
    start_btn_rect = start_btn_image.get_rect(center=(window_width // 2, 400))
    # יצירת ריבוע התגובה של כפתור הסגירה
    exit_btn_rect = exit_btn_image.get_rect(center=(window_width // 2, 540))
    # יצירת ריבוע התגובה של כפתור לדף המידע
    info_btn_rect = info_btn_image.get_rect(topright=(window_width - 20, 20))
    # יצירת ריבוע התגובה של כפתור לדף ההגדרות
    settings_btn_rect = settings_btn_image.get_rect(topright=(window_width - 20, 150))
    # יצירת ריבוע התגובה של כפתור לדף הדירוגים
    raiting_btn_rect = raiting_btn_image.get_rect(topright=(window_width - 20, 280))

    while menu_running:  # מריץ את התפריט הראשי
        clock.tick(FPS)  # change only under 60 frames in a second
        for event in pygame.event.get():  # רץ על כל האירועים על המסך
            if event.type == pygame.QUIT:  # אם סוגרים, תשנו את הדגלים לfalse, ותעצרו את הלולאה המשחק ולולאת התפריט
                running = False
                menu_running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:  # האם כפתור נלחץ?
                if event.button == 1:  # האם הכפתור השמאלי נלחץ?
                    mouse_pos = pygame.mouse.get_pos()  # שומר מיקום העכבר

                    # האם נוגע בריבוע התגובה של כפתור ההתחלה + התנאי בelif, גורם לכך שזה יופעל כשילחץ הכפתור
                    if start_btn_rect.collidepoint(mouse_pos):
                        menu_running = False  # מכבה את התפריט הראשי
                        player.is_died = False  # מחזיר את החללית לחיים

                    elif settings_btn_rect.collidepoint(mouse_pos):  # לוחצים על ריבוע התגובה של ההגדרות להפעיל את הפונקציה של העמוד
                        settings()  # מפעיל את עמוד ההגדרות

                    elif exit_btn_rect.collidepoint(mouse_pos):  # אם סוגרים, תשנו את הדגלים לfalse, ותעצרו את הלולאה המשחק ולולאת התפריט
                        menu_running = False  # מכבה את התפריט הראשי
                        running = False  # סוגר הכל

                    elif info_btn_rect.collidepoint(mouse_pos):  # לוחצים על כפתור מידע
                        info_page()  # ושולחים אותך לעמוד מידע

                    elif raiting_btn_rect.collidepoint(mouse_pos):  #לוחצים על כפתור הדירוגים
                        displaing_scores = not displaing_scores  # אם חלון הדילוגים פתוח הוא סוגר, ואם סגור הוא פותח

        backround_y -= 4  # גולל את התמונת רקע
        if backround_y <= -backround_image.get_height():  # אם הקצה העליון של תמונת הרקע התקדם לחלוטין מחוץ לאזור הראיה
            backround_y = 0  # תתחיל את גובה התמונה מהתחלה

        window.blit(background_surface, (0, backround_y))  # מוציא למסך את הרקע במיקום 0,גובה
        window.blit(header_image, header_rect)  # מוציא למסך את הבאנר בקוביה שלו
        window.blit(start_btn_image, start_btn_rect)  # מוציא למסך את הכפתור התחלה בקוביה שלו
        window.blit(exit_btn_image, exit_btn_rect)  # מוציא למסך את הכפתור התחלה בקוביה שלו
        window.blit(info_btn_image, info_btn_rect)  # מוציא למסך את הכפתור המידע בקוביה שלו
        window.blit(raiting_btn_image, raiting_btn_rect)  # מוציא למסך את הכפתור הדירוגים בקוביה שלו
        window.blit(settings_btn_image, settings_btn_rect)  # מוציא למסך את הכפתור הגדרות בקוביה שלו

        if displaing_scores:  # יםwindow.blitבודק אם לפתוח, צריך להיות מתחת ל
            high_scores_page()  # מפעיל את הדף

        pygame.display.update()  # לעדכן את המראה בלולאה


def info_page():
    global running, menu_running, backround_y, displaing_scores

    back_btn_img = pygame.transform.scale(pygame.image.load("Assets/Main_Menu/Setting/Backward_BTN.png"), (150, 150))# תמונת הכפתור אחורה בגודל הנכון
    back_btn_rect = back_btn_img.get_rect(topleft=(20, 20))
    info_lines = [
        "Controls:",
        "Use the Arrow Keys or WASD Keys to move:",
        "   Up Arrow  \ W: Move Up",
        "   Down Arrow \ S: Move Down",
        "   Left Arrow  \ A: Move Left",
        "   Right Arrow  \ D: Move Right",
        "Press the Space Bar to shoot projectiles."
    ]
    info_running = True

    while info_running:
        for event in pygame.event.get():  # רץ על כל האירועים על המסך
            if event.type == pygame.QUIT:  # אם סוגרים, תשנו את הדגלים לfalse, ותעצרו את הלולאה המשחק ולולאת התפריט
                    running = False
                    menu_running = False
                    info_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:  # כפתור העכבר נלחץ
                mouse_pos = pygame.mouse.get_pos()  # שומר מיקום העכבר
                if back_btn_rect.collidepoint(mouse_pos):  # אם לוחצים אחורה סוגרים את ההגדרות
                    info_running = False
                    displaing_scores = False

        backround_y -= 4  # גולל את התמונת רקע
        if backround_y <= -backround_image.get_height():  # אם הקצה העליון של תמונת הרקע התקדם לחלוטין מחוץ לאזור הראיה
            backround_y = 0  # תתחיל את גובה התמונה מהתחלה

        window.blit(background_surface, (0, backround_y))  # מוציא למסך את הרקע במיקום 0,גובה
        window.blit(back_btn_img, back_btn_rect) #

        y_offset = 100
        for line in info_lines:
            text_surface = info_font.render(line, False, colors.white.value)
            text_rect = text_surface.get_rect(center=(window_width // 2, y_offset))
            window.blit(text_surface, text_rect)
            y_offset += 90

        pygame.display.update()  # לעדכן את המראה בלולאה



def read_high_scores():
    try:  # תנסה
        with open("space_shooter_scores.txt", "r") as file:  # במצב קריאה shooter scores תפתח את הקובץ
            scores = [int(line.strip()) for line in file]  # שורה שורה ,int שומר ברשימה את כל הטקסט מהקובץ, בטיפוס
            return scores  # מחזיר את הציונים השמורים בקובץ
    except FileNotFoundError:  # אם הקובץ לא נמצא
        return ["empty"]  # להחזיר רשימה ריקה
    except ValueError: #אם יש שורה ריקה בקובץ
        return ["file is broken"]


def high_scores_page():
    high_scores = read_high_scores()  # שומרת את ציונים מהקובץ

    # טעינת החלון הקופץ וקביעת גודל החלון הקופץ
    pop_up_window = pygame.transform.scale(pygame.image.load("Assets/Main_Menu/Pause/Window.png"), (550, 750))
    # ממקם את החלון בתמונה שלו
    window.blit(pop_up_window,
                ((window_width - pop_up_window.get_width()) // 2,
                 (window_height - pop_up_window.get_height()) // 2 - 10)
                )

    # רווח בין ספרה לספרה = (גובה החלון - סהך הגובה של כל הציונים) לאמצע
    y_offset = (window_height - len(high_scores) * 70) // 2 + 10
    # טעינת התמונה לטקסט של הציונים וקביעת גודל התמונה
    score_text_img = pygame.transform.scale(pygame.image.load("Assets/Main_Menu/Pause/Score.png"),(500, 80))

    """
    :שווה ל xחישוב ציר ה
    עובי החלון - עובי החלון הקופץ חלקי 2 כדי שיהיה באמצע + עובי החלון הקופץ - עובי תמונת טקסט חלקי 2 כדי שיהיה באמצע
    :שווה ל yחישוב ציר ה
    גובה החלון - גובה החלון הקופץ + 28 חלקי 2 כדי שיהיה באמצע - 5 כדי לייצב אותו החלון הקופץ
    """
    window.blit(score_text_img,  # מציג את תמונת הטקסט במיקום
                (((window_width - pop_up_window.get_width()) // 2) +
                 ((pop_up_window.get_width() - score_text_img.get_width()) // 2),
                 (window_height - pop_up_window.get_height() + 28) // 2 - 5)
                )

    for high_score in high_scores:  # רץ על כל הציונים
        score_string = str(high_score).zfill(6)  # מוסיף אפסים עד שיהיו 6 ספרות לציון
        x_offset = (window_width - 6 * 75) // 2  # עובי החלון - אורך הציון * 80 // 2, 80 זה המרחק בין ספרות
        for char in score_string:  # רץ על הספרות אחד אחד
            window.blit(pygame.transform.scale(digit_pngs[int(char)], (70, 70)), (x_offset, y_offset))  # לשמור את
            x_offset += 75  # xמרחק בין הספרות ב
        y_offset += 75  # yמרחק בין ספרות ב


def update_high_scores(current_score):
    scores = read_high_scores()
    scores.append(current_score)
    scores.sort(reverse=True)
    if len(scores) > 8:
        scores = scores[:8]
    with open("space_shooter_scores.txt", "w") as file:
        for s in scores:
            file.write(f"{s}\n")


def settings():
    global running, menu_running, backround_y  #
    settings_running = True  # דגל הלולאה

    is_bg_music_on = background_music.get_volume() > 0  # בודק אם מוזיקת הרקע פועלת
    is_sound_effects_on = laser_sound.get_volume() > 0  # בודק אם אפקטי הצליל פועלים

    # התמונות הטעונות של כפתור המוזיקה, מופעל או לא, (בסדר הזה)
    music_btn_imgs = [pygame.image.load("Assets/Main_Menu/BTNs_Active/Music_BTN.png"),
                      pygame.image.load("Assets/Main_Menu/Setting/Music_BTN.png")]
    # התמונות הטעונות של כפתור אפקטי הצליל, מופעל או לא, (בסדר הזה)
    sound_btn_imgs = [pygame.image.load("Assets/Main_Menu/BTNs_Active/Sound_BTN.png"),
                      pygame.image.load("Assets/Main_Menu/Setting/Sound_BTN.png")]

    back_btn_img = pygame.image.load("Assets/Main_Menu/Setting/Backward_BTN.png")  # תמונת הכפתור אחורה
    music_text_img = pygame.image.load("Assets/Main_Menu/Setting/Music.png")  # התמונה של טקסט מוזיקה
    sound_text_img = pygame.image.load("Assets/Main_Menu/Setting/Sound.png")  # התמונה של טקסט אפקטי צליל

    # שומר את הבאנר של ההגדרות בגודל הזה
    header_image = pygame.transform.scale(pygame.image.load("Assets/Main_menu/Setting/Header.png"),(1200, 200))

    # גודל כפתורי ההגדרות, ללא כפתור האחורה
    image_width = 150
    image_height = 150
    # משנה את גודל התמונה של הכפתורים הכבויים והדלוקים ל(200,200)
    back_btn_img = pygame.transform.scale(back_btn_img, (image_width, image_height))
    music_btn_imgs[1] = pygame.transform.scale(music_btn_imgs[1], (image_width, image_height))
    sound_btn_imgs[1] = pygame.transform.scale(sound_btn_imgs[1], (image_width, image_height))
    music_btn_imgs[0] = pygame.transform.scale(music_btn_imgs[0], (image_width, image_height))
    sound_btn_imgs[0] = pygame.transform.scale(sound_btn_imgs[0], (image_width, image_height))

    # מיקום הבאנר של ההגדרות
    header_rect = header_image.get_rect(center=(window_width // 2 + 100, 125))
    # מיקום התמונה של טקסט המוזיקה
    music_text_rect = music_text_img.get_rect(midleft=(window_width // 2 - 70, window_height // 2 - 80))
    # מיקום התמונה של טקסט אפקטי צליל
    sound_text_rect = sound_text_img.get_rect(midleft=(window_width // 2 - 70, window_height // 2 + 80))
    # מיקום התמונה של כפתור מוזיקה
    music_button_rect = music_btn_imgs[1].get_rect(midright=(window_width // 2 - 90, window_height // 2 - 80))
    # מיקום התמונה של כפתור אפקטי צליל
    sound_button_rect = sound_btn_imgs[1].get_rect(midright=(window_width // 2 - 90, window_height // 2 + 80))
    # מיקום התמונה של כפתור האחורה
    back_btn_rect = back_btn_img.get_rect(topleft=(20, 20))

    while settings_running:
        clock.tick(FPS)  # change only under 60 frames in a second

        if is_bg_music_on:
            music_btn = music_btn_imgs[0]  # כפתור מוזיקה מודלק
        else:
            music_btn = music_btn_imgs[1]  # כפתור מוזיקה מכובה

        if is_sound_effects_on:
            sound_btn = sound_btn_imgs[0]  # כפתור אפקטי צליל מודלק
        else:
            sound_btn = sound_btn_imgs[1]  # כפתור אפקטי צליל מכובה

        # מזיז את הרקע
        backround_y -= 4
        if backround_y <= -backround_image.get_height():
            backround_y = 0

        # מכניס למסך את הרקע, הכפתורים
        window.blit(background_surface, (0, backround_y))
        window.blit(header_image, header_rect)
        window.blit(music_btn, music_button_rect)
        window.blit(sound_btn, sound_button_rect)
        window.blit(music_text_img, music_text_rect)
        window.blit(sound_text_img, sound_text_rect)
        window.blit(back_btn_img, back_btn_rect)

        for event in pygame.event.get():  # רצים על כל האירןעים
            if event.type == pygame.QUIT:  # ,אם סוגרים ,לעצור את לולאת המשחק, לולאת התפריט הראשי, לולאת ההגדרות
                running = False
                menu_running = False
                settings_running = False
                info_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:  # כפתור העכבר נלחץ
                mouse_pos = pygame.mouse.get_pos()  # שומר מיקום העכבר

                if music_button_rect.collidepoint(mouse_pos):  # לוחצים על ריבוע תגובת כפתור המוזיקה
                    if is_bg_music_on:  # האם המוזיקה דולקת?
                        background_music.set_volume(0)  # שים את הווליום ל0
                        life_to_score_sound.set_volume(0)  #
                        is_bg_music_on = False  # המוזיקה כבויה
                    else:  # אחרת
                        background_music.set_volume(0.2)  # שים ווליום ל0.2
                        life_to_score_sound.set_volume(1)  #
                        is_bg_music_on = True  # המוזיקה דלוקה

                elif sound_button_rect.collidepoint(mouse_pos):  # האם אפקטי הצליל דולקים?
                    if is_sound_effects_on:
                        laser_sound.set_volume(0)  # מכבה צליל לייזר
                        explosion_sound.set_volume(0)  # מכבה צליל פיצוץ
                        power_up_sound.set_volume(0)  # מכבה את צליל קבלת יכולת מיוחדת
                        shield_sounds[0].set_volume(0)  # מכבה צליל של קבלת שיריון
                        shield_sounds[1].set_volume(0)  # מכבה צליל של איבוד שיריון
                        is_sound_effects_on = False  # האפקטים הקוליים כבויים
                    else:
                        laser_sound.set_volume(1)  # מדליק צליל לייזר
                        explosion_sound.set_volume(1)  # מדליק צליל פיצוץ
                        power_up_sound.set_volume(1)  # מדליק את צליל קבלת יכולת מיוחדת
                        shield_sounds[0].set_volume(1)  # מדליק צליל של קבלת שיריון
                        shield_sounds[1].set_volume(1)  # מדליק צליל של איבוד שיריון
                        is_sound_effects_on = True  # האפקטים הקוליים דלוקים

                elif back_btn_rect.collidepoint(mouse_pos):  # אם לוחצים אחורה סוגרים את ההגדרות
                    settings_running = False
                    displaing_scores = False

        pygame.display.update()  # מעדכנים את המסך בכל ריצת לולאה


def create_enemies():
    for i in range(Enemy.num_enemies_per_wave):
        enemies.append(Enemy(Enemy.green_enemy_pic,
        Movement(random.randint(Enemy.green_enemy_pic.get_rect().width, window_width - Enemy.green_enemy_pic.get_rect().width), #x
        random.randint(-window_height // 2, -Enemy.green_enemy_pic.get_rect().height),2,2), #y,dx,dy
        random.randint(-window_height // 2, -Enemy.green_enemy_pic.get_rect().height),3000,3000)) #start_y, last shoot (here its the first), cooldown

def display_score():
    score_str = str(score).zfill(6)
    x_offset = window_width - 30

    for char in reversed(score_str):
        image = digit_pngs[int(char)]
        x_offset -= image.get_width()
        window.blit(image, (x_offset, 30))


def display_life():
    if player.life < 0:
        player.life = 0
    x_offset = 30

    str_life = str(player.life).zfill(3)
    for current_img in [pygame.image.load("Assets/UI/playerLife1_red.png"), x_sign, str_life]:
        if current_img == str_life:  # אם רצים על החיים בטקסט
            x_offset += 70
            for char in reversed(str_life):  # תעבור על הספרות אחת אחת מהסוף להתחלה
                image = digit_pngs[int(char)]
                x_offset -= image.get_width()
                window.blit(image, (x_offset, 30))
            break
        window.blit(current_img, (x_offset, 30))
        x_offset += current_img.get_width() + 10


def shot_lasers():
    laser_offset = 24  # רווח קבוע בין הלייזרים
    laser_sound.play()  #
    if player.lasers_count % 2 == 0:  # אם כמות הלייזרים שהספינה יורה הם זוגיים
        """
        כנקודת ההתחלה של הלייזר אם זוגי = -קבוע הרווח * מציאת נקודת האמצע למספר לייזרים + חצי מקבוע הרווח
        כלומר נקודת ההתחלה היא 24-*נקודת האמצע של מספר הלייזרים + 12
        כלומר מחשב את נקודת התחלה הרחוקה מהאמצע
        """
        start_offset = -laser_offset * (player.lasers_count // 2) + laser_offset / 2
    else:
        """
        כנקודת ההתחלה של הלייזר אם אי-זוגי= -קבוע הרווח * מציאת נקודת האמצע למספר הלייזרים  
        כלומר נקודת ההתחלה היא 24-*נקודת האמצע של מספר הלייזרים 
        כלומר מחשב את נקודת התחלה הרחוקה מהאמצע
        """
        start_offset = -laser_offset * (player.lasers_count // 2)

    for i in range(player.lasers_count):  # יוצר לייזרים בכמות שהספינה יורה
        """
        החישוב:
        מיקום הספינה בציר x + מיקום אמצע הספינה - מיקום אמצע הלייזר + קבוע הרווח*כמות הלייזרים שכבר על המסך
        """
        lasers_x.append(player.movement.x + Player.avatar.get_width() / 2 - Player.laser_red_pic.get_width() / 2 + start_offset + i * laser_offset)  # מחשב את מיקום הלייזר על ציר הx
        """
        החישוב:
        גובה הספינה - גובה הלייזר + בערך מוחלט(מרכז מערך הלייזרים של הספינה) * 16
        נותן מרווח בין כל לייזר של 16
        """
        lasers_y.append(player.movement.y - Player.laser_red_pic.get_height() + abs(i - (player.lasers_count - 1) / 2) * 16)  # מחשב את גובה הלייזר
        lasers.append(Player.laser_red_pic)  # להוסיף את הלייזר למסך

running = True  # מכניס אותך ללולאה שאחרי הפונקציה
Main_menu()  # כתוב בקוד שלו, תקוע בפונקציה עד שבוחרים עמוד

while running:  # ריצת המשחק
    clock.tick(FPS)  # change only under 60 frames in a second
    boss.collosion = Boss.green_boss_pic.get_rect(topleft=(boss.movement.x, boss.movement.y))  # שומר את הריבוע ההתנגשות של הבוס בכל ריצה
    # אם המגן פתוח לעשות את המלבן מתאימים למגן
    player.collosion = Player.avatar.get_rect(topleft=(player.movement.x, player.movement.y))  # שומר את הריבוע ההתנגשות של השחקן בכל ריצה
    for event in pygame.event.get():  # רצים על כל האירןעים
        if event.type == pygame.QUIT:  # אם סוגרים ,לעצור את לולאת המשחק
            running = False
        if event.type == pygame.KEYDOWN:  # אם לוחצים
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:  # אם לוחצים כפתור חץ שמאל,
                player.movement.dx -= 5  # זזים שמאלה
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # אם לוחצים כפתור חץ ימין,
                player.movement.dx += 5  # זזים ימינה
            if event.key == pygame.K_UP or event.key == pygame.K_w:  # אם לוחצים כפתור חץ למעלה,
                player.movement.dy -= 5  # זזים למעלה
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:  # אם לוחצים כפתור חץ למטה,
                player.movement.dy += 5  # זזים למטה
            #צריך להוסיף תנאי שלא יאפשר לירות בזמן *המעבר* לטקסט בוס
            if event.key == pygame.K_SPACE and not player.is_died and not is_boss_text_on:  # אם לוחצים על רווח והספינה חיה
                shot_lasers()  # יורים לייזר/ים

        if event.type == pygame.KEYUP:  # אם משחחרים
            #כפתור מאלו
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d]:
                    player.movement.dx = 0  # לא ממשיכים לזוז בציר הx

                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s]:
                    player.movement.dy = 0  # לא ממשיכים לזוז בציר הy

    player.movement = Movement(player.movement.x + player.movement.dx,
                   player.movement.y + player.movement.dy, player.movement.dx, player.movement.dy) #שנה את מיקום הספינה אחרי לחיצה על כפתורים


    """
    אם המגן פתוח לעשות את הגבולות מתאימים למגן
    if shield_active:

        if player.movement.x <= 10:  # אם מיקום החללית בציר הx קטן או שווה ל0
            player.movement.x = 10  # מאפס את שיעור הx של החללית
        if player.movement.y <= 10:  # אם מיקום החללית בציר y קטן או שווה ל0
            player.movement.y = 10  # מאפס את שיעור הy של החללית
        if player.movement.x >= window_width - Player.avatar.get_rect().width - 10:  # אם חוצה את גבול הרוחב
            player.movement.x = window_width - Player.avatar.get_rect().width - 10  # להגיע לקצה
        if player.movement.y >= window_height - Player.avatar.get_rect().height - 20:  #
            player.movement.y = window_height - Player.avatar.get_rect().height - 20  # להגיע לקצה
        
    else:
    """
    if player.movement.x <= 10:  # אם מיקום החללית בציר הx קטן או שווה ל0
        player.movement.x = 10  # מאפס את שיעור הx של החללית
    if player.movement.y <= 10:  # אם מיקום החללית בציר y קטן או שווה ל0
        player.movement.y = 10  # מאפס את שיעור הy של החללית
    if player.movement.x >= window_width - Player.avatar.get_rect().width - 10:  # אם חוצה את גבול הרוחב
        player.movement.x = window_width - Player.avatar.get_rect().width - 10  # להגיע לקצה
    if player.movement.y >= window_height - Player.avatar.get_rect().height - 20:  #
        player.movement.y = window_height - Player.avatar.get_rect().height - 20  # להגיע לקצה

    remove_lasers = set()  # לייזרים שנמחקו בטיפוס קבוצה כדי שלא יהיו כפילויות
    remove_enemies = set()  # אויבים שנמחקו בטיפוס קבוצה כדי שלא יהיו כפילויות

    for i in range(len(lasers)):  # רץ על כל הלייזרים
        lasers_y[i] -= laser_speed  # מזיז את הליזריים למטה במסך

        laser_collosion = lasers[i].get_rect(topleft=(lasers_x[i], lasers_y[i]))  # שומר את הריבוע ההתנגשות של הלייזר

        if laser_collosion.colliderect(boss.collosion) and boss.hp > 0:  #
            boss.hit = True  #
            boss.hp -= 1  #
            remove_lasers.add(i)  #
            if boss.hp <= 0:  #
                player.destroyed_time = pygame.time.get_ticks()  #
                explosion_effect.append(explosion_frames)  #
                explosion_index.append(0)  #
                explosion_x.append(boss.collosion.x + Boss.green_boss_pic.get_rect().width)  #
                explosion_y.append(boss.collosion.y - Boss.green_boss_pic.get_rect().height - 10)  #
                explosion_sound.play()  #

        if lasers_y[i] < -lasers[i].get_rect().height:  # אם הלייזר יוצא מהמסך
            remove_lasers.add(i)  # , תוסיף אותו לרשימת הלייזרים שנמחקו, הוא עדיין על המסך
        else:
            for j in range(len(enemies)):  # רץ על האויבים
                enemy_collosion = enemies[j].pic.get_rect(topleft=(enemies[j].movement.x, enemies[j].movement.y))  # שומר את הריבוע ההתנגשות של האויב הנוכחי בריצה

                if enemy_collosion.colliderect(laser_collosion):  # אם האויב נוגע בלייזר
                    remove_lasers.add(i)  # , מוסיפים את הלייזר לרשימת הלייזרים שנמחקו,אך הוא עדיין על המסך
                    explosion_effect.append(explosion_frames)  # מכניסים את רשימת תמונות הפיצוץ למשתנה, כדי שנוכל לאפס כשמתחילים מחדש
                    explosion_index.append(0)  #
                    explosion_x.append(enemy_collosion.x + enemies[j].pic.get_rect().width)  # של ריבוע האויב + עובי האויב xשל הפיצוץ שווה ל:שיעור ה xשיעור ה
                    explosion_y.append(enemy_collosion.y - enemies[j].pic.get_rect().height - 10)  # של ריבוע האויב + גובה האויב - 10 yשל הפיצוץ שווה ל: שיעור ה  yשיעור ה
                    explosion_sound.play()  # משמיע צליל פיצוץ
                    score += 15  # האויב מת, אז להוסיף ניקוד שווה לחיים
                    Enemy.enemies_destroyed += 1  # להוסיף אויב מושמד
                    remove_enemies.add(j)  # מוסיפים את האויב לרשימת האויבים שנמחקו, אך הוא עדיין על המסך
                    # מזמן את היכולות המיוחדות
                    if random.randint(1, 100) < 50:  # מופעל בצורה אקראית 50%
                        """
                        
                        """
                        power_up_Xs.append(enemies[j].movement.x + enemies[j].pic.get_rect().width / 2)
                        power_up_Ys.append(enemies[j].movement.y - enemies[j].pic.get_rect().height)
                        power_up_dropper.append(power_up_list[random.randint(0, 3)])


    for i in reversed(list(remove_lasers)):
        lasers.pop(i)
        lasers_x.pop(i)
        lasers_y.pop(i)

    remove_explosiones = []
    for i in range(len(explosion_effect)):
        explosion_index[i] += 1
        if explosion_index[i] >= len(explosion_frames):
            remove_explosiones.append(i)

    for i in reversed(remove_explosiones):
        explosion_effect.pop(i)
        explosion_index.pop(i)
        explosion_x.pop(i)
        explosion_y.pop(i)

    for i in range(len(enemies)):
        if enemies[i].movement.y < abs(enemies[i].start_y / 2):
            enemies[i].movement.y += enemies[i].movement.dy
        else:
            enemies[i].movement.x += enemies[i].movement.dx

        if enemies[i].movement.x <= 0:
            enemies[i].movement.dx = 2

        if enemies[i].movement.x >= window_width - enemies[i].pic.get_rect().width:
            enemies[i].movement.dx = -2

        current_time = pygame.time.get_ticks()
        if current_time - enemies[i].last_shoot >= enemies[i].shoot_cooldown:
            if random.randint(1, 100) < 3:
                enemies[i].lasers.append(Laser(Enemy.laser_pic))
                enemies[i].lasers[-1].movement = Movement( #מיקום הלייזר האחרון
                    enemies[i].movement.x + enemies[i].pic.get_rect().width / 2 - Enemy.laser_pic.get_rect().width / 2, #x
                    (enemies[i].movement.y + enemies[i].pic.get_rect().height),0,8) #y
                laser_sound.play()
                enemies[i].last_shoot = current_time

    remove_enemy_lasers = []
    for enemy in enemies:
        for laser in range(len(enemy.lasers)):
            if enemy.lasers[laser].movement.dy != 0:
                enemy.lasers[laser].movement.y += enemy.lasers[laser].movement.dy
            else:
                enemy.lasers[laser].movement.y += 8

            laser_collosion = enemy.lasers[laser].pic.get_rect(topleft=(enemy.lasers[laser].movement.x, enemy.lasers[laser].movement.y))

            for j in range(len(enemies)):
                enemy_collosion = enemies[j].pic.get_rect(topleft=(enemies[j].movement.x, enemies[j].movement.y))

                if player.collosion.colliderect(enemy_collosion) and not player.is_died:  # אם השחקן נוגע באוייב
                    explosion_effect.append(explosion_frames)
                    explosion_index.append(0)
                    explosion_x.append(enemy_collosion.x + enemies[j].pic.get_rect().width)
                    explosion_y.append(enemy_collosion.y - enemies[j].pic.get_rect().height - 10)
                    explosion_sound.play()
                    score += 15
                    Enemy.enemies_destroyed += 1
                    remove_enemies.add(j)

                    if shield_active:
                        shield_life -= 1
                        shield_frame_index -= 1
                        if shield_life == 0:
                            shield_active = False
                            shield_sounds[1].play()
                    else:
                        if player.life > 1:
                            player.got_hit()
                        else:
                            player.life -= 1  # מוריד ל0
                            player.is_died = True  # הורג אותו
                            player.destroyed_time = pygame.time.get_ticks()  # שומר את זמן ההשמדה
                        continue

            if enemy.lasers[laser].movement.y > window_height:
                remove_enemy_lasers.append(laser)

            elif player.collosion.colliderect(laser_collosion) and not player.is_died:
                remove_enemy_lasers.append(laser)
                if shield_active:
                    shield_life -= 1
                    shield_frame_index -= 1
                    if shield_life == 0:
                        shield_active = False
                        shield_sounds[1].play()
                else:
                    explosion_effect.append(explosion_frames)
                    explosion_index.append(0)
                    explosion_x.append(player.collosion.x +  Player.avatar.get_rect().width)
                    explosion_y.append(player.collosion.y -  Player.avatar.get_rect().height - 10)
                    explosion_sound.play()
                    if player.life > 1:
                        player.life -= 1  # יורד לו חיים
                        player.og_place() # מחזיר את החללית למיקום המקורי
                    else:
                        player.life -= 1  # מוריד ל0
                        player.is_died = True  # הורג אותו
                        player.destroyed_time = pygame.time.get_ticks()  # שומר את זמן ההשמדה

        for laser_to_remove_index in reversed(remove_enemy_lasers):  # מסיר את הלייזרים של האויב שיצאו מהמסך
            enemy.lasers.pop(laser_to_remove_index) #מוריד את הלייזר מספר
            remove_enemy_lasers.remove(laser_to_remove_index)

    for i in reversed(list(remove_enemies)):  # מסיר את האויבים המתים מהמסך
        enemies.pop(i)

    power_up_remove = [] #
    for i in range(len(power_up_dropper)):
        power_up_Ys[i] += 2

        drop_collosion = power_up_dropper[i].get_rect(topleft=(power_up_Xs[i], power_up_Ys[i]))

        if power_up_Ys[i] > window_height:
            power_up_remove.append(i)
        if drop_collosion.colliderect(player.collosion) and not player.is_died:
            power_up_remove.append(i)
            power_up_sound.play()
            if power_up_dropper[i] == power_up_list[0]:  # אם נוגע ביכולת המיוחדת של הברק
                score += 100
                if player.lasers_count < 5:
                    player.lasers_count += 1
                else:
                    score += 120
            if power_up_dropper[i] == power_up_list[1]:  # אם נוגע ביכולת המיוחדת של הכוכב
                score += 500
            if power_up_dropper[i] == power_up_list[2]:  # אם נוגע ביכולת המיוחדת של התרופה
                score += 15
                player.life += 1
            if power_up_dropper[i] == power_up_list[3]:  # אם נוגע ביכולת המיוחדת של המגן
                if shield_life != 0:
                    score += 60
                score += 45
                shield_active = True
                shield_sounds[0].play()
                shield_duration = 10
                shield_life = 3

    for i in reversed(power_up_remove):
        power_up_dropper.pop(i)
        power_up_Xs.pop(i)
        power_up_Ys.pop(i)

    if wave.finished and pygame.time.get_ticks() - wave.ending_time >= wave.time_between_waves:
        wave.counter += 1
        wave.finished = False
        Enemy.num_enemies_per_wave += 1
        Enemy.enemies_destroyed = 0
        create_enemies()

    if len(enemies) == 0 and wave.counter < wave.max_wave and not wave.finished:
        wave.finished = True
        wave.ending_time = pygame.time.get_ticks()

    backround_y -= 4
    if backround_y <= -backround_image.get_height():
        backround_y = 0

    window.blit(background_surface, (0, backround_y))
    
    if wave.counter == wave.max_wave:
        is_boss_text_on = True

    if is_boss_text_on and len(enemies) == 0 and len(power_up_dropper) == 0 and pygame.time.get_ticks() - wave.ending_time >= wave.time_between_waves:
        current_time = pygame.time.get_ticks()

        if boss_text_i == 0:
            if boss.text_time == 0:
                boss.text_time = current_time #מופעל בלולאת הצגת הטקסט
                lasers.clear()
                enemies.clear()
                power_up_dropper.clear()
                explosion_effect.clear()
                explosion_x.clear()
                explosion_y.clear()
                is_boss_text_on = True

            if current_time - boss.text_time >= 2000:
                boss_text_i += 1 #הופעל בלולאת הוצאת הטקסט
                boss.text_time = 0
                is_boss_text_on = False

            wave_text = wave_font.render("Boss fight!", False, colors.red.value)
            window.blit(wave_text, wave_text.get_rect(center=(window_width // 2, window_height // 2)))

        elif boss_text_i == 1:
            boss_text_i += 1
            player.og_place()

        if player.collosion.colliderect(boss.collosion) and not player.is_died:  # מופעל רק שיורים בבוס
            if not has_kamikazed:
                explosion_effect.append(explosion_frames)
                explosion_index.append(0)
                explosion_x.append(boss.movement.x)
                explosion_y.append(boss.movement.y)
                explosion_sound.play()
                has_kamikazed = True

            else:
                player.life = 0
                shield_life = 0
                shield_active = False
                player.is_died = True
                player.destroyed_time = pygame.time.get_ticks()

        if boss.hp <= 0:
            if text_i == 0:
                lasers.clear()
                enemies.clear()
                boss.lasers.clear()
                power_up_dropper.clear()
                explosion_effect.clear()
                wave_text = wave_font.render("you WON!!", False, colors.blue_green.value)
                window.blit(wave_text,wave_text.get_rect(center=(window_width // 2, window_height // 2)))

            elif text_i == 1:
                score += 1000  # תוספת נקודות על הבוס
                pygame.time.delay(3000)  # ההמתנה לטקסט ניצחון
                wave_text = wave_font.render("turning your life,", False, colors.green.value)
                window.blit(wave_text,wave_text.get_rect(center=(window_width // 2, window_height // 2 - 100)))
                wave_text = wave_font.render("to score.", False, colors.dark_gray.value)
                window.blit(wave_text ,wave_text.get_rect(center=(window_width // 2, window_height // 2 + 100)))

            elif text_i == 2:
                score += (player.life + shield_life) * 15  # מוסיף ציון לכל חיים
                life_to_score_sound.play()
                pygame.time.delay(3000)  # המתנה לטקסט הפיכת חיים לניקוד ולניקוד להופיע

            elif text_i == 3:
                wave_text = wave_font.render("final score:", False, colors.blue.value)
                window.blit(wave_text,wave_text.get_rect(center=(window_width // 2, window_height // 2 - 100)))
                wave_text = wave_font.render(str(score), False, colors.orange.value)
                window.blit(wave_text,wave_text.get_rect(center=(window_width // 2, window_height // 2 + 100)))

            elif text_i == 4:
                pygame.time.delay(3000)  # המתנה לטקסט ציון סופי

            if text_i < 5:  # מוודא שהטקסט רץ רק עד סופו ולא ממשיך לנצח
                text_i += 1  # מקדם את שומר הצגת הטקסט בסדר, נכנס לתנאי הבא אם שווה ל5

            if pygame.time.get_ticks() - player.destroyed_time >= 2 and text_i == 5:
                update_high_scores(score)
                Main_menu()
                player = Player()
                explosion_index.clear()
                explosion_x.clear()
                explosion_y.clear()
                text_i = 0
                boss_text_i = 0
                boss.text_time = 0
                lasers_x.clear()
                lasers_y.clear()
                power_up_Xs.clear()
                power_up_Ys.clear()
                boss.movement.x = window_width / 2 - Boss.green_boss_pic.get_width() / 2
                boss.movement.y = -Boss.green_boss_pic.get_height() - 100
                wave.counter = 1  # מאפס את כמות הגלים
                Enemy.num_enemies_per_wave = 1  # מאפס את כמות האוייבים פר גל
                score = 0
                shield_duration = 10
                shield_life = 3
                shield_active = False
                shield_frame_index = 0
                boss.hp = 100
                player = Player()
        else:
            if not is_boss_text_on:
                if boss.movement.y < Boss.green_boss_pic.get_height() + 50:
                    boss.movement.y += boss.movement.dy
                else:
                    boss.movement.x += boss.movement.dx

                if boss.movement.x <= 0:
                    boss.movement.dx = 2

                if boss.movement.x >= window_width - Boss.green_boss_pic.get_width():
                    boss.movement.dx = -2

                if boss.hit:
                    boss.hit = False
                    boss_hit_pic = pygame.Surface.copy(Boss.green_boss_pic)
                    boss_hit_pic.fill(colors.red.value, special_flags=pygame.BLEND_RGB_MULT) #מחזיר מלבן, ולא משטח
                    window.blit(boss_hit_pic,(boss.movement.x, boss.movement.y))
                else:
                    window.blit(Boss.green_boss_pic, (boss.movement.x, boss.movement.y))

                if text_i == 0 and not is_boss_text_on:  # אם הטקסט לא מופעל
                    bar_width = 300  # עובי הבר
                    bar_height = 20  # גובה הבר
                    """
                    :מעדכן את החיים של הבוס
                    מעגל את עובי הבר * יחס הבוס
                    """
                    remaining_hp = int(bar_width * (boss.hp / Boss.max_hp))
                    pygame.draw.rect(window, colors.black.value,
                                     [window_width // 2 - bar_width // 2, 50, bar_width, bar_height])  # רקע חיי הבוס
                    pygame.draw.rect(window, colors.red.value,
                                     [window_width // 2 - bar_width // 2, 50, remaining_hp, bar_height])  # חיי הבוס

                if current_time - boss.last_time_laser >= boss.shoot_cooldown and boss.hp > 0:
                    if current_time - boss.last_time_shoot >= boss.lasers_cooldown:
                        boss.last_time_shoot = current_time
                        if len(boss.lasers) < 6:
                            boss.lasers.append(
                                Laser(Enemy.laser_pic,Movement(boss.movement.x + Boss.green_boss_pic.get_width() / 2 - Enemy.laser_pic.get_width() / 2,
                                boss.movement.y + Boss.green_boss_pic.get_height(), 0, 9)))
                            laser_sound.play()
                        else:
                            boss.last_time_laser = current_time

                remove_boss_lasers = []

                for i in range(len(boss.lasers)):
                    boss.lasers[i].movement.y += boss.lasers[i].movement.dy
                    boss_laser_collosion = boss.lasers[i].pic.get_rect(topleft=(boss.lasers[i].movement.x, boss.lasers[i].movement.y))

                    if boss_laser_collosion.colliderect(player.collosion):
                        remove_boss_lasers.append(i)
                        if shield_active:
                            shield_life -= 1
                            shield_frame_index -= 1
                            if shield_life == 0:
                                shield_active = False
                                shield_sounds[1].play()
                        else:
                            explosion_effect.append(explosion_frames)
                            explosion_index.append(0)
                            explosion_x.append(player.collosion.x +  Player.avatar.get_rect().width)
                            explosion_y.append(player.collosion.y -  Player.avatar.get_rect().height - 10)
                            explosion_sound.play()
                            if player.life > 1:
                                player.got_hit()
                            else:
                                player.life -= 1  # מוריד ל0
                                player.is_died = True  # הורג אותו
                                player.destroyed_time = pygame.time.get_ticks()  # שומר את זמן ההשמדה

                    elif boss.lasers[i].movement.y > window_height:
                        remove_boss_lasers.append(i)

                for i in reversed(remove_boss_lasers):
                    boss.lasers.pop(i)

                for i in range(len(boss.lasers)):
                    window.blit(boss.lasers[i].pic, (boss.lasers[i].movement.x, boss.lasers[i].movement.y))

    if wave.finished:
        wave_text = wave_font.render("Wave: " + str(wave.counter), True, colors.white.value)
        wave_text_rect = wave_text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(wave_text, wave_text_rect)

    display_life()
    display_score()

    for i in range(len(power_up_dropper)):
        window.blit(power_up_dropper[i], (power_up_Xs[i], power_up_Ys[i]))

    for i in range(len(lasers)):
        if text_i != 0:
            lasers.clear()
            break
        window.blit(lasers[i], (lasers_x[i], lasers_y[i]))

    for enemy in enemies:
        for i in range(len(enemy.lasers)):
            window.blit(enemy.lasers[i].pic, (enemy.lasers[i].movement.x, enemy.lasers[i].movement.y))

        window.blit(enemy.pic, (enemy.movement.x, enemy.movement.y))

    for i in range(len(explosion_effect)):
        frame = explosion_effect[i][explosion_index[i]]
        frame_rect = frame.get_rect(center=(explosion_x[i], explosion_y[i]))
        window.blit(frame, frame_rect)

    if (not player.is_died) and text_i == 0 and (not is_boss_text_on):  # אם לא מתים ולא בהצגת המסך הסופי, או בטקסט קרב בוס
        window.blit(Player.avatar, (player.movement.x, player.movement.y))  # תצייר את הספינה
        if shield_active:
            shield_duration -= 1
            if shield_frame_index < shield_life - 1 and shield_duration <= 0:
                shield_frame_index += 1
                shield_duration = 10

            shield_frame = shield_farmes[shield_frame_index]
            shield_x = player.movement.x + ( Player.avatar.get_rect().width - shield_frame.get_width()) // 2
            shield_y = player.movement.y + ( Player.avatar.get_rect().height - shield_frame.get_height()) // 2
            window.blit(shield_frame, (shield_x, shield_y))

    if player.is_died:
        if pygame.time.get_ticks() - player.destroyed_time >= 2:
            Main_menu()
            text_i = 0
            boss_text_i = 0
            boss.text_time = 0
            is_boss_text_on = False
            lasers.clear()
            lasers_x.clear()
            lasers_y.clear()
            enemies.clear()
            boss.lasers.clear()
            power_up_dropper.clear()
            power_up_Xs.clear()
            power_up_Ys.clear()
            shield_active = False
            has_kamikazed = False
            explosion_effect.clear()
            explosion_x.clear()
            explosion_y.clear()
            explosion_index.clear()
            boss.movement.x = window_width / 2 - Boss.green_boss_pic.get_width() / 2
            boss.movement.y = -Boss.green_boss_pic.get_height() - 100
            wave.counter = 1  # מאפס את כמות הגלים
            Enemy.num_enemies_per_wave = 1  # מאפס את כמות האוייבים פר גל
            score = 0
            shield_duration = 10
            shield_life = 3
            shield_active = False
            has_kamikazed = False
            shield_frame_index = 0
            boss.hp = 100
            player = Player()

    pygame.display.update()

pygame.quit()
exit()
