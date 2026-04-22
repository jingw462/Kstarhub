# K-Star Hub ✨

> 一站式 K-pop 追星日历 — 回归 / 演唱会 / 音乐节 / Fan Meet
> 每日自动抓取最新新闻 · 4 语言切换 · 签到升级 · 5 款可解锁皮肤

[![Made with Claude](https://img.shields.io/badge/Made%20with-Claude-c4a07a)](https://claude.ai)
[![GitHub Pages](https://img.shields.io/badge/Hosted%20on-GitHub%20Pages-a68968)](https://pages.github.com)
[![Auto-Update](https://img.shields.io/badge/News-Auto%20Updated%20Daily-2d2a24)](./AUTO_UPDATE_SETUP.md)

## 👀 在线预览

🌏 **https://jingw462.github.io/Kstarhub/**

## 🌟 核心功能

### 📅 追星日历
- **33 个热门团体**：BTS、BLACKPINK、NewJeans、aespa、SEVENTEEN、Stray Kids、TWICE、IVE、LE SSERAFIM、ENHYPEN、ITZY、TXT、Cortis（HYBE 最新男团）等
- **41+ 真实日程**：2026 年回归、世界巡演（BTS ARIRANG / ENHYPEN BLOOD SAGA 等）、Waterbomb / KCON / Rock in Rio 等音乐节
- **时区切换**：🇰🇷 KST · 🇨🇳 CST · 🇺🇸 EDT · 🇺🇸 PDT，点一下自动换算所有日程时间
- **性别/类型过滤**：男团 / 女团 / 混合团 · 回归 / 演唱会 / 音乐节 / Fan Meet
- **团体详情页**：点击头像看出道日期、风格、团队介绍、近期日程、Weverse 深链

### 🌐 多语言
- **中文 / English / 한국어 / Español** 四语切换
- 日程标题、地点、风格均有对应翻译字典

### 🤖 新闻自动更新
- 每日 00:00 UTC GitHub Actions 自动从 **Soompi / allkpop / Reddit r/kpop** 抓 RSS
- 过滤 33 个跟踪团体的头条，写入 `news.json`
- Pages 自动重建，"最新"页面实时刷新
- 零依赖 RSS 解析器（不用 npm install）
- 详见 [AUTO_UPDATE_SETUP.md](./AUTO_UPDATE_SETUP.md)

### ⭐ 养成玩法（新）
- **追星等级**：6 级成长系统（新手粉 → 星光大使）
- **星光值**：签到 +10~50 · 收藏日程 +2 · 关注团体 +5 · 首次打开团体页 +1
- **每日签到**：打开 App 自动签到，7 天循环奖励递增（第 7 天大礼）
- **5 款主页皮肤**：📜 米白简约（默认）· 🌸 樱花粉（80⭐）· 🌊 海蓝（200⭐）· 🌃 午夜蓝（400⭐，深色模式）· 🌅 日落橙（800⭐）
- 所有进度 localStorage 持久化，换设备也能继续追星

### 🎨 视觉风格
- **Paper & Cream** 简约配色：暖米白 + 焦糖色，低饱和无刺眼粉紫
- 米白 / 纯白交替，细边 + 柔和阴影
- 所有卡片都有圆角、卡通 emoji，规避肖像权

## 📁 项目结构

```
Kstarhub/
├── index.html                      # 单页 App（UI + 事件 + i18n + 状态）
├── news.json                       # 自动更新的新闻种子
├── scripts/
│   └── fetch-news.mjs              # 零依赖 RSS 抓取器
├── .github/workflows/
│   └── update-data.yml             # 每日 GitHub Actions
├── README.md                       # 你正在看这个
├── AUTO_UPDATE_SETUP.md            # 部署 + 自动更新 pipeline 指南
├── DEPLOY.md                       # GitHub Pages 基础部署
├── data-sources.md                 # 数据源说明
└── .gitignore
```

## 🚀 快速开始

**本地预览** — 直接双击 `index.html`，任何浏览器都能打开。

**公开部署** — 查看 [AUTO_UPDATE_SETUP.md](./AUTO_UPDATE_SETUP.md) 获取部署 + 每日自动更新的完整指南。

**手动刷新新闻** —
```bash
cd Kstarhub
node scripts/fetch-news.mjs
git add news.json index.html
git commit -m "Manual refresh"
git push
```

## 🛡️ 版权与合规

- ✅ 仅使用**真实团体名**（属于公开信息）+ **原创 emoji 形象**
- ❌ 不使用艺人照片、专辑封面、官方 logo 或 IP
- ✅ 新闻只显示 Soompi/allkpop/Reddit 的**标题 + 摘要 + 原文链接**（合理使用）
- 详见 [data-sources.md](./data-sources.md)

## 📊 数据来源

日程数据快照：**2026/04/21**，来源：

- [Soompi](https://www.soompi.com) · [Billboard](https://www.billboard.com) · [allkpop](https://www.allkpop.com)
- [Kpop Profiles](https://kprofiles.com) · [Ticketmaster](https://www.ticketmaster.com)
- [Reddit r/kpop](https://reddit.com/r/kpop) · [Wikipedia](https://wikipedia.org)（公开报道）

## 🛠️ 技术栈

- **纯静态**：HTML + CSS + vanilla JS，无框架、无打包
- **GitHub Pages** 托管，**GitHub Actions** 每日更新
- **Node 20** RSS 抓取（原生 `fetch` + 正则解析器，零依赖）
- **localStorage** 状态持久化（多语言、收藏、关注、等级、签到、皮肤）
- **CSS 变量** 驱动主题切换（5 款皮肤一键换肤）

## 🤝 参与贡献

- 想加新团体？编辑 `index.html` 里 `GROUPS` 数组（~line 1090）
- 想加日程？编辑 `events` 数组（~line 1453）
- 想加 RSS 源？编辑 `scripts/fetch-news.mjs` 里 `FEEDS` 数组
- 想加皮肤？编辑 `index.html` 里 `SKINS` 数组，5 个 CSS 变量即可

## 📜 License

MIT — 欢迎 fork / 二次创作。卡通 emoji 形象为 Unicode 通用符号，不涉及任何官方 IP。

---

Made with ✨ by K-pop 粉丝，for K-pop 粉丝。
