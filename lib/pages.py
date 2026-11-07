# -*- coding: utf-8 -*-
"""
页面层：每个函数返回一个完整 HTML 文档。

页面 = 报头 + 若干 block + 若干 cell。不写坐标、不写绝对定位，
增删一个状态只需在列表里加一行 dict。
"""
from html import escape

from .components import (
    block, cell, field, grid, icon_btn, inspector, label, page, panel, track_card,
)
from .icons import ICONS, icon


# ------------------------------------------------------------------ 轨道卡页
def track_cards_page():
    rows = [
        ("Video track", dict(title="Video 1", kind="video", letter="V"), "Default state"),
        ("Audio track", dict(title="Audio 1", kind="audio", letter="A"), "Default state"),
        ("Text track", dict(title="Text 1", kind="text", letter="T", sound=False), "无扬声器开关"),
        ("Long name", dict(title="Interview — B-roll take 03", kind="video", letter="V"),
         "标题超出时省略号截断，动作区不被挤压"),
        ("Locked", dict(title="Video 1", kind="video", letter="V", locked=True),
         "锁变强调色，卡片描边转为虚线"),
        ("Hidden", dict(title="Video 1", kind="video", letter="V", hidden=True),
         "眼睛划掉 + 强调色"),
        ("Muted", dict(title="Audio 1", kind="audio", letter="A", muted=True),
         "扬声器划掉 + 强调色"),
        ("Locked, hidden and muted",
         dict(title="Video 1", kind="video", letter="V", locked=True, hidden=True, muted=True),
         "三个开关同时激活"),
        ("Hover: toggle", dict(title="Video 1", kind="video", letter="V", hover="lock"),
         "灰底浮起，图标提亮"),
        ("Hover: delete", dict(title="Video 1", kind="video", letter="V", hover="trash"),
         "图标转红，底色带红晕"),
        ("First track", dict(title="Video 1", kind="video", letter="V", first=True),
         "上移不可用，降到 32% 不透明度"),
        ("Last track", dict(title="Video 1", kind="video", letter="V", last=True),
         "下移不可用"),
    ]
    cells = "".join(cell(name, track_card(**kw), note) for name, kw, note in rows)

    body = (
        '<div class="page">'
        + masthead(
            "Component · Track card",
            "轨道卡 · 状态矩阵",
            "同一个 HTML 组件，12 种状态。锁、隐藏、静音、禁用全部是 class 修饰符，"
            "不换结构、不换图形，改一个布尔值就切换。卡片宽度由内容决定，标题过长自动省略。",
        )
        + block("01", "状态矩阵", "四列一行，同一行内的卡片共享顶线与基线。", "240 × 84",
                cells)
        + foot_blurb()
        + "</div>"
    )
    return page("Track card · 状态矩阵", body=body)


# ------------------------------------------------------------------ 面板页
def inspector_page():
    left = cell("常规态", inspector(), "未选中，字段底色比面板亮一级")
    right = cell(
        "选中并锁定",
        inspector(locked=True, selected=True, caret=True, pointer=True),
        "虚线外框 + 四角标记 + 光标 + 指针；不可编辑字段整体降色",
    )
    body = (
        '<div class="page">'
        + masthead(
            "Component · Inspector",
            "属性面板 · 两种状态",
            "面板高度由内容撑开，不写死。四角标记是四个 span 各带两条 border，"
            "不是画出来的 SVG —— 但视觉上与矢量一致。",
        )
        + block("01", "同一组件的两个状态", "左为默认，右为选中（同时处于锁定）。", "344 × auto",
                left + right, "row row--2")
        + foot_blurb()
        + "</div>"
    )
    return page("Inspector · 属性面板", body=body)


# ------------------------------------------------------------------ 图标页
def icons_page():
    cells = "".join(
        cell(name, f'<div class="icon-tile">{icon(name, 32)}</div>')
        for name in ICONS
    )
    body = (
        '<div class="page">'
        + masthead(
            "Assets · Icons",
            f"图标库 · {len(ICONS)} 枚",
            "全部来自同一份 symbols 定义：设计稿里内联复用，生产代码可直接引 "
            "<code>icons.svg</code>。图标是唯一值得用 SVG 手写的东西 —— 布局不该用。",
        )
        + block("01", "16 × 16 网格", "统一 1.5px 描边、round cap / round join。", "16 × 16",
                cells, "row row--icons")
        + foot_blurb()
        + "</div>"
    )
    return page("Icons · 图标库", body=body)


