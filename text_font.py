import pygame as pg
from colors import questionColor, answerColor,answerArrowColor

def load_font(fontName, size):
    #print(pg.font.get_fonts())
    if fontName in pg.font.get_fonts():
        font = pg.font.SysFont(fontName, size)
    else:
        try:
            font = pg.font.Font(fontName, size)
        except:
            font = pg.font.Font(None, size)

    # get the height of the font
    #self.fontHeight = self.font.size("Tg")[1]

    return font


# draw some text into an area of a surface
# automatically wraps words
# returns height of text ////any text that didn't get blitted
def drawText(surface, text, color, rect, fontName, fontSize, aa=False, bkg=None):
    font = load_font(fontName, fontSize)
    rect = pg.Rect(rect)
    y = rect.top
    lineSpacing = -2

    fontHeight = font.size("Tg")[1]
    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i1 = text.rfind("\n", 0, i) + 1
            i2 = text.rfind(" ", 0, i) + 1
            if i1 > 0:
                i = i1
            else:
                i = i2
        else:
            i1 = text.find("\n") + 1
            if i1 > 0:
                i = i1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            t = text[:i].strip()
            image = font.render(t, aa, color)
            #image = font.render(t.encode('utf8'), aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return y
    #return text
