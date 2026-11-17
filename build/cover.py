"""cover.py - the cover, an homage to the Apple-1 Operation Manual (1976): an engraving in an ornamented frame
with a ribbon banner and a motto, the title in Bookman inside a double-ruled frame on cream paper."""
from reportlab.lib.units import mm
from layout import PAGE_W, PAGE_H, PAPER, INK, INK_SOFT, IMG, picture

COVER_TEXT = {
    'en': dict(title1='MiniVIC', title2='OPERATION', title3='MANUAL', ribbon='BOOGS77  ·  MiniVIC',
               motto='A SMALL MACHINE FOR PLAYING, WRITING AND COUNTING',
               chips='W65C02S · TMS9918A · 2 × AY-3-8910 · SD CARD',
               url='https://github.com/Boogs77/miniVIC_65c02',
               foot='BIOS 16.11.26 KEYB/SD R2  —  2026'),
    'it': dict(title1='MiniVIC', title2='MANUALE', title3="D'USO", ribbon='BOOGS77  ·  MiniVIC',
               motto='UNA PICCOLA MACCHINA PER GIOCARE, SCRIVERE E CONTARE',
               chips='W65C02S · TMS9918A · 2 × AY-3-8910 · SD CARD',
               url='https://github.com/Boogs77/miniVIC_65c02',
               foot='BIOS 16.11.26 KEYB/SD R2  —  2026'),
}


def _ribbon(c, cx, y, w, h, text):
    """banner with folded tails, drawn in ink lines on paper"""
    tail = 16 * mm
    drop = 3.2 * mm
    x1, x2 = cx - w / 2, cx + w / 2
    c.setStrokeColor(INK); c.setLineWidth(0.9)
    # tails (behind)
    for side in (-1, 1):
        xe = x1 if side < 0 else x2
        xo = xe + side * tail
        p = c.beginPath()
        p.moveTo(xe - side * 6 * mm, y - drop)
        p.lineTo(xo, y - drop)
        p.lineTo(xo - side * 4 * mm, y - drop + h / 2)
        p.lineTo(xo, y - drop + h)
        p.lineTo(xe, y - drop + h)
        p.close()
        c.setFillColor(PAPER); c.drawPath(p, stroke=1, fill=1)
        # shading lines on the tail
        c.setLineWidth(0.35)
        for k in range(1, 6):
            yy = y - drop + k * h / 6
            c.line(xe + side * 1.5 * mm, yy, xo - side * (4 * mm * (1 - abs(2 * k / 6 - 1))) - side * 1 * mm, yy)
        c.setLineWidth(0.9)
        # fold triangle
        q = c.beginPath()
        q.moveTo(xe, y); q.lineTo(xe, y - drop); q.lineTo(xe - side * 6 * mm, y - drop); q.close()
        c.setFillColor(INK); c.drawPath(q, stroke=1, fill=1)
    # front band
    c.setFillColor(PAPER)
    c.rect(x1, y, w, h, stroke=1, fill=1)
    c.setLineWidth(0.4)
    c.line(x1 + 2, y + 2.2, x2 - 2, y + 2.2); c.line(x1 + 2, y + h - 2.2, x2 - 2, y + h - 2.2)
    c.setFillColor(INK); c.setFont('Book-B', 11.5)
    c.drawCentredString(cx, y + h / 2 - 4, text)


def _corner(c, x, y, r):
    c.setLineWidth(0.7)
    c.circle(x, y, r, stroke=1, fill=0)
    c.circle(x, y, r * 0.45, stroke=0, fill=1)


def _hatch(c, poly, angle, step, width=0.3):
    """parallel lines clipped to a polygon: the engraver's shading"""
    import math
    c.saveState()
    p = c.beginPath(); p.moveTo(*poly[0])
    for pt in poly[1:]:
        p.lineTo(*pt)
    p.close()
    c.clipPath(p, stroke=0, fill=0)
    xs = [q[0] for q in poly]; ys = [q[1] for q in poly]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    r = math.hypot(max(xs) - min(xs), max(ys) - min(ys))
    a = math.radians(angle); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    c.setLineWidth(width)
    k = -r
    while k <= r:
        c.line(cx + nx * k - ux * r, cy + ny * k - uy * r, cx + nx * k + ux * r, cy + ny * k + uy * r)
        k += step
    c.restoreState()


