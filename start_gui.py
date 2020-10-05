import pygame as pg
import text_font
from sound import soundHandler

def get_players_number(SCREEN, clock):
    #print('before load images')
    pg.init()
    pg.mixer.init()
    colorKey = (255, 255, 255)
    cancelImg = pg.image.load('images/cancel.png')
    if cancelImg.get_alpha():
        cancelImg = cancelImg.convert_alpha()
    else:
        cancelImg = cancelImg.convert()
        cancelImg.set_colorkey(colorKey)

    while True:
        #print('before display')
        user_text = run_start(SCREEN, cancelImg, clock)
        try:
            players = int(user_text)
            if players == -1:
                return -1
            if players > 0 and players < 6:
                return players
            else:
                soundHandler.play('error-beep')
                #errSound1.play()

        except ValueError:
            soundHandler.play('error-beep')
            #errSound1.play()
            pass

    return players


def run_start(SCREEN, cancelImg, clock):
    r = SCREEN.get_rect()
    view = SCREEN.subsurface(100,100, r.width - 200, r.height - 200)
    #print('before arial 1')
    base_font = text_font.load_font('arial', 24)
    user_text = ''
    description_text = 'Unesi broj igraca (1-5) ili Q za kraj.'
    time_delta = clock.tick(60)/1000.0
    #print('before is_running = True')
    is_running = True
    cancelrect = pg.Rect(r.width - 100 - cancelImg.get_width(), 100, cancelImg.get_width(), cancelImg.get_height())
    input_rect = pg.Rect(200,200, 140, 32)
    border_color = pg.Color('lightblue3')
    while is_running:
        pos = pg.mouse.get_pos()
        pressed1, pressed2, pressed3 = pg.mouse.get_pressed()
        # Check if the rect collided with the mouse pos
        # and if the left mouse button was pressed.
        if cancelrect.collidepoint(pos) and pressed1:
            return '-1'
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False
                return '-1'

            if event.type == pg.QUIT:
                is_running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    is_running = False
                    return '-1'
                if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                    is_running = False
                    return user_text

                if event.key == pg.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        view.fill((0,0,0))
        pg.draw.rect(view, border_color, input_rect, 2)
        text_surface = base_font.render(user_text, True, (255,255,255))
        #print('before print description')
        description_surface = base_font.render(description_text, True, (255,255,255))

        view.blit(description_surface, (input_rect.x, input_rect.y - 35))
        view.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max (100, text_surface.get_width() + 10)
        SCREEN.blit(cancelImg, (cancelrect.x, cancelrect.y))

        #print('before pg.display.flip()')
        pg.display.flip()
        clock.tick()

    return user_text