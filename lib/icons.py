# -*- coding: utf-8 -*-
"""
图标库：唯一数据源是 ICONS 里的 path 描述。

同一个 path 集合有三种产出，互相等价：
1. sprite_html()  -> 内联进设计稿头部，页面里 <svg><use href="#i-lock"/></svg>
2. sprite_file()  -> 独立 icons.svg，生产代码可直接 <img> 或复制 <symbol>
3. icon()         -> 单枚内联，用于需要独立控制尺寸/颜色的地方

新增图标只需往 ICONS 里加一条，不用改任何 CSS。
"""

ICONS = {
    "up": '<path d="M8 13.4V3.2"/><path d="M3.6 7.4 8 3l4.4 4.4"/>',
    "down": '<path d="M8 2.6v10.2"/><path d="M3.6 8.6 8 13l4.4-4.4"/>',
    "trash": (
        '<path d="M2.4 4.6h11.2"/>'
        '<path d="M6.1 4.6V3.2a1.1 1.1 0 0 1 1.1-1.1h1.6a1.1 1.1 0 0 1 1.1 1.1v1.4"/>'
        '<path d="M4.1 4.6l.6 8.2a1.4 1.4 0 0 0 1.4 1.3h3.8a1.4 1.4 0 0 0 1.4-1.3l.6-8.2"/>'
        '<path d="M6.6 7.1v4.4M9.4 7.1v4.4"/>'
    ),
    "lock": (
        '<rect x="3.4" y="7" width="9.2" height="6.5" rx="1.8"/>'
        '<path d="M5.7 7V5.3a2.3 2.3 0 0 1 4.6 0V7"/>'
    ),
    "eye": (
        '<path d="M1.3 8S3.9 3.8 8 3.8 14.7 8 14.7 8 12.1 12.2 8 12.2 1.3 8 1.3 8Z"/>'
        '<circle cx="8" cy="8" r="2"/>'
    ),
    "eyeoff": (
        '<path d="M1.3 8S3.9 3.8 8 3.8 14.7 8 14.7 8 12.1 12.2 8 12.2 1.3 8 1.3 8Z"/>'
        '<circle cx="8" cy="8" r="2"/>'
        '<path d="M3.1 12.9 12.9 3.1"/>'
    ),
    "sound": (
        '<path d="M2.4 6.2h2.3L8 3.5v9L4.7 9.8H2.4z"/>'
        '<path d="M10.5 6.3a2.7 2.7 0 0 1 0 3.5"/>'
        '<path d="M12.6 5a4.9 4.9 0 0 1 0 6"/>'
    ),
    "soundoff": (
        '<path d="M2.4 6.2h2.3L8 3.5v9L4.7 9.8H2.4z"/>'
        '<path d="M10.7 6.5l2.9 3M13.6 6.5l-2.9 3"/>'
    ),
    "chev": '<path d="m4.2 6.4 3.8 3.8 3.8-3.8"/>',
    "plus": '<path d="M8 3.2v9.6M3.2 8h9.6"/>',
    "check": '<path d="m3.4 8.4 3 3 6.2-6.6"/>',
    "dots": '<circle cx="3.6" cy="8" r="1.1"/><circle cx="8" cy="8" r="1.1"/><circle cx="12.4" cy="8" r="1.1"/>',
    "play": '<path fill="currentColor" stroke="none" d="M5.6 3.4 12.9 8l-7.3 4.6z"/>',
    "cut": '<circle cx="4.3" cy="4.3" r="2.1"/><circle cx="4.3" cy="11.7" r="2.1"/><path d="M6 5.6 12.8 12M6 10.4 12.8 4"/>',
    "text": '<path d="M3.4 3.6h9.2M8 3.6v9"/>',
    "zoom": '<circle cx="7.2" cy="7.2" r="4.4"/><path d="m10.6 10.6 2.8 2.8"/>',
    "undo": '<path d="M3 7.4h6.2a3.4 3.4 0 0 1 0 6.8H6"/><path d="M5.6 4.6 2.8 7.4l2.8 2.8"/>',
    "redo": '<path d="M13 7.4H6.8a3.4 3.4 0 0 0 0 6.8H10"/><path d="m10.4 4.6 2.8 2.8-2.8 2.8"/>',
}

# 这些图标带“划掉/禁用”语义，使用时通常是告警色
ALERT_STATES = {"eyeoff", "soundoff"}


def _symbols():
    out = []
    for name, body in ICONS.items():
        out.append(
            f'<symbol id="i-{name}" viewBox="0 0 16 16">'
            f'<g fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round">{body}</g>'
            f"</symbol>"
        )
    return "".join(out)


def sprite_html(hidden=True):
    """内联 sprite：挂在页面最顶部，之后所有 <use href="#i-xxx"> 都零网络请求。"""
    style = ' style="display:none"' if hidden else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg"{style} aria-hidden="true">{_symbols()}</svg>'


def sprite_file():
    """独立 icons.svg：生产代码可直接当资产引用。"""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" '
        'style="display:none" aria-hidden="true">' + _symbols() + "</svg>"
    )


def icon(name, size=16, cls="", style=""):
    """单枚内联图标。颜色由 CSS 的 color 控制（currentColor 继承）。"""
    if name not in ICONS:
        raise KeyError(f"unknown icon: {name}")
    c = f' class="{cls}"' if cls else ""
    s = f' style="{style}"' if style else ""
    return (
        f'<svg{c}{s} width="{size}" height="{size}" viewBox="0 0 16 16" aria-hidden="true">'
        f'<use href="#i-{name}"/></svg>'
    )
