"""layout.py - page layout of the miniVIC manual, in the style of the 1976 Apple-1 Operation Manual:
cream paper, typewriter body text, Bookman headings, "SECTION I" chapter openings, ruled tables.

The content (content.py) is written with the small helpers defined here (H1, H2, P, TBL, ...)."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                Image, PageBreak, NextPageTemplate, KeepTogether, Flowable, CondPageBreak,
                                Preformatted)
from reportlab.platypus.tableofcontents import TableOfContents

HERE = Path(__file__).resolve().parent
IMG = HERE / 'img'

# ---------------------------------------------------------------- fonts
FONTS = 'C:/Windows/Fonts/'
pdfmetrics.registerFont(TTFont('Type', FONTS + 'cour.ttf'))
pdfmetrics.registerFont(TTFont('Type-B', FONTS + 'courbd.ttf'))
pdfmetrics.registerFont(TTFont('Type-I', FONTS + 'couri.ttf'))
pdfmetrics.registerFont(TTFont('Type-BI', FONTS + 'courbi.ttf'))
addMapping('Type', 0, 0, 'Type'); addMapping('Type', 1, 0, 'Type-B')
addMapping('Type', 0, 1, 'Type-I'); addMapping('Type', 1, 1, 'Type-BI')
pdfmetrics.registerFont(TTFont('Book', FONTS + 'BOOKOS.TTF'))
pdfmetrics.registerFont(TTFont('Book-B', FONTS + 'BOOKOSB.TTF'))
pdfmetrics.registerFont(TTFont('Book-I', FONTS + 'BOOKOSI.TTF'))
pdfmetrics.registerFont(TTFont('Book-BI', FONTS + 'BOOKOSBI.TTF'))
addMapping('Book', 0, 0, 'Book'); addMapping('Book', 1, 0, 'Book-B')
addMapping('Book', 0, 1, 'Book-I'); addMapping('Book', 1, 1, 'Book-BI')

# ---------------------------------------------------------------- colours
# MANUAL_PRINT=1 makes the print edition: white paper, black ink, pictures in grey tones
import os
PRINT = os.environ.get('MANUAL_PRINT') == '1'
if PRINT:
    PAPER = colors.white
    PAPER_DARK = colors.HexColor('#E4E4E4')
    INK = colors.black
    INK_SOFT = colors.HexColor('#505050')
else:
    PAPER = colors.HexColor('#FAF5E8')
    PAPER_DARK = colors.HexColor('#EDE4CC')
    INK = colors.HexColor('#2A2118')
    INK_SOFT = colors.HexColor('#5A4A38')


def picture(path):
    """the picture to use: the original, or a grey copy for the print edition (white stays white)"""
    path = Path(path)
    if not PRINT:
        return path
    from PIL import Image as PI, ImageOps
    out = HERE / 'img' / 'grey' / (path.parent.name + '_' + path.stem + '.png')
    if not out.exists() or out.stat().st_mtime < path.stat().st_mtime:
        out.parent.mkdir(parents=True, exist_ok=True)
        im = PI.open(path).convert('RGBA')
        bg = PI.new('RGBA', im.size, (255, 255, 255, 255))
        g = PI.alpha_composite(bg, im).convert('L')
        g = g.point(lambda v: 255 if v > 225 else v)        # paper tint of the engraving -> white
        g.save(out)
    return out

PAGE_W, PAGE_H = A4
ML, MR, MT, MB = 22 * mm, 22 * mm, 20 * mm, 20 * mm
BODY_W = PAGE_W - ML - MR

# ---------------------------------------------------------------- styles
S = {}
S['body'] = ParagraphStyle('body', fontName='Type', fontSize=9, leading=12.2, textColor=INK,
                           alignment=TA_LEFT, spaceAfter=5)
S['bullet'] = ParagraphStyle('bullet', parent=S['body'], leftIndent=14, bulletIndent=3, spaceAfter=2)
S['note'] = ParagraphStyle('note', parent=S['body'], fontSize=8.5, leading=11.5, leftIndent=10, rightIndent=10,
                           borderColor=INK, borderWidth=0.6, borderPadding=6, spaceBefore=6, spaceAfter=10)
S['cell'] = ParagraphStyle('cell', fontName='Type', fontSize=7.8, leading=9.6, textColor=INK)
S['cellb'] = ParagraphStyle('cellb', parent=S['cell'], fontName='Type-B')
S['cellc'] = ParagraphStyle('cellc', parent=S['cell'], alignment=TA_CENTER)
S['code'] = ParagraphStyle('code', fontName='Type-B', fontSize=8.4, leading=10.4, textColor=INK)
S['caption'] = ParagraphStyle('caption', fontName='Type-I', fontSize=7.8, leading=9.5, textColor=INK_SOFT,
                              alignment=TA_CENTER, spaceBefore=2, spaceAfter=8)
S['sec_num'] = ParagraphStyle('sec_num', fontName='Book-B', fontSize=13, leading=16, alignment=TA_CENTER,
                              textColor=INK, spaceAfter=2)
S['sec_title'] = ParagraphStyle('sec_title', fontName='Book-B', fontSize=21, leading=25, alignment=TA_CENTER,
                                textColor=INK, spaceAfter=4)
S['h2'] = ParagraphStyle('h2', fontName='Book-B', fontSize=12.5, leading=15, textColor=INK, spaceBefore=12,
                         spaceAfter=6)
S['h3'] = ParagraphStyle('h3', fontName='Type-B', fontSize=9.6, leading=12, textColor=INK, spaceBefore=8,
                         spaceAfter=4)
S['toc0'] = ParagraphStyle('toc0', fontName='Type-B', fontSize=9.6, leading=13, leftIndent=0, spaceBefore=6)
S['toc1'] = ParagraphStyle('toc1', fontName='Type', fontSize=8.8, leading=11.2, leftIndent=18)
S['toc_title'] = ParagraphStyle('toc_title', parent=S['sec_title'], spaceAfter=14)


class Rule(Flowable):
    """horizontal double rule, like the frame of the cover"""
    def __init__(self, width=BODY_W, double=True, space=6):
        super().__init__()
        self.width, self.double, self.space = width, double, space

    def wrap(self, aw, ah):
        return self.width, self.space * 2 + 4

    def draw(self):
        c = self.canv
        c.setStrokeColor(INK)
        y = self.space + 4
        c.setLineWidth(1.6); c.line(0, y, self.width, y)
        if self.double:
            c.setLineWidth(0.5); c.line(0, y - 3, self.width, y - 3)


class Underline(Flowable):
    def __init__(self, width=BODY_W):
        super().__init__(); self.width = width

    def wrap(self, aw, ah):
        return self.width, 3

    def draw(self):
        self.canv.setStrokeColor(INK); self.canv.setLineWidth(0.6); self.canv.line(0, 2, self.width, 2)


class Placeholder(Flowable):
    """an empty area; its page number is recorded so that build.py can draw a schematic page on it"""
    REG = {}

    def __init__(self, key, height):
        super().__init__(); self.key, self.height, self.width = key, height, 0

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.height

    def draw(self):
        x, y = self.canv.absolutePosition(0, 0)
        Placeholder.REG[self.key] = (self.canv.getPageNumber(), x, y, self.width, self.height)


# ---------------------------------------------------------------- helpers used by content.py
_counter = {'n': 0}


def _key():
    _counter['n'] += 1
    return 'k%d' % _counter['n']


def H1(num, title):
    """chapter opening: new page, 'SECTION I' and the title, double rule"""
    p = Paragraph(title.upper(), S['sec_title'])
    p._toc = (0, f'{num}. {title.upper()}', _key())
    return [NextPageTemplate('body'), PageBreak(), Spacer(1, 18), Paragraph(SECTION_WORD[0] + ' ' + num, S['sec_num']),
            p, Rule(), Spacer(1, 8)]


SECTION_WORD = ['SECTION']


def H2(title, toc=True):
    p = Paragraph(title.upper(), S['h2'])
    if toc:
        p._toc = (1, title, _key())
    return [CondPageBreak(60 * mm), p, Underline(), Spacer(1, 4)]


def H3(title):
    return [CondPageBreak(30 * mm), Paragraph(title, S['h3'])]


def P(text):
    return [Paragraph(text, S['body'])]


def NOTE(text):
    return [Paragraph(text, S['note'])]


def B(items):
    return [Paragraph(t, S['bullet'], bulletText='\u2022') for t in items]


def CODE(text, width=BODY_W):
    """a typed example in a box"""
    pre = Preformatted(text.strip('\n'), S['code'])
    t = Table([[pre]], colWidths=[width])
    t.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.6, INK), ('BACKGROUND', (0, 0), (-1, -1), PAPER_DARK),
                           ('LEFTPADDING', (0, 0), (-1, -1), 8), ('TOPPADDING', (0, 0), (-1, -1), 5),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    return [Spacer(1, 2), t, Spacer(1, 8)]


def _cell(v, style):
    if isinstance(v, Flowable):
        return v
    return Paragraph(str(v), style)


def TBL(rows, widths, header=True, spans=(), center_cols=(), bold_first=False, font=None, repeat=1):
    """ruled table; widths in mm, or fractions (sum 1.0) of the body width"""
    if sum(widths) <= 1.01:
        widths = [w * BODY_W for w in widths]
    else:
        widths = [w * mm for w in widths]
    data = []
    for r, row in enumerate(rows):
        line = []
        for c, v in enumerate(row):
            st = S['cellb'] if (header and r == 0) or (bold_first and c == 0) else (
                S['cellc'] if c in center_cols else S['cell'])
            if font:
                st = ParagraphStyle('x', parent=st, fontSize=font, leading=font * 1.22)
            line.append(_cell(v, st))
        data.append(line)
    t = Table(data, colWidths=widths, repeatRows=repeat if header else 0)
    st = [('GRID', (0, 0), (-1, -1), 0.5, INK), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
          ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4),
          ('TOPPADDING', (0, 0), (-1, -1), 2.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]
    if header:
        st += [('BACKGROUND', (0, 0), (-1, 0), PAPER_DARK), ('LINEBELOW', (0, 0), (-1, 0), 1.2, INK)]
    for sp in spans:
        st.append(('SPAN',) + tuple(sp))
    t.setStyle(TableStyle(st))
    return [t, Spacer(1, 9)]


def IMG_(path, width_mm, caption=None, border=True):
    from PIL import Image as PI
    path = picture(path)
    w, h = PI.open(path).size
    wd = width_mm * mm
    im = Image(str(path), width=wd, height=wd * h / w)
    out = im
    if border:
        t = Table([[im]], colWidths=[wd + 4])
        t.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.8, INK), ('LEFTPADDING', (0, 0), (-1, -1), 2),
                               ('RIGHTPADDING', (0, 0), (-1, -1), 2), ('TOPPADDING', (0, 0), (-1, -1), 2),
                               ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
        out = t
    items = [out]
    if caption:
        items.append(Paragraph(caption, S['caption']))
    return [KeepTogether(items)]


def IMGROW(paths_caps, width_mm, gap=5):
    """pictures side by side, each with its caption"""
    from PIL import Image as PI
    cells, caps = [], []
    for path, cap in paths_caps:
        path = picture(path)
        w, h = PI.open(path).size
        cells.append(Image(str(path), width=width_mm * mm, height=width_mm * mm * h / w))
        caps.append(Paragraph(cap or '', S['caption']))
    n = len(cells)
    t = Table([cells, caps], colWidths=[width_mm * mm + gap * mm] * n)
    t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('LEFTPADDING', (0, 0), (-1, -1), 1), ('RIGHTPADDING', (0, 0), (-1, -1), 1),
                           ('TOPPADDING', (0, 0), (-1, -1), 1), ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    return [KeepTogether([t]), Spacer(1, 4)]


def SPACE(h_mm):
    return [Spacer(1, h_mm * mm)]


def PB():
    return [PageBreak()]


# ---------------------------------------------------------------- document
class ManualDoc(BaseDocTemplate):
    def __init__(self, filename, lang, meta, cover_fn, **kw):
        super().__init__(filename, pagesize=A4, leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
                         title=meta['title'], author=meta['author'], subject=meta['subject'], **kw)
        self.lang, self.meta = lang, meta
        body = Frame(ML, MB, BODY_W, PAGE_H - MT - MB, id='body', leftPadding=0, rightPadding=0,
                     topPadding=0, bottomPadding=0)
        cover = Frame(ML, MB, BODY_W, PAGE_H - MT - MB, id='cover')
        self.addPageTemplates([
            PageTemplate('cover', [cover], onPage=cover_fn),
            PageTemplate('body', [body], onPage=self._page),
            PageTemplate('plain', [body], onPage=self._paper),
        ])

    def _paper(self, c, doc):
        c.saveState()
        c.setFillColor(PAPER); c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        c.restoreState()

    def _page(self, c, doc):
        self._paper(c, doc)
        c.saveState()
        c.setFillColor(INK); c.setFont('Type', 8.5)
        c.drawCentredString(PAGE_W / 2, 11 * mm, '- %d -' % doc.page)
        c.setFont('Type', 7); c.setFillColor(INK_SOFT)
        c.drawString(ML, PAGE_H - 11 * mm, self.meta['running'])
        c.drawRightString(PAGE_W - MR, PAGE_H - 11 * mm, self.meta['version'])
        c.setStrokeColor(INK_SOFT); c.setLineWidth(0.4)
        c.line(ML, PAGE_H - 12.5 * mm, PAGE_W - MR, PAGE_H - 12.5 * mm)
        c.restoreState()

    def afterFlowable(self, f):
        toc = getattr(f, '_toc', None)
        if toc:
            level, text, key = toc
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=level == 0)
            self.notify('TOCEntry', (level, text, self.page, key))


def make_toc(title):
    toc = TableOfContents(dotsMinLevel=0)
    toc.levelStyles = [S['toc0'], S['toc1']]
    return [NextPageTemplate('body'), PageBreak(), Spacer(1, 18), Paragraph(title, S['toc_title']), Rule(),
            Spacer(1, 6), toc]
