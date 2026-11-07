# -*- coding: utf-8 -*-
"""
组件层：每个函数返回一段 HTML 字符串。

这是整套方案省时省 token 的关键——
组件定义一次，页面里一行调用；布局交给浏览器，不用算坐标。
新增页面 = 拼装已有组件 + 写少量新组件，不重画。

命名遵循 BEM，class 与 assets/ui.css 一一对应。
生产项目可直接把这些 class 抄进自己的模板。
"""
from html import escape

from .icons import icon, ALERT_STATES


# ------------------------------------------------------------------ 原子
def badge(kind, letter):
    """kind: video | audio | text"""
    return f'<span class="badge badge--{kind}">{escape(letter)}</span>'


def icon_btn(name, *, hover=False, danger=False, disabled=False, size=15):
    cls = "icon-btn"
    if danger:
        cls += " icon-btn--danger"
    elif hover:
        cls += " icon-btn--hover"
    dis = " disabled" if disabled else ""
    return f'<button class="{cls}"{dis} type="button" tabindex="-1">{icon(name, size)}</button>'


def toggle(name, *, on=False, hover=False, size=16):
    cls = "toggle"
    if hover:
        cls += " toggle--hover"
    elif on:
        cls += " toggle--on"
    return f'<span class="{cls}">{icon(name, size)}</span>'


# ------------------------------------------------------------------ 轨道卡
def track_card(
    title,
    *,
    kind="video",
    letter="V",
    locked=False,
    hidden=False,
    muted=False,
    sound=True,
    hover=None,
    first=False,
    last=False,
    width=None,
):
    """
    hover: None | 'up' | 'down' | 'trash' | 'lock'
    其余状态全是布尔开关，不改结构 —— 这就是组件复用的意义。
    """
    cls = "track-card"
    if locked:
        cls += " track-card--locked"
    style = f' style="width:{width}px"' if width else ""

    actions = "".join(
        [
            icon_btn("up", hover=hover == "up", disabled=first),
            icon_btn("down", hover=hover == "down", disabled=last),
            icon_btn("trash", hover=hover == "trash", danger=hover == "trash"),
        ]
    )

    toggles = [toggle("lock", on=locked, hover=hover == "lock")]
    if hidden:
        toggles.append(toggle("eyeoff", on=True))
    else:
        toggles.append(toggle("eye"))
    if sound:
        toggles.append(toggle("soundoff", on=True) if muted else toggle("sound"))

    return (
        f'<div class="{cls}"{style}>'
        f'<div class="track-card__top">'
        f"{badge(kind, letter)}"
        f'<span class="track-card__title">{escape(title)}</span>'
        f'<span class="track-card__actions">{actions}</span>'
        f"</div>"
        f'<div class="track-card__toggles">{"".join(toggles)}</div>'
        f"</div>"
    )


# ------------------------------------------------------------------ 字段
def field(value, *, suffix=None, hint=None, mono=True, focus=False,
          swatch=False, chevron=False, caret=False):
    cls = "field field--focus" if focus else "field"
    parts = [f'<div class="{cls}">']
    if swatch:
        parts.append('<span class="field__swatch"></span>')
    vcls = "field__value" if mono else "field__value field__value--text"
    parts.append(f'<span class="{vcls}">{escape(value)}</span>')
    if caret:
        parts.append('<span class="caret"></span>')
    if chevron:
        parts.append(f'<span class="field__hint">{icon("chev", 12)}</span>')
    elif suffix:
        parts.append(f'<span class="field__suffix">{escape(suffix)}</span>')
    elif hint:
        parts.append(f'<span class="field__hint">{escape(hint)}</span>')
    parts.append("</div>")
    return "".join(parts)


def label(text):
    return f'<div class="insp__label">{escape(text)}</div>'


def grid(*children):
    return f'<div class="insp__grid">{"".join(children)}</div>'


# ------------------------------------------------------------------ 面板
def panel(head_html, body_html, *, locked=False, selected=False, extra=""):
    """通用面板容器。四角标记只在 selected 时挂上；extra 放需要绝对定位的装饰（指针等）。"""
    cls = "inspector"
    if selected:
        cls += " inspector--selected"
    if locked:
        cls += " inspector--locked"
    corners = ""
    if selected:
        corners = "".join(
            f'<span class="corner corner--{p}"></span>' for p in ("tl", "tr", "bl", "br")
        )
    return f'<div class="{cls}">{corners}{head_html}{body_html}{extra}</div>'


def inspector_head(name, sub, *, kind="text", letter="T", locked=False):
    if locked:
        prefix = f'<span class="insp__prefix">{icon("lock", 14)}</span>'
    else:
        prefix = badge(kind, letter)
    return (
        f'<div class="insp__head">{prefix}'
        f'<div class="insp__titles">'
        f'<div class="insp__name">{escape(name)}</div>'
        f'<div class="insp__sub">{escape(sub)}</div>'
        f"</div></div>"
    )


def inspector(name="Let’s get started", *, locked=False, selected=False,
              caret=False, pointer=False):
    sub = "Text clip · Track: Text 1" + (" · Locked" if locked else "")
    head = inspector_head(name, sub, kind="text", letter="T", locked=locked)
    head += '<div class="insp__divider"></div>'

    body = (
        label("CONTENT")
        + field(name, mono=False, focus=locked, caret=caret)
        + label("TIMING")
        + grid(
            field("0:10.03", suffix="303 f"),
            field("2.90", suffix="s"),
        )
        + label("STYLE")
        + field("Sans", mono=False, chevron=True)
        + '<div style="height:8px"></div>'
        + grid(
            field("64", hint="px"),
            field("#FFFFFF", mono=True, swatch=True),
        )
    )

    extra = ""
    if pointer:
        extra = (
            '<svg class="pointer" viewBox="0 0 12 17" style="left:150px;top:101px">'
            '<path d="M0 0v16.2l4.1-3.9 2.4 5.6 3-1.3-2.4-5.5h5.6z" '
            'fill="#15151A" stroke="#F4F4F6" stroke-width="1.2" stroke-linejoin="round"/>'
            "</svg>"
        )

    return panel(head, body, locked=locked, selected=selected, extra=extra)


# ------------------------------------------------------------------ 文档
def page(title, *, eyebrow="", lede="", body="", foot=""):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<style>
/*__CSS__*/
</style>
</head>
<body>
{body}
</body>
</html>"""


def block(num, title, desc="", meta="", body="", row_cls="row"):
    desc_html = f'<p class="block__desc">{desc}</p>' if desc else ""
    meta_html = f'<span class="block__meta">{escape(meta)}</span>' if meta else ""
    return (
        f'<section class="block">'
        f'<div class="block__head"><span class="block__num">{escape(num)}</span>'
        f"<h2>{escape(title)}</h2>{meta_html}</div>"
        f"{desc_html}"
        f'<div class="{row_cls}">{body}</div>'
        f"</section>"
    )


def cell(title, mock, note=""):
    note_html = f'<p class="cell__note">{note}</p>' if note else ""
    return f'<div class="cell"><p class="cell__title">{escape(title)}</p>{mock}{note_html}</div>'