def _chip(c, x, y, w, h):
    """a 40-pin DIP chip marked 6502, seen from above, drawn with engraved lines"""
    def poly(pts, stroke=1, fill=0, lw=0.6):
        p = c.beginPath(); p.moveTo(*pts[0])
        for pt in pts[1:]:
            p.lineTo(*pt)
        p.close()
        c.setLineWidth(lw); c.drawPath(p, stroke=stroke, fill=fill)

    c.saveState()
    c.setStrokeColor(INK); c.setFillColor(INK)
    L, Wd = 52 * mm, 14 * mm                      # body
    leg, lw_ = 3.4 * mm, 1.3 * mm                 # pin length and width
    bx = x + (w - L) / 2
    by = y + (h - Wd) / 2 - 3.5 * mm
    pitch = L / 20.0
    off = 1.4 * mm                                # shadow offset (light from the top left)
    # shadow of body and pins, cross hatched
    sh = [(bx + off, by - off), (bx + L + off, by - off), (bx + L + off, by + Wd - off), (bx + off, by + Wd - off)]
    _hatch(c, sh, 0, 0.6, 0.3); _hatch(c, sh, 90, 0.9, 0.22)
    for i in range(20):
        px = bx + (i + 0.5) * pitch
        for (y0, d) in ((by, -1), (by + Wd, 1)):
            q = [(px - lw_ / 2 + off, y0 - off), (px + lw_ / 2 + off, y0 - off),
                 (px + lw_ / 2 + off, y0 + d * leg - off), (px - lw_ / 2 + off, y0 + d * leg - off)]
            _hatch(c, q, 0, 0.6, 0.3)
    # pins: wide shoulder near the body, narrow leg outside
    for i in range(20):
        px = bx + (i + 0.5) * pitch
        for (y0, d) in ((by, -1), (by + Wd, 1)):
            q = [(px - lw_ / 2, y0), (px + lw_ / 2, y0), (px + lw_ / 2, y0 + d * 1.2 * mm),
                 (px + 0.3 * mm, y0 + d * 1.6 * mm), (px + 0.3 * mm, y0 + d * leg),
                 (px - 0.3 * mm, y0 + d * leg), (px - 0.3 * mm, y0 + d * 1.6 * mm), (px - lw_ / 2, y0 + d * 1.2 * mm)]
            c.setFillColor(PAPER); poly(q, 1, 1, 0.45); c.setFillColor(INK)
            c.setLineWidth(0.25)
            c.line(px + 0.35 * mm, y0 + d * 0.2 * mm, px + 0.35 * mm, y0 + d * 1.1 * mm)
    # body with bevelled edges: top and left light, bottom and right in shadow
    bev = 1.6 * mm
    o = [(bx, by), (bx + L, by), (bx + L, by + Wd), (bx, by + Wd)]
    i_ = [(bx + bev, by + bev), (bx + L - bev, by + bev), (bx + L - bev, by + Wd - bev), (bx + bev, by + Wd - bev)]
    c.setFillColor(PAPER); poly(o, 1, 1, 0.9); c.setFillColor(INK)
    bottom = [o[0], o[1], i_[1], i_[0]]
    right = [o[1], o[2], i_[2], i_[1]]
    left = [o[3], o[0], i_[0], i_[3]]
    _hatch(c, bottom, 0, 0.45, 0.35)
    _hatch(c, right, 90, 0.5, 0.35)
    _hatch(c, left, 90, 1.1, 0.2)
    poly(i_, 1, 0, 0.5)
    for k in range(4):
        c.setLineWidth(0.4); c.line(o[k][0], o[k][1], i_[k][0], i_[k][1])
    # light shading on the top face, along the bottom and right edges
    _hatch(c, [i_[0], i_[1], (i_[1][0], i_[1][1] + 1.6 * mm), (i_[0][0], i_[0][1] + 1.6 * mm)], 0, 0.8, 0.2)
    # notch on the left end, pin-1 dot, type number
    p = c.beginPath()
    nr = 2.0 * mm
    p.arc(i_[0][0] - nr, by + Wd / 2 - nr, i_[0][0] + nr, by + Wd / 2 + nr, -90, 180)
    c.setLineWidth(0.6); c.drawPath(p, stroke=1, fill=0)
    c.circle(i_[0][0] + 3.2 * mm, i_[0][1] + 2.4 * mm, 0.75 * mm, stroke=0, fill=1)
    c.setFont('Book-B', 22)
    c.drawCentredString(bx + L / 2 + 1.5 * mm, by + Wd / 2 - 2.8 * mm, '6502')
    c.restoreState()

