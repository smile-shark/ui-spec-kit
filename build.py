#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建器：把 lib/pages.py 里的页面装配成独立 HTML。

用法：
    python build.py                 # 输出到 ./out
    python build.py -o ../dist      # 指定输出目录
    python build.py --css-only      # 只导出 css，给生产项目用

产物特点：
- CSS 全内联 → 单文件，截图/转发不丢样式
- 图标 sprite 内联 → 零网络请求，file:// 直接打开也能显示
- 同时导出 icons.svg 与 tokens.css/ui.css 独立文件，生产代码可直接复用
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from lib.pages import PAGES                    # noqa: E402
from lib.icons import sprite_html, sprite_file  # noqa: E402

ASSETS = os.path.join(HERE, "assets")


def read_css():
    parts = []
    for name in ("tokens.css", "ui.css", "page.css"):
        with open(os.path.join(ASSETS, name), encoding="utf-8") as f:
            parts.append(f"/* ---- {name} ---- */\n" + f.read())
    return "\n".join(parts)


def build(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    css = read_css()
    sprite = sprite_html()

    # 独立资产：生产项目可直接引用
    with open(os.path.join(out_dir, "icons.svg"), "w", encoding="utf-8") as f:
        f.write(sprite_file())
    with open(os.path.join(out_dir, "ui.css"), "w", encoding="utf-8") as f:
        f.write(css)

    written = []
    for slug, fn in PAGES:
        html = fn()
        html = html.replace("/*__CSS__*/", css)
        html = html.replace("<body>\n", "<body>\n" + sprite + "\n", 1)
        path = os.path.join(out_dir, f"{slug}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        written.append((slug, len(html)))

    # 索引页
    display = {
        "track-cards": ("轨道卡 · 状态矩阵", "12 种状态，一个组件"),
        "inspector": ("属性面板 · 两态", "常规 / 选中并锁定"),
        "icons": ("图标库 · 18 枚", "16×16 手绘，三种出口"),
        "editor": ("整页编辑器", "三栏 + 时间轴，grid 自动排布"),
    }
    links = "".join(
        f'<li><a href="{slug}.html"><span>{display.get(slug, (slug, ""))[0]}</span>'
        f'<em>{display.get(slug, ("", ""))[1]}</em></a></li>'
        for slug, _ in PAGES
    )
    index = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>UI 设计稿索引</title>
<style>{css}
.index{{max-width:720px;margin:120px auto;padding:0 40px}}
.index h1{{font-size:24px;letter-spacing:-.5px;margin:0 0 8px}}
.index p{{color:var(--page-fg-2);font-size:13px;line-height:1.7;margin:0 0 28px}}
.index ul{{list-style:none;padding:0;margin:0;border-top:1px solid var(--page-rule)}}
.index li{{border-bottom:1px solid var(--page-rule)}}
.index a{{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:16px 2px;color:inherit;text-decoration:none;font-size:14px}}
.index em{{font-style:normal;font-size:11.5px;color:var(--page-fg-3)}}
.index a:hover{{color:#A8641C}}
</style></head>
<body><div class="index">
<h1>UI 设计稿</h1>
<p>每个页面都是独立 HTML，可直接截图评审；组件与图标在 <code>lib/</code> 里复用。</p>
<ul>{links}</ul>
</div></body></html>"""
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index)

    for slug, size in written:
        print(f"  {slug}.html  {size/1024:.1f} KB")
    print(f"  icons.svg   {os.path.getsize(os.path.join(out_dir, 'icons.svg'))/1024:.1f} KB")
    print(f"  ui.css      {os.path.getsize(os.path.join(out_dir, 'ui.css'))/1024:.1f} KB")
    print(f"→ {out_dir}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=os.path.join(HERE, "out"))
    args = ap.parse_args()
    build(os.path.abspath(args.out))
