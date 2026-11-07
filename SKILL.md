---
name: ui-spec-kit
display_name: UI 设计系统 · HTML+SVG
display_name_en: UI Design System · HTML+SVG
version: 1.0.2
license: MIT
description: 构建可复用的 UI 设计稿与设计系统。当用户要求"出个设计稿/界面稿/原型"、"改样式/改配色/改布局"、"做个组件库/设计系统"、"照着某个产品做一版 UI"、"先设计再写代码"，或需要把设计稿交付给前端直接使用时使用。核心是 HTML+CSS 管布局、SVG 只管图标与特殊矢量，产物既能在浏览器里直接看，也能被生产代码复用。
description_zh: 构建可复用的 UI 设计稿与设计系统。HTML+CSS 负责布局、SVG 只画图标与特殊矢量，一个组件函数出全部状态，产物是可直接进项目的 CSS 与 SVG 资产，而非截图。
description_en: Build review-ready UI design specs and design systems with HTML+CSS for layout and hand-drawn SVG paths for icons. Use when asked to design a screen, restyle a component, build a component library, or produce a design spec a front-end can implement directly. Outputs are reusable CSS and SVG assets, not screenshots.
---

# UI 设计系统

## 先定一件事：什么用 HTML，什么用 SVG

这是整套方法的分水岭。用错会**慢十倍且无法复用**。

| 内容 | 用什么 | 原因 |
|---|---|---|
| 页面布局、栅格、三栏、列表、表单 | **HTML + CSS** | 浏览器负责排版，改一个 `padding` 不用重算任何坐标 |
| 卡片、面板、按钮、徽章的层次与状态 | **HTML + CSS** | `box-shadow` 一行 = SVG 里的描边 + 内高光 + 渐变三个元素 |
| 图标 | **SVG `<path>`** | 位图缩放会糊；且图标是可复用资产 |
| 特殊图形（曲线、插画、logo、波形、图表） | **SVG** | HTML 画不了非矩形几何 |
| 设计标注、尺寸线、辅助网格 | **HTML**（或 SVG 局部叠层） | 只是线段和文字，CSS 足够 |

**判断口诀**：能被「盒子 + 间距 + 边框 + 阴影」描述的，用 HTML；需要描述一条**路径**的，用 SVG。

反例（不要这样做）：把整张卡片画成一个 `<svg>`，手算 `x/y`。改一次内边距要重排所有坐标，且前端无法直接拿去用。

正例：`<div class="track-card">` + flex 布局，标题自动省略，图标 `<svg><use href="#i-lock"/></svg>`。

---

## 三层结构

```
tokens.css      设计变量：颜色 / 字号 / 间距 / 圆角。唯一来源。
   ↓
components      组件：CSS class + 生成函数（Python/JSX/模板均可）
   ↓
pages           页面：报头 + 若干 block，block 里排 cell
```

规矩：
- 组件里**不写裸值**，一律走 `var(--*)`。
- 页面里**不写新样式**，只组装组件；需要新样式就先抽组件。
- 同一个视觉重复出现两次以上 → 必须抽成组件。

---

## 设计页不是应用

这是最容易做错的地方。设计页是**关于 UI 的文档**：

- **页面用浅底深字，只有 mock-up 用应用主题的深色**。这样 mock-up 像贴在纸上，一眼分得清"这是界面"和"这是说明"。
- **页面上不放 JavaScript**。交互状态（hover / selected / disabled / editing）各画一个静态版本并排展示，而不是让它真的能点。
- **说明文字在 mock-up 外面**，面板边距或卡片下方。mock-up 内部的文字一律视为真实 UI 内容。
- **同一组对比共用栅格**：同一行的标题、卡片、说明各自对齐，不要用逐个 `margin-top` 去凑。
- **让内容自然流动**：用 grid/flex 排版，不用绝对定位。多一行、文案变长都自动撑开，不需要重新摆位置。

---

## 工作流

1. **定范围**：先问清这是哪一屏、有哪些状态、给谁看（评审 / 交付前端 / 自用）。
2. **列组件**：把这一屏拆成可复用的原子（卡片、字段、按钮、徽章、图标）。
3. **先写 tokens**：颜色、字号、间距一次定完，写进 `tokens.css`。
4. **写组件**：一个组件 = 一段 CSS + 一个生成函数（带状态参数）。
5. **组装页面**：页面函数只调用组件，不写样式。
6. **构建**：CSS 与图标 sprite 内联进 HTML，产出单文件。
7. **截图自检**（必须）：`chrome --headless --screenshot --force-device-scale-factor=2` → 裁剪放大 → 逐块看。
8. **交付**：给出可点的 HTML 链接 + 说明每个状态对应哪个 class。

**不要跳过第 7 步。** 只读代码看不出问题；实测中每轮都能抓到 2–4 处（文字溢出、虚线在浅底上不可见、装饰元素被插到错误父级、图标糊成一团）。

---

## 状态一律用修饰符，不换结构

```html
<div class="track-card track-card--locked">   <!-- 锁定 -->
<span class="toggle toggle--on">              <!-- 激活 -->
<button class="icon-btn icon-btn--danger">    <!-- 危险 -->
<button class="icon-btn" disabled>            <!-- 禁用 -->
```