def draw_cover(lang):
    T = COVER_TEXT[lang]

    def fn(c, doc):
        c.saveState()
        c.setFillColor(PAPER); c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        c.setStrokeColor(INK); c.setFillColor(INK)
        # big double frame (like the BO6502 manual)
        fx, fy, fw, fh = 30 * mm, 42 * mm, PAGE_W - 60 * mm, PAGE_H - 92 * mm
        c.setLineWidth(3.2); c.rect(fx, fy, fw, fh)
        c.setLineWidth(1.2); c.rect(fx + 3.2 * mm, fy + 3.2 * mm, fw - 6.4 * mm, fh - 6.4 * mm)

        # small engraved plate, overlapping the top of the frame (like the logo of the Apple-1 manual)
        vw, vh = 80 * mm, 44 * mm
        vx = (PAGE_W - vw) / 2
        vy = fy + fh - vh + 12 * mm
        pad = 4 * mm
        c.setFillColor(PAPER)
        c.rect(vx - pad - 3 * mm, vy - pad - 9 * mm, vw + 2 * pad + 6 * mm, vh + 2 * pad + 9 * mm + 3 * mm,
               stroke=0, fill=1)
        c.setFillColor(INK)
        c.setLineWidth(1.8)
        c.rect(vx - pad, vy - pad - 7 * mm, vw + 2 * pad, vh + 2 * pad + 7 * mm)
        c.setLineWidth(0.6)
        c.rect(vx - pad + 1.5 * mm, vy - pad - 7 * mm + 1.5 * mm, vw + 2 * pad - 3 * mm,
               vh + 2 * pad + 7 * mm - 3 * mm)
        c.line(vx - pad + 1.5 * mm, vy - 2.2 * mm, vx + vw + pad - 1.5 * mm, vy - 2.2 * mm)
        _chip(c, vx, vy, vw, vh)
        c.setLineWidth(0.5); c.rect(vx, vy, vw, vh)
        c.setFont('Book-I', 6.2)
        c.drawCentredString(PAGE_W / 2, vy - pad - 3.2 * mm, '•  ' + T['motto'] + '  •')
        for (x, y) in [(vx - pad, vy - pad - 7 * mm), (vx + vw + pad, vy - pad - 7 * mm),
                       (vx - pad, vy + vh + pad), (vx + vw + pad, vy + vh + pad)]:
            c.setFillColor(PAPER); c.circle(x, y, 2.4 * mm, stroke=0, fill=1); c.setFillColor(INK)
            _corner(c, x, y, 2.0 * mm)
        _ribbon(c, PAGE_W / 2, vy + vh + pad - 4 * mm, 66 * mm, 8.5 * mm, T['ribbon'])

        # title
        ty = fy + 62 * mm
        c.setFont('Book-B', 30); c.drawCentredString(PAGE_W / 2, ty + 22 * mm, T['title1'])
        c.setFont('Book-B', 25)
        c.drawCentredString(PAGE_W / 2, ty + 10 * mm, T['title2'])
        c.drawCentredString(PAGE_W / 2, ty - 1 * mm, T['title3'])
        c.setLineWidth(0.8)
        c.line(PAGE_W / 2 - 30 * mm, ty - 8 * mm, PAGE_W / 2 + 30 * mm, ty - 8 * mm)
        c.setFont('Type', 8.6); c.drawCentredString(PAGE_W / 2, ty - 16 * mm, T['chips'])
        c.setFont('Type', 9); c.drawCentredString(PAGE_W / 2, fy + 14 * mm, T['url'])
        # outside the frame
        c.setFont('Type', 8); c.setFillColor(INK_SOFT)
        c.drawCentredString(PAGE_W / 2, 28 * mm, T['foot'])
        c.restoreState()
    return fn