# ------------------------------------------------------------------ 编辑器页
def editor_shell():
    media = [
        ("仓库全景.mp4", "00:12", True),
        ("货架特写.mp4", "00:08", False),
        ("过秤记录.mp4", "00:21", False),
        ("环境音.wav", "01:45", False),
    ]
    media_html = "".join(
        f'<div class="sci__item"><span class="sci__thumb"></span>'
        f'<div class="sci__meta"><div class="sci__name">{escape(n)}</div>'
        f'<div class="sci__dur">{d}</div></div></div>'
        for n, d, _ in media
    )

    ticks = "".join(f"<span>{t}</span>" for t in ("0s", "5s", "10s", "15s", "20s"))

    def row(tag, clips):
        return (
            f'<div class="tl__row"><span class="tl__tag">{tag}</span>'
            f'<div class="tl__lane">{clips}</div></div>'
        )

    tl = (
        row("V2", '<span class="clip clip--text" style="left:18%;width:16%">标题：出库作业</span>')
        + row("V1", '<span class="clip clip--selected" style="left:0%;width:42%">仓库全景.mp4</span>'
                    '<span class="clip" style="left:44%;width:26%">货架特写.mp4</span>')
        + row("A1", '<span class="clip clip--audio" style="left:0%;width:70%">环境音.wav</span>')
        + row("T1", '<span class="clip clip--text" style="left:4%;width:22%">字幕轨</span>')
    )

    return (
        '<div class="editor">'
        '<div class="editor__bar">'
        '<span class="editor__mark">O</span>'
        '<span class="editor__name">粮库运维纪实</span>'
        '<span class="editor__crumb">1080p · 30fps · 00:24</span>'
        '<span class="editor__spacer"></span>'
        f'{icon_btn("undo")}{icon_btn("redo")}'
        '<span class="btn btn--primary">导出</span>'
        "</div>"
        '<div class="editor__body">'
        f'<div class="editor__aside"><div class="sci"><div class="sci__title">媒体库</div>{media_html}</div></div>'
        '<div class="editor__stage">'
        '<div class="preview"><span class="preview__label">1920 × 1080</span></div>'
        "</div>"
        f'<div class="editor__insp">{inspector(locked=True, selected=True)}</div>'
        "</div>"
        '<div class="tl">'
        f'<div class="tl__ruler"><div class="tl__gutter"></div><div class="tl__ticks">{ticks}</div></div>'
        f'<div class="tl__rows">{tl}</div>'
        '<div class="tl__playhead" style="left:44%"></div>'
        "</div>"
        "</div>"
    )


def editor_page():
    body = (
        '<div class="page">'
        + masthead(
            "Example · Editor shell",
            "整页编辑器 · 三栏 + 时间轴",
            "这一页是「为什么布局该用 HTML」的证据：三栏宽度、预览区 16:9 比例、时间轴轨道行，"
            "全部由 grid 自动分配。同样一页如果手写 SVG，需要算上百个坐标，改一次侧栏宽度就全废。",
        )
        + '<section class="block"><div class="block__head">'
          '<span class="block__num">01</span><h2>完整界面</h2>'
          '<span class="block__meta">1060 × 620</span></div>'
          f'<div class="stage">{editor_shell()}</div></section>'
        + foot_blurb()
        + "</div>"
    )
    return page("Editor shell · 整页编辑器", body=body)


# ------------------------------------------------------------------ 公共片段
def masthead(eyebrow, h1, lede):
    return (
        f'<header class="masthead">'
        f'<div class="masthead__eyebrow">{escape(eyebrow)}</div>'
        f"<h1>{escape(h1)}</h1>"
        f"<p>{lede}</p>"
        f"</header>"
    )


def foot_blurb():
    return (
        '<footer class="foot">'
        "layout: css grid / flex &nbsp;·&nbsp; icons: svg symbols &nbsp;·&nbsp; "
        "tokens: assets/tokens.css<br>"
        "本页是设计文档，不是应用本身；mock-up 才能使用深色主题。"
        "</footer>"
    )


PAGES = [
    ("track-cards", track_cards_page),
    ("inspector", inspector_page),
    ("icons", icons_page),
    ("editor", editor_page),
]