好处：页面里切状态只改一个 class；组件只有一个，不会分叉成十几个"长得差不多但代码不同"的版本。

**禁用态用 `opacity: .32`**，不要试图靠把颜色调暗来实现 —— 实测在深色底上肉眼几乎分辨不出。

---

## 图标：一份数据，三种出口

图标用 `<symbol>` 定义一次：

```html
<symbol id="i-lock" viewBox="0 0 16 16">
  <g fill="none" stroke="currentColor" stroke-width="1.5"
     stroke-linecap="round" stroke-linejoin="round">…</g>
</symbol>
```

| 出口 | 用法 | 场景 |
|---|---|---|
| 内联 sprite | `<use href="#i-lock"/>` | 设计稿：零请求，`file://` 直开也能显示 |
| 独立 `icons.svg` | `<use href="icons.svg#i-lock"/>` 或整包引入 | 生产代码复用 |
| 单枚内联 | 生成函数返回 `<svg>` | 需要单独控制尺寸/颜色 |

约束：统一 `16×16` viewBox、`1.5px` 描边、round cap/join、颜色走 `currentColor`。
**带"禁用/划掉"语义的图标（eyeoff / soundoff）只能有一种标记方式** —— 同时画斜杠和叉，缩到 16px 会糊成一团。

---

## 交付即代码

产物要能直接进项目，不是一次性图片：

- `out/*.html` — 单文件（CSS + sprite 内联），可直接截图评审、发链接
- `out/ui.css` — 组件样式，前端可整份引用
- `out/icons.svg` — 图标资产

给前端的说明只需三行：用哪套 token、哪些 class、图标怎么引。

---

## 常见错误

| 症状 | 原因 | 修法 |
|---|---|---|
| 改一处要改十处 | 布局用了绝对定位 | 改 flex/grid，让容器算位置 |
| 虚线/角标看不见 | 颜色是按深底选的，却放在浅底上 | 跨界元素用**中性灰**（约 `#7A7A80`），两端都可辨 |
| 装饰元素飘到别处 | `position:absolute` 的父级没设 `relative`，或被插到了容器外 | 检查 DOM 父子关系 |
| 图标糊 | 16×16 里塞了太多细节 | 减笔画；禁用类图标只留一种标记 |
| 卡片高度对不齐 | 用固定 `height` + 内部 `margin` 凑 | 改 `padding` + `gap`，高度交给内容 |
| 长标题把按钮挤走 | 标题没设 `min-width:0` | 标题 `flex:1; min-width:0; text-overflow:ellipsis` |

---

## 本 skill 自带的可运行实现

```bash
python build.py -o ./out          # 生成全部页面
```

| 文件 | 作用 |
|---|---|
| `assets/tokens.css` | 设计变量（浅色文档 + 深色 UI 两套） |
| `assets/ui.css` | 组件样式 |
| `assets/page.css` | 设计页布局（报头 / 章节 / 栅格 / 图标墙） |
| `lib/icons.py` | 图标 path 数据 + sprite 生成 |
| `lib/components.py` | 组件函数（badge / icon_btn / toggle / track_card / field / panel / inspector） |
| `lib/pages.py` | 页面组装示例，含一个完整编辑器壳 |
| `build.py` | 构建：内联 CSS 与 sprite，导出独立资产 |

新增一个组件 = 在 `ui.css` 加一段 + 在 `components.py` 加一个函数，页面里就能用。
需要换主题 = 只改 `tokens.css`。

---

## 示例

**示例 1｜从零出一屏设计稿**
> "帮我设计一个视频编辑器的轨道区，要能看出选中、锁定、静音、隐藏这几种状态。"

先列组件（轨道卡 / 状态开关 / 操作按钮 / 徽章）→ 写 `tokens.css` → `track_card(state=…)` 一个函数出 12 种状态 → 组装成设计页（浅底文档 + 深色 mock-up 并排）→ 无头 Chrome 截图自检 → 交付 HTML 链接 + `ui.css` + `icons.svg`。

**示例 2｜改已有设计稿的样式**
> "卡片圆角改小一点，背景压暗降下来，状态徽章换成橙色系。"

只改 `tokens.css` 与 `ui.css` 里对应的变量/规则，不动页面结构；改完重新构建并截图复核，交付前后对比。**不重写整段 HTML**。

**示例 3｜把设计稿交给前端落地**
> "这套设计稿给前端用，需要能直接接进项目。"

产出三件套：`out/ui.css`（整份引用）、`out/icons.svg`（图标 sprite，`<use href="icons.svg#i-lock"/>`）、每个页面的单文件 HTML（供对照）。附三行说明：用哪套 token、哪些 class、图标怎么引。

---

## 边界

- 擅长：后台/工具类界面、组件状态矩阵、图标系统、设计 token、可交付的设计页。
- 不擅长：写实插画、复杂品牌视觉、动效编排（动效请用 `svg-motion-video` 技能走逐帧渲染）。
- 设计稿**不含 JavaScript**：交互状态一律画成并排的静态版本。
