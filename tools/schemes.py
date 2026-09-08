# Рисует схемы-иллюстрации для уроков в img/<id>.svg. Запуск: python3 tools/schemes.py
import os

INK, YEL, MUTED, CREAM = '#1c1f2e', '#ffd84d', '#8a8f9e', '#fbf6ec'
C = {'win': '#2f6df6', 'word': '#4f46e5', 'excel': '#16a34a', 'ppt': '#ea580c'}
FONT = "Nunito, 'Segoe UI', system-ui, sans-serif"
OUT = os.path.join(os.path.dirname(__file__), '..', 'img')

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def text(x, y, s, size=14, w=600, fill=INK, anchor='start', mono=False):
    fam = "Consolas, Menlo, monospace" if mono else FONT
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>'

def rect(x, y, w, h, fill='#fff', stroke=INK, sw=2, r=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def line(x1, y1, x2, y2, stroke=INK, sw=2, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{d}/>'

def arrow(x1, y1, x2, y2, stroke=INK):
    import math
    a = math.atan2(y2 - y1, x2 - x1); L = 12
    p1 = (x2 - L * math.cos(a - 0.5), y2 - L * math.sin(a - 0.5)); p2 = (x2 - L * math.cos(a + 0.5), y2 - L * math.sin(a + 0.5))
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{stroke}" stroke-width="3" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x2} {y2} L{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f}z" fill="{stroke}"/>')

def callout(n, x, y, label='', side='right', size=14):
    s = f'<circle cx="{x}" cy="{y}" r="15" fill="{YEL}" stroke="{INK}" stroke-width="2"/>' + text(x, y + 5, str(n), 14, 800, anchor='middle')
    if label:
        if side == 'right': s += text(x + 22, y + 5, label, size, 700)
        else: s += text(x - 22, y + 5, label, size, 700, anchor='end')
    return s

def window(x, y, w, h, title, color, buttons=True):
    s = rect(x, y, w, h, '#fff', r=12)
    s += f'<path d="M{x+12} {y} h{w-24} a12 12 0 0 1 12 12 v22 h-{w} v-22 a12 12 0 0 1 12 -12z" fill="{color}"/>'
    s += line(x, y + 34, x + w, y + 34)
    s += text(x + 14, y + 23, title, 14, 700, '#fff')
    if buttons:
        s += text(x + w - 78, y + 23, '—', 15, 700, '#fff', 'middle')
        s += text(x + w - 50, y + 23, '▢', 15, 700, '#fff', 'middle')
        s += text(x + w - 22, y + 23, '✕', 15, 700, '#fff', 'middle')
    return s

def key(x, y, label, w=44, h=36, hl=False, size=13):
    return (rect(x, y, w, h, YEL if hl else '#fff', r=7) + line(x + 2, y + h - 1, x + w - 2, y + h - 1, INK, 4)
            + text(x + w / 2, y + h / 2 + 5, label, size, 800, anchor='middle'))

def tabs(x, y, names, active, color):
    s, cx = '', x
    for n in names:
        w = 14 + len(n) * 8
        if n == active:
            s += rect(cx, y, w, 30, '#fff', r=6) + text(cx + w / 2, y + 20, n, 13, 800, color, 'middle')
        else:
            s += text(cx + w / 2, y + 20, n, 13, 600, MUTED, 'middle')
        cx += w + 4
    return s

def button(x, y, w, label, icon=None, hl=False, color=INK):
    s = rect(x, y, w, 58, YEL if hl else '#fff', stroke=INK if hl else '#dfe3ee', sw=2, r=8)
    if icon: s += icon(x + w / 2, y + 22, color)
    s += text(x + w / 2, y + 50, label, 11, 700, anchor='middle')
    return s

def group_label(x, y, w, label):
    return line(x, y, x + w, y, '#dfe3ee') + text(x + w / 2, y + 16, label, 11, 600, MUTED, 'middle')

def folder(x, y, w=44, fill='#ffd84d'):
    return (f'<path d="M{x} {y+8} h{w*0.4} l6 -6 h{w*0.6-6} a4 4 0 0 1 4 4 v{w*0.6} a4 4 0 0 1 -4 4 h-{w} a4 4 0 0 1 -4 -4 v-{w*0.6-2} a4 4 0 0 1 4 -4z" fill="{fill}" stroke="{INK}" stroke-width="2"/>')

def doc_icon(x, y, w=32, h=40, color='#fff'):
    return (f'<path d="M{x} {y} h{w-10} l10 10 v{h-10} h-{w} z" fill="{color}" stroke="{INK}" stroke-width="2"/>'
            + f'<path d="M{x+w-10} {y} v10 h10" fill="none" stroke="{INK}" stroke-width="2"/>')

def cursor(x, y):
    return f'<path d="M{x} {y} l0 18 l5 -4 l3 7 l3 -1 l-3 -7 l6 -1z" fill="#fff" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'

def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="{INK}"/></marker></defs>'
            f'<rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>')

# --- иконки для кнопок ленты ---
def ic_bold(x, y, c): return text(x, y + 6, 'Ж', 20, 900, anchor='middle')
def ic_italic(x, y, c): return text(x, y + 6, 'К', 20, 700, anchor='middle') and f'<text x="{x}" y="{y+6}" font-family="{FONT}" font-size="20" font-weight="700" font-style="italic" text-anchor="middle" fill="{INK}">К</text>'
def ic_under(x, y, c): return f'<text x="{x}" y="{y+6}" font-family="{FONT}" font-size="20" font-weight="700" text-decoration="underline" text-anchor="middle" fill="{INK}">Ч</text>'
def ic_color(x, y, c): return text(x, y + 4, 'A', 20, 800, anchor='middle') + rect(x - 10, y + 8, 20, 5, '#d94848', 'none', 0)
def ic_bullets(x, y, c): return ''.join(f'<circle cx="{x-10}" cy="{y-8+i*8}" r="2.2" fill="{INK}"/>' + line(x - 4, y - 8 + i * 8, x + 10, y - 8 + i * 8, INK, 2) for i in range(3))
def ic_numbers(x, y, c): return ''.join(text(x - 13, y - 5 + i * 8, str(i + 1), 8, 800) + line(x - 4, y - 8 + i * 8, x + 10, y - 8 + i * 8, INK, 2) for i in range(3))
def ic_align(kind):
    def f(x, y, c):
        s = ''
        for i, w in enumerate([16, 10, 16, 8]):
            yy = y - 9 + i * 6
            if kind == 'l': s += line(x - 8, yy, x - 8 + w, yy, INK, 2)
            elif kind == 'c': s += line(x - w / 2, yy, x + w / 2, yy, INK, 2)
            elif kind == 'r': s += line(x + 8 - w, yy, x + 8, yy, INK, 2)
            else: s += line(x - 8, yy, x + 8, yy, INK, 2)
        return s
    return f
def ic_table(x, y, c): return rect(x - 12, y - 10, 24, 20, '#fff', INK, 1.5, 2) + line(x - 12, y - 3, x + 12, y - 3, INK, 1.5) + line(x - 12, y + 4, x + 12, y + 4, INK, 1.5) + line(x - 4, y - 10, x - 4, y + 10, INK, 1.5) + line(x + 4, y - 10, x + 4, y + 10, INK, 1.5)
def ic_picture(x, y, c): return rect(x - 12, y - 10, 24, 20, '#fff', INK, 1.5, 2) + f'<path d="M{x-10} {y+7} l6 -8 l5 5 l4 -3 l5 6z" fill="{c}"/>' + f'<circle cx="{x+5}" cy="{y-4}" r="2.5" fill="{YEL}"/>'
def ic_slide(x, y, c): return rect(x - 13, y - 9, 26, 18, '#fff', INK, 1.5, 2) + text(x, y + 14, '+', 14, 800, c, 'middle')
def ic_chart(x, y, c): return ''.join(rect(x - 11 + i * 8, y + 10 - h, 6, h, c, 'none', 0) for i, h in enumerate([8, 18, 12]))
def ic_theme(col):
    def f(x, y, c): return rect(x - 14, y - 10, 28, 20, col, INK, 1.5, 2) + rect(x - 10, y - 6, 12, 4, '#fff', 'none', 0)
    return f

# --- сцены ---
def w1():
    b = rect(0, 0, 800, 480, '#cfe3ff', 'none', 0)
    icons = [('Этот компьютер', 60, 60), ('Корзина', 60, 150), ('Мои уроки', 60, 240), ('Paint', 160, 60)]
    for name, x, y in icons:
        if name == 'Корзина':
            b += f'<path d="M{x-14} {y} h28 l-4 34 h-20z" fill="#fff" stroke="{INK}" stroke-width="2"/>' + rect(x - 18, y - 6, 36, 6, '#fff', INK, 2, 2)
        elif name == 'Paint':
            b += rect(x - 16, y - 2, 32, 32, '#fff', INK, 2, 6) + f'<circle cx="{x-6}" cy="{y+8}" r="4" fill="#d94848"/><circle cx="{x+6}" cy="{y+8}" r="4" fill="{C["win"]}"/><circle cx="{x}" cy="{y+20}" r="4" fill="{C["excel"]}"/>'
        elif name == 'Этот компьютер':
            b += rect(x - 18, y - 2, 36, 26, '#fff', INK, 2, 4) + rect(x - 8, y + 26, 16, 6, INK, 'none', 0)
        else:
            b += folder(x - 22, y, 44)
        b += text(x, y + 52, name, 12, 700, anchor='middle')
    b += rect(0, 424, 800, 56, '#e9eef7', INK, 2, 0)
    b += rect(18, 436, 32, 32, '#fff', INK, 2, 6) + ''.join(rect(24 + i % 2 * 11, 442 + i // 2 * 11, 9, 9, C['win'], 'none', 0) for i in range(4))
    b += rect(64, 438, 200, 28, '#fff', INK, 2, 14) + text(80, 457, 'Поиск', 13, 600, MUTED)
    for i, col in enumerate(['#4f46e5', '#16a34a', '#ea580c']):
        b += rect(290 + i * 44, 438, 30, 30, col, INK, 2, 6)
    b += text(770, 452, '14:05', 13, 800, anchor='end') + text(770, 468, '08.09', 12, 600, MUTED, 'end')
    b += callout(1, 210, 250, 'Значки: программы и папки')
    b += callout(2, 34, 410, 'Кнопка Пуск', side='right')
    b += callout(3, 400, 400, 'Панель задач')
    b += callout(4, 700, 400, 'Часы', side='right')
    return svg(800, 480, b)

def w2():
    b = ''
    # мышь
    b += f'<path d="M110 120 a90 90 0 0 1 180 0 v170 a90 90 0 0 1 -180 0z" fill="#fff" stroke="{INK}" stroke-width="3"/>'
    b += line(200, 30, 200, 190, INK, 3) + line(110, 190, 290, 190, INK, 3)
    b += rect(191, 90, 18, 40, '#fff', INK, 2, 9)
    b += f'<path d="M110 120 a90 90 0 0 1 90 -90 v160 h-90z" fill="{YEL}" fill-opacity=".6"/>'
    b += callout(1, 150, 110, '')
    b += callout(2, 250, 110, '')
    b += callout(3, 200, 60, '')
    b += text(40, 400, 'Левая кнопка: клик, двойной клик', 15, 700)
    b += text(40, 428, 'Правая кнопка: меню «что можно сделать»', 15, 700)
    b += text(40, 456, 'Колёсико: прокрутка страницы', 15, 700)
    b += callout(1, 22, 395) + callout(2, 22, 423) + callout(3, 22, 451)
    # клавиатура
    kx, ky = 380, 60
    b += rect(kx - 16, ky - 16, 440, 300, '#f3f4f8', INK, 2, 12)
    b += key(kx, ky, 'Esc', 44, hl=True)
    for i, ch in enumerate('1234567'): b += key(kx + 52 + i * 42, ky, ch, 36)
    b += key(kx + 52 + 7 * 42, ky, '⌫', 62, hl=True)
    b += key(kx, ky + 44, 'Tab', 56)
    for i, ch in enumerate('ЙЦУКЕН'): b += key(kx + 64 + i * 42, ky + 44, ch, 36)
    b += key(kx + 64 + 6 * 42, ky + 44, '', 40)
    b += key(kx, ky + 88, 'Caps', 66)
    for i, ch in enumerate('ФЫВАП'): b += key(kx + 74 + i * 42, ky + 88, ch, 36)
    b += key(kx + 74 + 5 * 42, ky + 88, 'Enter', 88, hl=True)
    b += key(kx, ky + 132, 'Shift', 86, hl=True)
    for i, ch in enumerate('ЯЧСМИ'): b += key(kx + 94 + i * 42, ky + 132, ch, 36)
    b += key(kx + 94 + 5 * 42, ky + 132, 'Shift', 92, hl=True)
    b += key(kx, ky + 176, 'Ctrl', 56, hl=True) + key(kx + 62, ky + 176, 'Win', 50, hl=True) + key(kx + 118, ky + 176, 'Alt', 46, hl=True)
    b += key(kx + 170, ky + 176, 'Пробел', 120, hl=True)
    for i, ch in enumerate('←↑↓→'): b += key(kx + 296 + i * 32, ky + 176, ch, 28)
    b += text(kx, 385, 'Жёлтые клавиши — главные в уроке', 14, 700, MUTED)
    return svg(820, 480, b)

def w3():
    b = window(20, 40, 480, 330, 'Блокнот — без имени', C['win'])
    b += text(44, 110, 'Привет! Это моё первое окно.', 16, 600)
    b += line(44, 130, 260, 130, MUTED, 1, '4 4')
    b += callout(1, 250, 57, '') + text(250, 20, 'Заголовок: держи и тащи, чтобы двигать окно', 13, 700, anchor='middle')
    for n, bx, cy, lbl in [(2, 422, 110, '— свернуть на панель задач'), (3, 450, 150, '▢ на весь экран / обратно'), (4, 478, 190, '✕ закрыть программу')]:
        b += line(bx, 70, 525, cy, INK, 1.5, '3 3') + callout(n, 540, cy, lbl)
    b += f'<path d="M484 354 l14 14" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
    b += callout(5, 540, 330, 'Край окна: тяни,') + text(562, 352, 'чтобы менять размер', 14, 700)
    b += rect(0, 430, 800, 50, '#e9eef7', INK, 2, 0)
    b += rect(18, 440, 30, 30, '#fff', INK, 2, 6) + ''.join(rect(24 + i % 2 * 10, 446 + i // 2 * 10, 8, 8, C['win'], 'none', 0) for i in range(4))
    b += rect(70, 440, 30, 30, C['win'], INK, 2, 6) + line(66, 474, 104, 474, C['win'], 4)
    b += rect(112, 440, 30, 30, '#fff', INK, 2, 6)
    b += text(160, 460, '← свёрнутое окно живёт здесь, кликни — вернётся', 13, 700)
    return svg(800, 480, b)

def w4():
    b = window(20, 20, 760, 440, 'Мои уроки — Проводник', C['win'])
    b += rect(36, 66, 24, 24, '#fff', INK, 2, 6) + text(48, 83, '←', 14, 800, anchor='middle')
    b += rect(70, 66, 690, 26, '#fff', INK, 2, 6)
    b += text(84, 84, 'Этот компьютер  ›  Документы  ›  Мои уроки', 13, 700)
    b += line(220, 104, 220, 458, '#dfe3ee')
    for i, (n, hl) in enumerate([('Рабочий стол', 0), ('Документы', 1), ('Изображения', 0), ('Загрузки', 0), ('Музыка', 0)]):
        y = 150 + i * 34
        if hl: b += rect(30, y - 6, 184, 28, '#e6f0ff', 'none', 0, 6)
        b += folder(38, y - 2, 20, '#ffd84d') + text(70, y + 13, n, 13, 800 if hl else 600)
    for i, (n, kind) in enumerate([('Рисунки', 'f'), ('Тексты', 'f'), ('О себе.docx', 'd'), ('кот.jpg', 'i')]):
        x, y = 260 + i * 125, 130
        b += folder(x, y, 60) if kind == 'f' else doc_icon(x + 8, y - 4, 44, 54, '#e6f0ff' if kind == 'd' else '#fff5d6')
        b += text(x + 30, y + 78, n, 13, 700, anchor='middle')
    b += callout(1, 48, 345, 'Главные папки')
    b += callout(2, 500, 84, 'Адрес: где ты сейчас')
    b += callout(3, 500, 260, 'Папки и файлы внутри')
    b += callout(4, 48, 118, 'Назад')
    b += text(260, 400, 'Правая кнопка на пустом месте → Создать → Папку', 14, 700, MUTED)
    return svg(800, 480, b)

def w5():
    b = ''
    b += rect(30, 40, 200, 150, '#fff', INK, 2, 12) + text(130, 66, 'Документы', 13, 800, MUTED, 'middle')
    b += doc_icon(112, 86, 36, 46, '#e6f0ff') + rect(104, 80, 52, 76, 'none', C['win'], 2, 6) + text(130, 176, 'проба.txt', 12, 700, anchor='middle')
    b += arrow(240, 115, 330, 115) + key(255, 60, 'Ctrl', 40, 30, True, 12) + text(299, 80, '+', 14, 800, anchor='middle') + key(305, 60, 'C', 30, 30, True, 12)
    b += rect(340, 70, 120, 90, YEL, INK, 2, 14) + text(400, 100, 'Буфер', 13, 800, anchor='middle') + text(400, 118, '(невидимый', 11, 600, MUTED, 'middle') + text(400, 132, 'карман)', 11, 600, MUTED, 'middle')
    b += arrow(470, 115, 560, 115) + key(485, 60, 'Ctrl', 40, 30, True, 12) + text(529, 80, '+', 14, 800, anchor='middle') + key(535, 60, 'V', 30, 30, True, 12)
    b += rect(570, 40, 200, 150, '#fff', INK, 2, 12) + text(670, 66, 'Мои уроки', 13, 800, MUTED, 'middle')
    b += doc_icon(652, 86, 36, 46, '#e6f0ff') + text(670, 176, 'проба.txt', 12, 700, anchor='middle')
    b += text(400, 215, 'Копировать: файл остаётся и там, и там. Вырезать (Ctrl+X): файл переезжает.', 13, 700, MUTED, 'middle')
    # удаление и корзина
    b += doc_icon(112, 290, 36, 46, '#e6f0ff') + text(130, 360, 'файл', 12, 700, anchor='middle')
    b += arrow(170, 315, 300, 315) + key(200, 262, 'Delete', 66, 30, True, 12)
    b += f'<path d="M330 290 h60 l-8 70 h-44z" fill="#fff" stroke="{INK}" stroke-width="2"/>' + rect(324, 280, 72, 10, '#fff', INK, 2, 3) + text(360, 385, 'Корзина', 13, 800, anchor='middle')
    b += arrow(410, 315, 540, 315) + text(475, 300, 'Восстановить', 12, 700, anchor='middle')
    b += doc_icon(552, 290, 36, 46, '#e6f0ff') + text(570, 360, 'вернулся', 12, 700, anchor='middle')
    b += key(640, 285, 'Ctrl', 40, 30, True, 12) + text(684, 305, '+', 14, 800, anchor='middle') + key(690, 285, 'Z', 30, 30, True, 12) + text(680, 345, 'отменить', 12, 700, anchor='middle') + text(680, 361, 'последнее', 12, 700, anchor='middle')
    return svg(800, 400, b)

def w6():
    b = rect(0, 0, 800, 480, '#cfe3ff', 'none', 0)
    b += rect(40, 30, 460, 394, '#fff', INK, 2, 14)
    b += rect(60, 50, 420, 36, '#fff', INK, 2, 18) + text(80, 74, 'paint', 16, 800) + line(122, 58, 122, 78, INK, 2)
    b += text(60, 118, 'Лучшее соответствие', 12, 700, MUTED)
    b += rect(60, 128, 420, 54, '#e6f0ff', INK, 2, 10)
    b += rect(72, 138, 34, 34, '#fff', INK, 2, 6) + f'<circle cx="82" cy="150" r="4" fill="#d94848"/><circle cx="96" cy="150" r="4" fill="{C["win"]}"/><circle cx="89" cy="162" r="4" fill="{C["excel"]}"/>'
    b += text(118, 152, 'Paint', 15, 800) + text(118, 170, 'Приложение', 12, 600, MUTED)
    b += text(60, 215, 'Ещё', 12, 700, MUTED)
    for i, n in enumerate(['Paint 3D', 'Параметры Paint', 'Найти в интернете']):
        b += text(72, 244 + i * 30, n, 14, 600)
    b += rect(0, 424, 800, 56, '#e9eef7', INK, 2, 0)
    b += rect(18, 436, 32, 32, YEL, INK, 2, 6) + ''.join(rect(24 + i % 2 * 11, 442 + i // 2 * 11, 9, 9, C['win'], 'none', 0) for i in range(4))
    b += callout(1, 34, 400, 'Нажми Win или Пуск и сразу печатай', side='right')
    b += callout(2, 500, 68, 'Название программы')
    b += callout(3, 500, 155, 'Нашлось! Жми Enter')
    b += key(520, 190, 'Enter', 90, 36, True)
    b += text(520, 260, 'Правая кнопка на программе →', 13, 700) + text(520, 280, '«Закрепить на панели задач»', 13, 700)
    return svg(800, 480, b)

def w7():
    b = window(30, 30, 520, 330, 'Браузер — какой-то сайт', '#7c86a2')
    b += text(54, 100, 'Сериал, серия 12', 14, 700, MUTED) + rect(54, 112, 470, 120, '#f3f4f8', '#dfe3ee', 2, 8)
    b += rect(150, 130, 330, 190, '#fff', '#d94848', 3, 12)
    b += text(315, 165, '⚠ ВНИМАНИЕ!', 20, 900, '#d94848', 'middle')
    b += text(315, 195, 'Ваш компьютер заражён!', 15, 800, anchor='middle')
    b += text(315, 216, 'Нажмите здесь, чтобы вылечить', 13, 600, MUTED, 'middle')
    b += rect(215, 240, 200, 40, '#d94848', 'none', 0, 8) + text(315, 266, 'СКАЧАТЬ ЛЕЧЕНИЕ', 13, 900, '#fff', 'middle')
    b += text(462, 152, '✕', 16, 800, MUTED, 'middle')
    b += f'<line x1="140" y1="120" x2="490" y2="330" stroke="{INK}" stroke-width="6" stroke-linecap="round" opacity=".85"/><line x1="490" y1="120" x2="140" y2="330" stroke="{INK}" stroke-width="6" stroke-linecap="round" opacity=".85"/>'
    b += callout(1, 590, 200, 'Это обман. Не нажимай!')
    b += callout(2, 590, 240, 'Закрой окно крестиком')
    b += text(612, 265, 'или', 13, 600, MUTED) + key(640, 250, 'Alt', 40, 30, True, 12) + text(684, 270, '+', 14, 800, anchor='middle') + key(690, 250, 'F4', 40, 30, True, 12)
    b += callout(3, 590, 320, 'Сомневаешься — зови взрослых')
    b += text(30, 400, 'Пароль — секрет. Незнакомцам — ничего о себе. Скачивать — только с разрешения.', 14, 700, MUTED)
    return svg(840, 430, b)

def word_ribbon(x, y, w, active, groups_fn):
    s = rect(x, y, w, 140, '#f7f7fb', INK, 2, 0)
    s += tabs(x + 10, y + 6, ['Файл', 'Главная', 'Вставка', 'Конструктор', 'Макет', 'Вид'], active, C['word'])
    s += line(x, y + 40, x + w, y + 40, '#dfe3ee')
    s += groups_fn(x, y + 48)
    return s

def d1():
    def groups(x, y):
        s = button(x + 12, y, 60, 'Вставить') + group_label(x + 6, y + 62, 72, 'Буфер')
        s += rect(x + 100, y + 4, 110, 24, '#fff', '#c9ccd6', 1.5, 4) + text(x + 108, y + 21, 'Calibri', 12, 600) + rect(x + 216, y + 4, 36, 24, '#fff', '#c9ccd6', 1.5, 4) + text(x + 234, y + 21, '11', 12, 600, anchor='middle')
        s += ic_bold(x + 112, y + 44, INK) + ic_italic(x + 142, y + 44, INK) + ic_under(x + 172, y + 44, INK) + group_label(x + 96, y + 62, 170, 'Шрифт')
        return s
    b = window(20, 20, 760, 440, 'О себе — Word', C['word'])
    b += word_ribbon(21, 55, 758, 'Главная', groups)
    b += rect(150, 205, 500, 255, '#fff', '#dfe3ee', 2, 0)
    b += text(190, 250, 'Меня зовут Миша. Мне 10 лет.', 16, 600)
    b += text(190, 278, 'Я люблю сериалы и', 16, 600) + text(354, 278, 'сабаку', 16, 600)
    b += f'<path d="M354 283 q4 4 8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0" fill="none" stroke="#d94848" stroke-width="2"/>'
    b += line(416, 264, 416, 284, INK, 2)
    b += callout(1, 444, 274, 'Курсор: здесь появится текст')
    b += callout(2, 384, 312, 'Красная волна — ошибка. Правая кнопка исправит', side='right', size=12)
    b += callout(3, 60, 410, '', ) + key(84, 395, 'Ctrl', 40, 30, True, 12) + text(128, 415, '+', 14, 800, anchor='middle') + key(134, 395, 'S', 30, 30, True, 12) + text(60, 445, 'сохранить, почаще', 12, 700)
    return svg(800, 480, b)

def d2():
    def groups(x, y):
        s = rect(x + 20, y + 4, 120, 24, '#fff', '#c9ccd6', 1.5, 4) + text(x + 28, y + 21, 'Calibri', 12, 600)
        s += rect(x + 146, y + 4, 42, 24, YEL, INK, 2, 4) + text(x + 167, y + 21, '24', 12, 800, anchor='middle')
        s += rect(x + 22, y + 32, 28, 28, YEL, INK, 2, 6) + ic_bold(x + 36, y + 40, INK)
        s += rect(x + 54, y + 32, 28, 28, '#fff', '#c9ccd6', 1.5, 6) + ic_italic(x + 68, y + 40, INK)
        s += rect(x + 86, y + 32, 28, 28, '#fff', '#c9ccd6', 1.5, 6) + ic_under(x + 100, y + 40, INK)
        s += rect(x + 200, y + 32, 34, 28, '#fff', '#c9ccd6', 1.5, 6) + ic_color(x + 217, y + 40, INK)
        s += callout(2, x + 36, y + 80) + callout(3, x + 167, y + 80) + callout(4, x + 217, y + 80)
        return s
    b = window(20, 20, 760, 440, 'Мой сериал — Word', C['word'])
    b += word_ribbon(21, 55, 758, 'Главная', groups)
    b += rect(150, 205, 500, 255, '#fff', '#dfe3ee', 2, 0)
    b += rect(186, 235, 250, 34, '#cfe0ff', 'none', 0) + text(190, 261, 'Мой сериал', 26, 900, C['word'])
    b += text(190, 300, 'Это история про ребят, которые', 15, 600) + text(190, 323, 'нашли карту сокровищ.', 15, 600)
    b += callout(1, 450, 252, 'Сначала выдели текст')
    b += text(190, 400, '2 — жирный (Ctrl+B)', 13, 700, MUTED) + text(190, 420, '3 — размер букв', 13, 700, MUTED) + text(190, 440, '4 — цвет букв', 13, 700, MUTED)
    return svg(800, 480, b)

def d3():
    def groups(x, y):
        s = rect(x + 20, y + 8, 30, 30, YEL, INK, 2, 6) + ic_bullets(x + 35, y + 23, INK)
        s += rect(x + 56, y + 8, 30, 30, YEL, INK, 2, 6) + ic_numbers(x + 71, y + 23, INK)
        for i, k in enumerate('lcrj'):
            s += rect(x + 110 + i * 36, y + 10, 30, 26, YEL if k == 'c' else '#fff', INK if k == 'c' else '#c9ccd6', 2 if k == 'c' else 1.5, 6) + ic_align(k)(x + 125 + i * 36, y + 23, INK)
        s += callout(1, x + 35, y + 66) + callout(2, x + 71, y + 66) + callout(3, x + 161, y + 66)
        s += text(x + 290, y + 30, 'группа «Абзац»', 12, 700, MUTED)
        return s
    b = window(20, 20, 760, 440, 'Мой день — Word', C['word'])
    b += word_ribbon(21, 55, 758, 'Главная', groups)
    b += rect(150, 205, 500, 255, '#fff', '#dfe3ee', 2, 0)
    b += text(400, 247, 'Мой день', 22, 900, anchor='middle')
    for i, s in enumerate(['Проснуться', 'Позавтракать', 'Школа']):
        b += text(200, 283 + i * 24, f'{i+1}.', 15, 800) + text(222, 283 + i * 24, s, 15, 600)
    for i, s in enumerate(['Пельмени', 'Блины']):
        b += f'<circle cx="206" cy="{365+i*24-5}" r="3" fill="{INK}"/>' + text(222, 365 + i * 24, s, 15, 600)
    b += callout(3, 500, 241, 'Заголовок по центру (Ctrl+E)')
    b += callout(2, 340, 305, 'Список с цифрами')
    b += callout(1, 340, 375, 'Список с точками')
    return svg(800, 480, b)

def d4():
    def groups(x, y):
        s = button(x + 12, y, 64, 'Таблица', ic_table, True, C['word']) + button(x + 82, y, 64, 'Рисунки', ic_picture, True, C['word']) + button(x + 152, y, 64, 'Фигуры', None)
        s += callout(1, x + 44, y + 76) + callout(2, x + 114, y + 76)
        return s
    b = window(20, 20, 760, 440, 'Мой сериал — Word', C['word'])
    b += word_ribbon(21, 55, 758, 'Вставка', groups)
    b += rect(150, 205, 500, 255, '#fff', '#dfe3ee', 2, 0)
    b += rect(190, 230, 150, 100, '#ffedd5', C['word'], 2, 4) + f'<path d="M200 320 l40 -50 l30 30 l20 -20 l40 40z" fill="{C["ppt"]}"/>' + f'<circle cx="305" cy="255" r="9" fill="{YEL}"/>'
    for cx, cy in [(190, 230), (340, 230), (190, 330), (340, 330)]: b += f'<circle cx="{cx}" cy="{cy}" r="5" fill="#fff" stroke="{C["word"]}" stroke-width="2"/>'
    for r in range(3):
        for c in range(2):
            b += rect(400 + c * 110, 230 + r * 32, 110, 32, '#fff', INK, 1.5, 0)
    b += text(410, 251, 'Герой', 13, 800) + text(520, 251, 'Кто он', 13, 800) + text(410, 283, 'Макс', 13, 600) + text(520, 283, 'капитан', 13, 600)
    b += callout(3, 346, 336, 'Тяни за угловой кружок')
    b += text(190, 400, '1 — таблица: выбери размер сеткой', 13, 700, MUTED) + text(190, 420, '2 — картинка с компьютера', 13, 700, MUTED)
    return svg(800, 480, b)

def d5():
    b = window(20, 20, 760, 440, 'Печать', C['word'])
    b += text(50, 90, 'Печать', 22, 900)
    b += rect(50, 110, 240, 44, C['word'], INK, 2, 10) + text(170, 138, 'Печать', 16, 900, '#fff', 'middle')
    b += text(50, 190, 'Копии:', 13, 700, MUTED) + rect(110, 172, 50, 26, '#fff', '#c9ccd6', 1.5, 4) + text(135, 190, '1', 13, 800, anchor='middle')
    b += text(50, 230, 'Принтер', 13, 700, MUTED) + rect(50, 240, 240, 34, '#fff', '#c9ccd6', 1.5, 6) + text(62, 262, 'HP LaserJet (дома)', 13, 700) + f'<circle cx="270" cy="257" r="5" fill="{C["excel"]}"/>'
    b += text(50, 310, 'Параметры', 13, 700, MUTED) + rect(50, 320, 240, 34, '#fff', '#c9ccd6', 1.5, 6) + text(62, 342, 'Напечатать все страницы', 13, 600)
    b += rect(340, 70, 400, 380, '#e9eef7', 'none', 0)
    b += rect(400, 90, 280, 350, '#fff', INK, 2, 0)
    b += text(540, 130, 'Мой сериал', 16, 900, anchor='middle')
    for i in range(9): b += line(430, 160 + i * 22, 430 + (250 if i % 3 else 180), 160 + i * 22, '#c9ccd6', 4)
    b += callout(1, 300, 132, 'Кнопка «Печать»', side='right')
    b += callout(2, 300, 257, 'Нужный принтер', side='right')
    b += callout(3, 430, 400, 'Предпросмотр: так будет на бумаге', side='right', size=12)
    b += text(50, 420, 'Открыть: Ctrl + P', 14, 800) + text(50, 445, 'В PDF: Файл → Сохранить как → тип PDF', 13, 700, MUTED)
    return svg(800, 480, b)

def excel_grid(x, y, cols, rows, cw=90, rh=28, data=None, sel=None):
    s = rect(x, y, 40, rh, '#f3f4f8', '#c9ccd6', 1.5, 0)
    for c in range(cols):
        s += rect(x + 40 + c * cw, y, cw, rh, '#f3f4f8', '#c9ccd6', 1.5, 0) + text(x + 40 + c * cw + cw / 2, y + rh - 9, 'ABCDEFGH'[c], 13, 800, anchor='middle')
    for r in range(rows):
        s += rect(x, y + rh + r * rh, 40, rh, '#f3f4f8', '#c9ccd6', 1.5, 0) + text(x + 20, y + rh * 2 + r * rh - 9, str(r + 1), 13, 800, anchor='middle')
        for c in range(cols):
            s += rect(x + 40 + c * cw, y + rh + r * rh, cw, rh, '#fff', '#c9ccd6', 1.5, 0)
    for (r, c, v, bold) in (data or []):
        num = v.replace('.', '').isdigit()
        s += text(x + 40 + c * cw + (cw - 8 if num else 8), y + rh * 2 + r * rh - 9, v, 13, 800 if bold else 600, anchor='end' if num else 'start')
    if sel:
        r, c = sel
        s += rect(x + 40 + c * cw, y + rh + r * rh, cw, rh, 'none', C['excel'], 3, 0)
    return s

def e1():
    b = window(20, 20, 760, 440, 'Оценки — Excel', C['excel'])
    b += rect(36, 66, 60, 26, '#fff', INK, 2, 4) + text(66, 84, 'B3', 13, 800, anchor='middle')
    b += rect(104, 66, 650, 26, '#fff', '#c9ccd6', 1.5, 4) + text(112, 84, 'fx', 12, 700, MUTED) + text(140, 84, '4', 13, 600)
    data = [(0, 0, 'Предмет', 1), (0, 1, 'Оценка', 1), (1, 0, 'Математика', 0), (1, 1, '5', 0), (2, 0, 'Русский', 0), (2, 1, '4', 0), (3, 0, 'Чтение', 0), (3, 1, '5', 0)]
    b += excel_grid(36, 110, 6, 9, 100, 30, data, sel=(2, 1))
    b += callout(1, 336, 100, 'Столбцы: буквы')
    b += callout(2, 56, 436, 'Строки: цифры')
    b += callout(3, 110, 60, 'Адрес ячейки: столбец B, строка 3', side='right', size=12)
    b += callout(4, 300, 200, '← ячейка B3', side='right')
    return svg(800, 480, b)

def e2():
    b = window(20, 20, 760, 440, 'Оценки — Excel', C['excel'])
    b += rect(36, 66, 60, 26, '#fff', INK, 2, 4) + text(66, 84, 'B6', 13, 800, anchor='middle')
    b += rect(104, 66, 650, 26, YEL, INK, 2, 4) + text(112, 84, 'fx', 12, 700, INK) + text(140, 84, '=СУММ(B2:B4)', 14, 800, mono=True)
    data = [(0, 0, 'Предмет', 1), (0, 1, 'Оценка', 1), (1, 0, 'Математика', 0), (1, 1, '5', 0), (2, 0, 'Русский', 0), (2, 1, '4', 0), (3, 0, 'Чтение', 0), (3, 1, '5', 0), (5, 0, 'Всего', 1), (5, 1, '14', 1)]
    b += excel_grid(36, 110, 6, 9, 100, 30, data, sel=(5, 1))
    b += rect(176, 170, 100, 90, 'none', C['excel'], 2, 0)
    b += callout(1, 390, 79, 'Строка формул: тут видно формулу')
    b += callout(2, 300, 305, 'В ячейке — ответ')
    b += callout(3, 300, 215, 'B2:B4 — «от B2 до B4»')
    b += text(36, 434, 'Формула всегда начинается со знака =', 14, 800)
    b += text(36, 454, 'Поменяй оценку — сумма пересчитается сама', 13, 700, MUTED)
    return svg(800, 480, b)

def e3():
    b = window(20, 20, 760, 440, 'Мои игры — Excel', C['excel'])
    b += rect(21, 55, 758, 40, '#f7f7fb', INK, 2, 0) + tabs(31, 60, ['Файл', 'Главная', 'Вставка', 'Формулы', 'Вид'], 'Вставка', C['excel'])
    b += rect(300, 58, 70, 34, YEL, INK, 2, 6) + ic_chart(335, 75, C['excel'])
    data = [(0, 0, 'Игра', 1), (0, 1, 'Часов', 1), (1, 0, 'Гонки', 0), (1, 1, '6', 0), (2, 0, 'Стройка', 0), (2, 1, '10', 0), (3, 0, 'Футбол', 0), (3, 1, '4', 0)]
    b += excel_grid(36, 120, 2, 5, 90, 30, data)
    b += rect(76, 150, 180, 120, '#cfe0ff', C['excel'], 2, 0) + rect(76, 150, 180, 120, 'none', C['excel'], 2, 0)
    for (r, c, v, bold) in data:
        num = v.isdigit()
        b += text(76 + c * 90 + (82 if num else 8), 171 + r * 30, v, 13, 800 if bold else 600, anchor='end' if num else 'start')
    b += rect(320, 120, 420, 300, '#fff', INK, 2, 10)
    b += text(530, 150, 'Во что я играю', 15, 900, anchor='middle')
    b += line(360, 390, 720, 390, INK, 2) + line(360, 170, 360, 390, INK, 2)
    for i, (n, h) in enumerate([('Гонки', 6), ('Стройка', 10), ('Футбол', 4)]):
        x = 400 + i * 110
        b += rect(x, 390 - h * 20, 70, h * 20, C['excel'], INK, 2, 4) + text(x + 35, 410, n, 12, 700, anchor='middle') + text(x + 35, 382 - h * 20, str(h), 12, 800, anchor='middle')
    b += callout(1, 262, 210, '', side='left') + callout(2, 380, 75, '', side='right')
    b += text(36, 320, '1 — выдели таблицу с заголовками', 13, 700, MUTED) + text(36, 340, '2 — Вставка → диаграмма', 13, 700, MUTED)
    b += text(36, 380, 'Выше столбик —', 13, 800) + text(36, 398, 'больше часов', 13, 800)
    return svg(800, 480, b)

def ppt_window(title, active, groups_fn):
    b = window(20, 20, 760, 440, title, C['ppt'])
    b += rect(21, 55, 758, 118, '#f7f7fb', INK, 2, 0) + tabs(31, 60, ['Файл', 'Главная', 'Вставка', 'Конструктор', 'Переходы', 'Анимация', 'Слайд-шоу'], active, C['ppt'])
    b += line(21, 94, 779, 94, '#dfe3ee') + groups_fn(21, 98)
    return b

def p1():
    def groups(x, y):
        return button(x + 12, y, 70, 'Создать слайд', ic_slide, True, C['ppt']) + button(x + 90, y, 60, 'Макет', None)
    b = ppt_window('Мой сериал — PowerPoint', 'Главная', groups)
    for i, t in enumerate(['Мой любимый сериал', 'О чём сериал', 'Главные герои', 'Спасибо!']):
        y = 188 + i * 62
        b += text(36, y + 30, str(i + 1), 12, 800, MUTED) + rect(52, y, 110, 52, '#fff', INK if i == 0 else '#c9ccd6', 2 if i == 0 else 1.5, 6) + text(107, y + 30, t, 8, 700, anchor='middle')
    b += line(180, 183, 180, 458, '#dfe3ee')
    b += rect(200, 188, 560, 240, '#fff', INK, 2, 6)
    b += rect(230, 225, 500, 60, 'none', '#c9ccd6', 1.5, 4) + text(480, 263, 'Мой любимый сериал', 24, 900, anchor='middle')
    b += rect(280, 305, 400, 40, 'none', '#c9ccd6', 1.5, 4) + text(480, 331, 'Миша, 4 «Б»', 15, 600, MUTED, 'middle')
    b += callout(1, 196, 128, 'Новый слайд (Ctrl+M)')
    b += callout(2, 48, 452, 'Все слайды по порядку')
    b += callout(3, 480, 385, 'Кликни в рамку и печатай')
    return svg(800, 480, b)

def p2():
    def groups(x, y):
        s = ''
        for i, col in enumerate(['#1c1f2e', '#2f6df6', '#16a34a', '#ea580c', '#7c3aed']):
            s += rect(x + 12 + i * 60, y + 4, 52, 36, col, INK, 2, 6) + rect(x + 18 + i * 60, y + 10, 24, 6, '#fff', 'none', 0)
        s += group_label(x + 6, y + 44, 310, 'Темы')
        return s
    b = ppt_window('Мой питомец — PowerPoint', 'Конструктор', groups)
    b += rect(200, 188, 560, 260, '#1c1f2e', INK, 2, 6)
    b += text(240, 238, 'Мой кот Барсик', 24, 900, YEL)
    b += text(240, 278, '• Рыжий', 15, 600, '#fff') + text(240, 303, '• Любит спать', 15, 600, '#fff') + text(240, 328, '• Ловит мух', 15, 600, '#fff')
    b += rect(520, 218, 200, 200, '#ffedd5', '#fff', 2, 8) + f'<circle cx="620" cy="308" r="55" fill="{C["ppt"]}"/><circle cx="600" cy="296" r="6" fill="{INK}"/><circle cx="640" cy="296" r="6" fill="{INK}"/><path d="M585 258 l10 -30 l25 22z M655 258 l-10 -30 l-25 22z" fill="{C["ppt"]}"/>'
    b += callout(1, 355, 134, 'Выбери одну тему на всю презентацию', side='right', size=12)
    b += callout(2, 520, 218, '') + text(50, 215, '2 — картинка:', 13, 800) + text(50, 235, 'Вставка → Рисунки', 13, 700, MUTED)
    b += callout(3, 400, 98, '') + text(50, 285, '3 — Переходы:', 13, 800) + text(50, 305, 'смена слайдов', 13, 700, MUTED)
    b += text(50, 355, 'Мало слов, крупно.', 13, 800) + text(50, 375, 'Тёмное на светлом', 13, 700, MUTED) + text(50, 395, 'или наоборот', 13, 700, MUTED)
    return svg(800, 480, b)

def p3():
    b = rect(0, 0, 800, 480, INK, 'none', 0)
    b += rect(40, 30, 720, 300, '#fff', '#fff', 2, 6)
    b += text(400, 170, 'Спасибо за внимание!', 34, 900, anchor='middle')
    b += text(400, 215, 'Есть вопросы?', 18, 600, MUTED, 'middle')
    b += key(50, 370, 'F5', 60, 40, True, 15) + text(80, 440, 'запустить', 13, 700, '#fff', 'middle') + text(80, 458, 'с начала', 13, 700, '#fff', 'middle')
    b += key(170, 370, 'Пробел', 130, 40, True, 15) + text(235, 440, 'следующий слайд', 13, 700, '#fff', 'middle') + text(235, 458, '(или → или клик)', 12, 600, '#c9ccd6', 'middle')
    b += key(340, 370, '←', 50, 40, True, 15) + text(365, 440, 'назад', 13, 700, '#fff', 'middle')
    b += key(430, 370, 'Esc', 60, 40, True, 15) + text(460, 440, 'выйти', 13, 700, '#fff', 'middle') + text(460, 458, 'из показа', 13, 700, '#fff', 'middle')
    b += text(560, 388, 'Смотри на людей,', 14, 800, YEL) + text(560, 408, 'а не в экран.', 14, 800, YEL) + text(560, 440, 'Не читай со слайда —', 13, 700, '#fff') + text(560, 458, 'рассказывай своими словами', 13, 700, '#fff')
    return svg(800, 480, b)

SCENES = {'w1': w1, 'w2': w2, 'w3': w3, 'w4': w4, 'w5': w5, 'w6': w6, 'w7': w7,
          'd1': d1, 'd2': d2, 'd3': d3, 'd4': d4, 'd5': d5, 'e1': e1, 'e2': e2, 'e3': e3, 'p1': p1, 'p2': p2, 'p3': p3}

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn in SCENES.items():
        with open(os.path.join(OUT, f'{name}.svg'), 'w') as f: f.write(fn())
    print('drawn', len(SCENES))
