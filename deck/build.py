"""Build the deck: 14 slides, two-colour system, rich backgrounds."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from . import theme as T
from . import data as D
from . import qr
from .helpers import (rgb, blank, fill_bg, rect, line, textbox, para, runs,
                      add_title, add_footer, icon, bar_chart, line_chart,
                      animate, dot_grid, ribbon, corner_arcs, halftone,
                      waffle, triangle_corner)

TOTAL = 14
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "out")            # scratch: icons, qr, previews
DELIVERABLE = os.path.join(REPO, "future-of-work.pptx")


def _prs():
    prs = Presentation()
    prs.slide_width = Inches(T.SLIDE_W)
    prs.slide_height = Inches(T.SLIDE_H)
    return prs


# --- slide 1: cover ---------------------------------------------------------
def slide_cover(prs):
    s = blank(prs)
    fill_bg(s, T.NAVY_DEEP)
    # textured right third: dot grid + halftone + corner arcs
    dot_grid(s, "24406B", T.SLIDE_W - 5.0, 0.0, 5.0, T.SLIDE_H,
             step=0.46, dot=0.05)
    halftone(s, T.ORANGE, T.SLIDE_W - 3.05, 0.0, cols=7, rows=5, step=0.42,
             max_d=0.34, big_left=False)
    corner_arcs(s, "2E4C79", T.SLIDE_W, T.SLIDE_H, [4.4, 3.4, 2.5], 2.0)
    rect(s, 0, 0, 0.22, T.SLIDE_H, fill=T.ORANGE)
    # brand mark
    icon(s, "robot", T.WHITE, T.MARGIN + 0.05, 0.95, 1.15)
    tb, tf = textbox(s, T.MARGIN + 0.1, 2.6, 8.4, 2.0)
    para(tf, D.TITLE, size=T.SZ_COVER_TITLE, color=T.WHITE, bold=True,
         first=True, line_spacing=1.02)
    line(s, T.MARGIN + 0.1, 4.75, T.MARGIN + 2.6, 4.75, color=T.ORANGE,
         width=4.0)
    tb2, tf2 = textbox(s, T.MARGIN + 0.1, 5.0, 8.4, 1.0)
    para(tf2, D.SUBTITLE, size=T.SZ_COVER_SUB, color="C9D6E8", first=True,
         line_spacing=1.1)
    tb3, tf3 = textbox(s, T.MARGIN + 0.1, 6.35, 9.0, 0.5)
    runs(para(tf3, "", size=T.SZ_SMALL, first=True),
         [(D.AUTHOR + "   ", {"color": T.WHITE, "bold": True}),
          (D.ORG + "   ·   " + D.DATE, {"color": "8FA6C4"})],
         size=T.SZ_SMALL)
    return s


# --- slide 2: hook (attention in the first seconds) -------------------------
def slide_hook(prs):
    s = blank(prs)
    fill_bg(s, T.NAVY)
    corner_arcs(s, "2A4A75", 0, 0, [5.2, 4.1, 3.0, 1.9], 2.0)
    dot_grid(s, "24406B", 0.0, T.SLIDE_H - 2.4, 4.5, 2.4, step=0.42, dot=0.05)
    tb, tf = textbox(s, 1.0, 1.6, 11.3, 2.4, anchor=MSO_ANCHOR.MIDDLE)
    para(tf, D.HOOK, size=T.SZ_HOOK, color=T.WHITE, bold=True, first=True,
         align=PP_ALIGN.CENTER, line_spacing=1.05)
    tb2, tf2 = textbox(s, 1.6, 4.15, 10.1, 0.9, anchor=MSO_ANCHOR.MIDDLE)
    para(tf2, D.HOOK_SUB, size=T.SZ_SUBTITLE - 2, color="C9D6E8",
         align=PP_ALIGN.CENTER, first=True)
    # yes/no chips
    cy = 5.35
    cw = 3.1
    for i, (label, col) in enumerate([("ДА", T.ORANGE), ("НЕТ", "33517F")]):
        x = T.SLIDE_W / 2 - cw - 0.35 + i * (cw + 0.7)
        chip = rect(s, x, cy, cw, 0.95, fill=col,
                    shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.28)
        ctb, ctf = textbox(s, x, cy, cw, 0.95, anchor=MSO_ANCHOR.MIDDLE)
        para(ctf, label, size=T.SZ_TITLE, color=T.WHITE, bold=True,
             align=PP_ALIGN.CENTER, first=True)
        animate(s, chip.shape_id, "zoom", delay=0,
                trigger="click" if i == 0 else "after")
    add_footer(s, 2, TOTAL)
    return s


# --- slide 3: contents ------------------------------------------------------
def slide_toc(prs):
    s = blank(prs)
    fill_bg(s)
    dot_grid(s, T.GREY_LIGHT, T.SLIDE_W - 2.6, 1.4, 2.4, 5.6, step=0.42,
             dot=0.05)
    add_title(s, "Содержание")
    top = 1.95
    gap = 0.82
    for i, (name, hint) in enumerate(D.TOC):
        y = top + i * gap
        marker = rect(s, T.MARGIN, y, 0.6, 0.6, fill=T.NAVY,
                      shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.22)
        mtb, mtf = textbox(s, T.MARGIN, y, 0.6, 0.6,
                           anchor=MSO_ANCHOR.MIDDLE)
        para(mtf, str(i + 1), size=22, color=T.WHITE, bold=True,
             align=PP_ALIGN.CENTER, first=True)
        tb, tf = textbox(s, T.MARGIN + 0.92, y, 8.4, 0.6,
                         anchor=MSO_ANCHOR.MIDDLE)
        runs(para(tf, "", first=True),
             [(name, {"bold": True, "color": T.NAVY, "size": T.SZ_BODY}),
              ("  —  " + hint, {"color": T.GREY, "size": T.SZ_SMALL})])
        if i < len(D.TOC) - 1:
            line(s, T.MARGIN + 0.92, y + 0.71, T.MARGIN + 8.4, y + 0.71,
                 color=T.GREY_LIGHT, width=0.75)
        animate(s, marker.shape_id, "wipe_right", delay=0,
                trigger="click" if i == 0 else "after")
    add_footer(s, 3, TOTAL)
    return s


# --- slide 4: scale of the problem ------------------------------------------
def slide_intro(prs):
    s = blank(prs)
    fill_bg(s)
    add_title(s, "Масштаб проблемы")
    # left: two stat cards
    cw = 6.0
    for i, st in enumerate(D.STATS):
        y = 1.95 + i * 2.1
        card = rect(s, T.MARGIN, y, cw, 1.85, fill=T.WHITE, line=T.GREY_LIGHT,
                    line_w=1.0)
        rect(s, T.MARGIN, y, 0.12, 1.85, fill=T.ORANGE)
        vtb, vtf = textbox(s, T.MARGIN + 0.35, y + 0.1, 2.2, 1.65,
                           anchor=MSO_ANCHOR.MIDDLE)
        para(vtf, st["value"], size=T.SZ_KPI, color=T.NAVY, bold=True,
             align=PP_ALIGN.CENTER, first=True)
        ttb, ttf = textbox(s, T.MARGIN + 2.6, y + 0.2, cw - 2.9, 1.45,
                           anchor=MSO_ANCHOR.MIDDLE)
        para(ttf, st["label"], size=T.SZ_BODY, color=T.NAVY, bold=True,
             first=True)
        para(ttf, st["text"], size=T.SZ_SMALL, color=T.TEXT)
        para(ttf, st["source"], size=T.SZ_SMALL, color=T.GREY)
        animate(s, card.shape_id, "wipe_left", delay=0,
                trigger="click" if i == 0 else "after")
    # right: isotype waffle "less than 1%"
    px = T.MARGIN + cw + 0.7
    pw = T.SLIDE_W - T.MARGIN - px
    ptb, ptf = textbox(s, px, 1.9, pw, 0.6)
    para(ptf, "100 рабочих мест в России", size=T.SZ_SMALL, color=T.GREY,
         first=True)
    waffle(s, px + 0.1, 2.45, 1, T.ORANGE, T.GREY_LIGHT, cols=10, rows=10,
           cell=0.225, gap=0.06)
    ftb, ftf = textbox(s, px, 5.35, pw, 1.0)
    p = para(ftf, "", first=True, line_spacing=1.1)
    runs(p, [("1", {"bold": True, "color": T.ORANGE, "size": T.SZ_SUBTITLE}),
             ("  из 100 — под угрозой полной автоматизации",
              {"color": T.NAVY, "size": T.SZ_SMALL})])
    para(ftf, D.FACT[1], size=T.SZ_SMALL, color=T.GREY)
    add_footer(s, 4, TOTAL)
    return s


# --- slide 5: methodology ---------------------------------------------------
def slide_factors(prs):
    s = blank(prs)
    fill_bg(s)
    add_title(s, "Критерии уязвимости профессий")
    tb, tf = textbox(s, T.MARGIN, 1.7, T.CONTENT_W, 0.5)
    para(tf, "Пять факторов, по которым оценивают, насколько профессия "
             "подвержена автоматизации.", size=T.SZ_SMALL, color=T.GREY,
         first=True)
    cols = 5
    gap = 0.28
    cw = (T.CONTENT_W - gap * (cols - 1)) / cols
    top = 2.55
    for i, (ic, title, desc) in enumerate(D.FACTORS):
        x = T.MARGIN + i * (cw + gap)
        card = rect(s, x, top, cw, 3.5, fill=T.WHITE, line=T.GREY_LIGHT,
                    line_w=1.0)
        rect(s, x, top, cw, 0.09, fill=T.NAVY)
        icon(s, ic, T.NAVY, x + (cw - 1.05) / 2, top + 0.35, 1.05)
        ntb, ntf = textbox(s, x + 0.12, top + 1.6, cw - 0.24, 0.9,
                           anchor=MSO_ANCHOR.TOP)
        para(ntf, title, size=T.SZ_SMALL + 1, color=T.NAVY, bold=True,
             align=PP_ALIGN.CENTER, first=True, line_spacing=1.0)
        dtb, dtf = textbox(s, x + 0.12, top + 2.5, cw - 0.24, 0.9)
        para(dtf, desc, size=T.SZ_SMALL, color=T.GREY,
             align=PP_ALIGN.CENTER, first=True, line_spacing=1.05)
        animate(s, card.shape_id, "fade", delay=0,
                trigger="click" if i == 0 else "after")
    add_footer(s, 5, TOTAL)
    return s


# --- slide 6: high-risk jobs ------------------------------------------------
def slide_high(prs):
    s = blank(prs)
    fill_bg(s)
    ribbon(s, T.SLIDE_W - 3.2, -1.0, 6.0, 2.2, T.ORANGE_TINT, angle=0)
    add_title(s, "Под ударом: высокий риск автоматизации", accent=T.ORANGE)
    top = 1.85
    gap = 1.02
    for i, (ic, name, desc) in enumerate(D.HIGH_RISK):
        y = top + i * gap
        card = rect(s, T.MARGIN, y, T.CONTENT_W, 0.88, fill=T.WHITE,
                    line=T.GREY_LIGHT, line_w=1.0)
        rect(s, T.MARGIN, y, 0.14, 0.88, fill=T.ORANGE)
        icon(s, ic, T.ORANGE, T.MARGIN + 0.34, y + 0.14, 0.6)
        tb, tf = textbox(s, T.MARGIN + 1.2, y, 5.6, 0.88,
                         anchor=MSO_ANCHOR.MIDDLE)
        para(tf, name, size=T.SZ_BODY, color=T.NAVY, bold=True, first=True)
        dtb, dtf = textbox(s, T.MARGIN + 7.0, y, T.CONTENT_W - 7.2, 0.88,
                           anchor=MSO_ANCHOR.MIDDLE)
        para(dtf, desc, size=T.SZ_SMALL, color=T.GREY, first=True,
             align=PP_ALIGN.RIGHT)
        animate(s, card.shape_id, "wipe_left", delay=0,
                trigger="click" if i == 0 else "after")
    add_footer(s, 6, TOTAL, note="Источник: Атлас новых профессий")
    return s


# --- slide 7: bar chart -----------------------------------------------------
def slide_bar(prs):
    s = blank(prs)
    fill_bg(s)
    dot_grid(s, T.GREY_LIGHT, T.MARGIN, 6.3, 6.0, 0.6, step=0.4, dot=0.05)
    add_title(s, "Насколько автоматизируемы задачи?")
    tb, tf = textbox(s, T.MARGIN, 1.7, T.CONTENT_W, 0.5)
    para(tf, "Вероятность автоматизации профессий, % задач", size=T.SZ_SMALL,
         color=T.GREY, first=True)
    bar_chart(s, T.MARGIN + 0.1, 2.2, T.CONTENT_W - 0.2, 4.25,
              D.CHART_CATS, "Доля автоматизируемых задач, %",
              D.CHART_VALUES,
              colors=[T.ORANGE, T.ORANGE, T.NAVY, T.ORANGE, T.NAVY])
    tb2, tf2 = textbox(s, T.MARGIN, 6.55, T.CONTENT_W, 0.4)
    para(tf2, D.CHART_SOURCE, size=T.SZ_SMALL, color=T.GREY, first=True)
    add_footer(s, 7, TOTAL)
    return s


# --- slide 8: low-risk jobs -------------------------------------------------
def slide_low(prs):
    s = blank(prs)
    fill_bg(s)
    corner_arcs(s, T.GREY_LIGHT, T.SLIDE_W, 0, [3.2, 2.4], 2.0)
    add_title(s, "Вне зоны риска: устойчивые профессии", accent=T.NAVY)
    top = 1.85
    gap = 1.02
    for i, (ic, name, desc) in enumerate(D.LOW_RISK):
        y = top + i * gap
        card = rect(s, T.MARGIN, y, T.CONTENT_W, 0.88, fill=T.WHITE,
                    line=T.GREY_LIGHT, line_w=1.0)
        rect(s, T.MARGIN, y, 0.14, 0.88, fill=T.NAVY)
        icon(s, ic, T.NAVY, T.MARGIN + 0.34, y + 0.14, 0.6)
        tb, tf = textbox(s, T.MARGIN + 1.2, y, 6.0, 0.88,
                         anchor=MSO_ANCHOR.MIDDLE)
        para(tf, name, size=T.SZ_BODY, color=T.NAVY, bold=True, first=True)
        dtb, dtf = textbox(s, T.MARGIN + 7.4, y, T.CONTENT_W - 7.6, 0.88,
                           anchor=MSO_ANCHOR.MIDDLE)
        para(dtf, desc, size=T.SZ_SMALL, color=T.GREY, first=True,
             align=PP_ALIGN.RIGHT)
        animate(s, card.shape_id, "fade", delay=0,
                trigger="click" if i == 0 else "after")
    add_footer(s, 8, TOTAL)
    return s


# --- slide 9: comparison table ----------------------------------------------
def slide_table(prs):
    s = blank(prs)
    fill_bg(s)
    add_title(s, "Риски и возможности")
    rows = len(D.TABLE_ROWS) + 1
    cols = 3
    x, y = T.MARGIN, 1.95
    w, h = T.CONTENT_W * 0.92, 4.3
    gt = s.shapes.add_table(rows, cols, Inches(x), Inches(y),
                            Inches(w), Inches(h))
    tbl = gt.table
    tbl.columns[0].width = Inches(w * 0.24)
    tbl.columns[1].width = Inches(w * 0.24)
    tbl.columns[2].width = Inches(w * 0.52)
    for c, text in enumerate(D.TABLE_HEAD):
        cell = tbl.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb(T.NAVY)
        cell.margin_left = cell.margin_right = Inches(0.12)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER
        r = p.add_run()
        r.text = text
        r.font.size = Pt(T.SZ_SMALL)
        r.font.bold = True
        r.font.name = T.FONT
        r.font.color.rgb = rgb(T.WHITE)
    for ri, (prof, risk, opp) in enumerate(D.TABLE_ROWS, start=1):
        zebra = T.WHITE if ri % 2 else T.GREY_LIGHT
        risk_color = T.ORANGE if risk == "Высокий" else T.NAVY
        for ci, text in enumerate((prof, risk, opp)):
            cell = tbl.cell(ri, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(zebra)
            cell.margin_left = cell.margin_right = Inches(0.12)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.alignment = (PP_ALIGN.LEFT if ci == 0
                           else PP_ALIGN.CENTER if ci == 1
                           else PP_ALIGN.LEFT)
            r = p.add_run()
            r.text = text
            r.font.size = Pt(T.SZ_SMALL)
            r.font.bold = ci in (0, 1)
            r.font.name = T.FONT
            r.font.color.rgb = rgb(T.NAVY if ci == 0
                                   else risk_color if ci == 1 else T.TEXT)
    tb, tf = textbox(s, T.MARGIN, 6.4, T.CONTENT_W, 0.4)
    para(tf, "Одна и та же профессия может терять рутинные задачи и "
             "получать новые роли.", size=T.SZ_SMALL, color=T.GREY,
         first=True)
    animate(s, gt.shape_id, "fade", delay=0, trigger="click")
    add_footer(s, 9, TOTAL)
    return s


# --- slide 10: new professions ----------------------------------------------
def slide_new_jobs(prs):
    s = blank(prs)
    fill_bg(s)
    dot_grid(s, T.GREY_LIGHT, T.MARGIN, 1.5, 3.6, 5.4, step=0.42, dot=0.05)
    add_title(s, "Кем станут люди?")
    tb, tf = textbox(s, T.MARGIN, 1.7, T.CONTENT_W, 0.5)
    para(tf, "Вместе с автоматизацией появляются новые профессии "
             "на стыке человека и ИИ.", size=T.SZ_SMALL, color=T.GREY,
         first=True)
    scheme_x = T.MARGIN
    scheme_y = 2.7
    icon(s, "people", T.NAVY, scheme_x, scheme_y + 0.55, 1.15)
    ptb, ptf = textbox(s, scheme_x + 1.2, scheme_y + 1.35, 1.6, 0.4)
    para(ptf, "Человек", size=T.SZ_SMALL, color=T.NAVY, bold=True,
         align=PP_ALIGN.CENTER, first=True)
    ptb, ptf = textbox(s, scheme_x + 1.35, scheme_y + 0.85, 0.9, 0.6,
                       anchor=MSO_ANCHOR.MIDDLE)
    para(ptf, "+", size=40, color=T.ORANGE, bold=True,
         align=PP_ALIGN.CENTER, first=True)
    icon(s, "robot", T.ORANGE, scheme_x + 2.35, scheme_y + 0.55, 1.15)
    ptb, ptf = textbox(s, scheme_x + 2.2, scheme_y + 1.35, 1.5, 0.4)
    para(ptf, "ИИ", size=T.SZ_SMALL, color=T.ORANGE, bold=True,
         align=PP_ALIGN.CENTER, first=True)
    ptb, ptf = textbox(s, scheme_x, scheme_y + 2.0, 3.6, 0.6)
    para(ptf, "Новые роли", size=T.SZ_SUBTITLE - 4, color=T.NAVY, bold=True,
         align=PP_ALIGN.CENTER, first=True)
    list_x = T.MARGIN + 4.15
    list_w = T.SLIDE_W - T.MARGIN - list_x
    jy = 2.15
    jgap = 1.02
    for i, (ic, name, desc) in enumerate(D.NEW_JOBS):
        y = jy + i * jgap
        icon(s, ic, T.NAVY, list_x, y + 0.06, 0.66)
        tb, tf = textbox(s, list_x + 0.9, y, list_w - 0.9, 0.78,
                         anchor=MSO_ANCHOR.MIDDLE)
        para(tf, name, size=T.SZ_BODY - 1, color=T.NAVY, bold=True,
             first=True)
        para(tf, desc, size=T.SZ_SMALL, color=T.GREY)
    add_footer(s, 10, TOTAL)
    return s


# --- slide 11: outlook ------------------------------------------------------
def slide_outlook(prs):
    s = blank(prs)
    fill_bg(s)
    add_title(s, "Что нас ждёт? Прогноз до 2030 года")
    tb, tf = textbox(s, T.MARGIN, 1.7, T.CONTENT_W, 0.5)
    para(tf, "Спрос на профессии, 2024 = 100", size=T.SZ_SMALL, color=T.GREY,
         first=True)
    line_chart(s, T.MARGIN + 0.1, 2.15, T.CONTENT_W - 0.2, 4.2,
               D.OUTLOOK_CATS, D.OUTLOOK_SERIES)
    tb2, tf2 = textbox(s, T.MARGIN, 6.5, T.CONTENT_W, 0.4)
    para(tf2, D.OUTLOOK_SOURCE, size=T.SZ_SMALL, color=T.GREY, first=True)
    add_footer(s, 11, TOTAL)
    return s


# --- slide 12: skills -------------------------------------------------------
def slide_skills(prs):
    s = blank(prs)
    fill_bg(s)
    corner_arcs(s, T.GREY_LIGHT, 0, T.SLIDE_H, [3.2, 2.4], 2.0)
    add_title(s, "Навыки будущего")
    tb, tf = textbox(s, T.MARGIN, 1.7, T.CONTENT_W, 0.5)
    para(tf, "Четыре опоры адаптации к автоматизированной экономике.",
         size=T.SZ_SMALL, color=T.GREY, first=True)
    gw = (T.CONTENT_W - 0.5) / 2.0
    gh = 1.9
    top = 2.5
    for i, (ic, name, desc) in enumerate(D.SKILLS):
        col = i % 2
        row = i // 2
        x = T.MARGIN + col * (gw + 0.5)
        y = top + row * (gh + 0.45)
        card = rect(s, x, y, gw, gh, fill=T.WHITE, line=T.GREY_LIGHT,
                    line_w=1.0)
        rect(s, x, y, 0.14, gh, fill=T.ORANGE)
        icon(s, ic, T.ORANGE, x + 0.4, y + 0.42, 1.0)
        tb, tf = textbox(s, x + 1.65, y + 0.28, gw - 1.9, gh - 0.5,
                         anchor=MSO_ANCHOR.MIDDLE)
        para(tf, name, size=T.SZ_BODY, color=T.NAVY, bold=True, first=True)
        para(tf, desc, size=T.SZ_SMALL, color=T.GREY)
        animate(s, card.shape_id, "fade", delay=0,
                trigger="click" if i == 0 else "after")
    add_footer(s, 12, TOTAL)
    return s


# --- slide 13: conclusions --------------------------------------------------
def slide_conclusions(prs):
    s = blank(prs)
    fill_bg(s)
    add_title(s, "Главное")
    top = 2.1
    gap = 1.28
    for i, text in enumerate(D.CONCLUSIONS):
        y = top + i * gap
        rect(s, T.MARGIN, y, 0.12, 1.0, fill=T.ORANGE)
        tb, tf = textbox(s, T.MARGIN + 0.55, y, T.CONTENT_W - 0.55, 1.0,
                         anchor=MSO_ANCHOR.MIDDLE)
        runs(para(tf, "", first=True),
             [(f"{i + 1}.  ", {"bold": True, "color": T.ORANGE,
                               "size": T.SZ_SUBTITLE}),
              (text, {"color": T.NAVY, "bold": True,
                      "size": T.SZ_SUBTITLE})])
    add_footer(s, 13, TOTAL)
    return s


# --- slide 14: closing ------------------------------------------------------
def slide_closing(prs):
    s = blank(prs)
    fill_bg(s, T.NAVY_DEEP)
    dot_grid(s, "24406B", 0.0, T.SLIDE_H - 2.6, 5.0, 2.6, step=0.44,
             dot=0.05)
    corner_arcs(s, "2E4C79", T.SLIDE_W, 0, [4.4, 3.4, 2.5], 2.0)
    rect(s, 0, 0, 0.22, T.SLIDE_H, fill=T.ORANGE)
    tb, tf = textbox(s, T.MARGIN + 0.1, 1.2, 8.2, 1.2)
    para(tf, "Спасибо за внимание!", size=T.SZ_COVER_TITLE, color=T.WHITE,
         bold=True, first=True)
    line(s, T.MARGIN + 0.1, 2.7, T.MARGIN + 2.6, 2.7, color=T.ORANGE,
         width=4.0)
    tb2, tf2 = textbox(s, T.MARGIN + 0.1, 2.95, 8.2, 2.8)
    para(tf2, "Источники", size=T.SZ_SUBTITLE - 6, color=T.ORANGE, bold=True,
         first=True, space_after=6)
    for src in D.SOURCES:
        para(tf2, "•  " + src, size=T.SZ_SMALL, color="C9D6E8",
             space_after=4, line_spacing=1.0)
    qr_path = qr.render(D.CONTACT_QR, dark=T.NAVY)
    s.shapes.add_picture(qr_path, Inches(T.SLIDE_W - T.MARGIN - 2.35),
                         Inches(3.1), Inches(2.35), Inches(2.35))
    ctb, ctf = textbox(s, T.SLIDE_W - T.MARGIN - 2.35, 5.55, 2.35, 0.5)
    para(ctf, "Проект на GitHub", size=T.SZ_SMALL, color="C9D6E8",
         align=PP_ALIGN.CENTER, first=True)
    tb3, tf3 = textbox(s, T.MARGIN + 0.1, 6.6, 9.0, 0.5)
    para(tf3, D.AUTHOR + "   ·   " + D.ORG, size=T.SZ_SMALL,
         color="8FA6C4", first=True)
    return s


def build(path=None):
    prs = _prs()
    slide_cover(prs)
    slide_hook(prs)
    slide_toc(prs)
    slide_intro(prs)
    slide_factors(prs)
    slide_high(prs)
    slide_bar(prs)
    slide_low(prs)
    slide_table(prs)
    slide_new_jobs(prs)
    slide_outlook(prs)
    slide_skills(prs)
    slide_conclusions(prs)
    slide_closing(prs)
    os.makedirs(OUT, exist_ok=True)
    path = path or DELIVERABLE
    prs.save(path)
    return path


if __name__ == "__main__":
    print(build())