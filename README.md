# UI Design System — 让 AI 画的设计稿，前端能直接用

一个 AI Agent 技能（Skill）：**HTML + CSS 负责布局，手绘 SVG `<path>` 负责图标**，产出可评审、可复用、可交付的设计稿。

> The same `SKILL.md` works in WorkBuddy, Claude Code, Codex, Cursor, Cline, Zed and 30+ other agents.

---

## 它解决什么问题

AI 做 UI 常见两个坑，方向相反：

**坑一：全用 HTML 堆**
按钮里的箭头用字符 `→`，图标用 emoji 或字体符号。结果是"大致像"，但箭头比例不对、图标糊、悬停态全靠猜 —— 实际产物和预期差很远，因为字符不是矢量，你无法控制它的基线、粗细和视觉重量。

**坑二：全用 SVG 画**
每张卡片手算 `x/y`，改一个 `padding` 要重排所有坐标。慢十倍、token 消耗大，而且前端拿不走 —— 那是张图，不是代码。

**这个技能给的是分工：**

| 内容 | 用什么 | 原因 |
|---|---|---|
| 栅格、三栏、列表、表单、卡片 | **HTML + CSS** | 浏览器排版，改间距不用重算坐标 |
| 层次、状态、阴影、描边 | **HTML + CSS** | 一行 `box-shadow` = SVG 里三个元素 |
| 图标 | **SVG `<path>`** | 16×16 网格手绘，`currentColor` 跟随文字色 |
| 曲线、插画、logo、图表 | **SVG** | HTML 画不了非矩形几何 |

判断口诀：**能被「盒子 + 间距 + 边框 + 阴影」描述的用 HTML；需要描述一条路径的用 SVG。**

---

## 安装

### WorkBuddy

**方式 A｜技能市场**（如果已上架）
左侧「专家·技能·连接器」→ 技能 → 搜索 `UI Design System` → 一键安装。

**方式 B｜上传技能包**
「专家·技能·连接器」→ 技能 → 添加技能 → 上传技能 → 选 `ui-spec-kit.zip`。

**方式 C｜手动放置**
把本目录复制到 `~/.workbuddy/skills/ui-spec-kit/`（Windows：`C:\Users\<你>\.workbuddy\skills\`）。

### Claude Code

```bash
git clone https://github.com/smile-shark/ui-spec-kit.git \
  ~/.claude/skills/ui-spec-kit
```

### Codex / Cursor / Cline / Zed / 其他

多数 Agent 读取 `~/.<agent>/skills/` 或项目内 `.agents/skills/`。把本目录复制进去即可 —— 格式是通用的 `SKILL.md` 文件夹。

也可以直接把仓库地址丢给任意 Agent：

> 帮我安装这个 GitHub 上的技能仓库：`smile-shark/ui-spec-kit`。先读仓库 README 里的安装说明，按你这个工具对应的方式装好，装完告诉我怎么调用。

---

## 用法

装好后直接说人话，Agent 会自动加载这个技能：

- "帮我设计一个后台的用户管理页，要能看出启用/禁用/待审核三种状态"
- "把这套设计稿的配色换成深绿系，卡片圆角小一点"
- "做个组件库，包含按钮、徽章、输入框、开关"
- "这套稿子要给前端，产出能直接引用的 CSS 和图标"

### 内置可运行实现

```bash
python build.py -o ./out
```

无第三方依赖，只用标准库。输出：

| 产物 | 说明 |
|---|---|
| `out/*.html` | 每个页面一个单文件（CSS 与图标 sprite 全内联，`file://` 直开也能看） |
| `out/index.html` | 页面索引 |
| `out/ui.css` | 组件样式，前端可整份引用 |
| `out/icons.svg` | 图标资产，`<use href="icons.svg#i-lock"/>` |

### 目录结构

```
SKILL.md              方法论：决策表 / 三层结构 / 工作流 / 常见错误 / 示例
assets/tokens.css     设计变量（浅色文档 + 深色 UI 两套），换主题只改这里
assets/ui.css         组件样式（卡片 / 面板 / 字段 / 按钮 / 开关）
assets/page.css       设计页布局（报头 / 章节 / 栅格 / 图标墙）
lib/icons.py          18 枚图标 path + sprite 生成
lib/components.py     组件函数，状态走 class 修饰符
lib/pages.py          页面组装示例，含一个完整编辑器壳
build.py              构建：内联 CSS 与 sprite，导出独立资产
```

---

## 三条关键约定

**1. 设计页不是应用。**
页面用浅底深字，只有 mock-up 用应用主题的深色 —— 像贴在纸上，一眼分得清"这是界面"和"这是说明"。页面不放 JavaScript，交互状态画成并排的静态版本。

**2. 状态一律用修饰符，不换结构。**
```html
<div class="track-card track-card--locked">
<button class="icon-btn" disabled>
```
一个组件出十几种状态，不分成十几个"长得差不多但代码不同"的版本。

**3. 交付即代码，不是截图。**
`ui.css` 和 `icons.svg` 直接进项目。给前端的说明只需三行：用哪套 token、哪些 class、图标怎么引。

---

## 授权

MIT —— 随便用、随便改、随便商用，保留版权声明即可。
