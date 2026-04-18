# K-Star Hub ✨

> 一站式 K-pop 追星日历 — 回归 / 演唱会 / 音乐节 / Fan Meet

[![Made with Claude](https://img.shields.io/badge/Made%20with-Claude-ff6fb5)](https://claude.ai)
[![GitHub Pages](https://img.shields.io/badge/Hosted%20on-GitHub%20Pages-8a5cf6)](https://pages.github.com)

## 👀 在线预览

- 🏠 主站（用户端）：https://YOUR_USERNAME.github.io/kstarhub/
- 🛠️ 管理后台：https://YOUR_USERNAME.github.io/kstarhub/admin.html

*（上线后把 `YOUR_USERNAME` 改成你的 GitHub 用户名）*

## 🌟 功能特性

- **32 个热门团体**：BTS、BLACKPINK、NewJeans、aespa、SEVENTEEN、Stray Kids 等
- **44+ 真实日程**：回归、世界巡演、音乐节、Fan Meet
- **4 档时区切换**：🇰🇷 韩国 · 🇨🇳 中国 · 🇺🇸 美东 · 🇺🇸 美西
- **性别分类**：男团 / 女团 / 混合团
- **个性化收藏**：关注团体、收藏日程、贴纸收集玩法
- **卡通 emoji 形象**：规避肖像权，视觉统一
- **零依赖**：纯 HTML + CSS + JS，任何浏览器打开即用

## 📁 项目结构

```
kstarhub/
├── index.html          # 主站 — 用户追星日历
├── admin.html          # 管理后台 — 录入日程
├── spotify_sync.py     # 自动化脚本 — 从 Spotify API 同步回归数据
├── data-sources.md     # 数据源完整指南（11 个 API + 各区票务平台）
├── README.md           # 你正在看的文件
└── .gitignore          # Git 忽略清单
```

## 🚀 快速开始

**想本地预览？** 直接双击 `index.html` 即可（所有浏览器都支持）。

**想公开部署？** 查看 [DEPLOY.md](./DEPLOY.md) 获取 5 分钟 GitHub Pages 部署指南。

**想自动同步回归数据？**
```bash
pip install requests python-dotenv
# 在 .env 中填入 Spotify API 凭证
python spotify_sync.py
```

## 🛡️ 版权与合规

- ✅ 使用**真实团体名** + **原创 emoji 形象**
- ❌ 不使用艺人照片、专辑封面、官方 IP
- 详见 [data-sources.md](./data-sources.md) 第七章"法律与合规提示"

## 📊 数据来源

所有日程均来自公开报道（2026/04/17 快照）：
- [Soompi](https://www.soompi.com)
- [Billboard](https://www.billboard.com)
- [allkpop](https://www.allkpop.com)
- [Kpop Profiles](https://kprofiles.com)
- [Ticketmaster](https://www.ticketmaster.com)

## 🤝 参与贡献

欢迎提交 Pull Request 补充日程、修正错误、新增团体。

## 📜 License

MIT — 欢迎 fork / 二次创作。卡通 emoji 形象为通用符号，不涉及任何官方 IP。

---

Made with 💜 by K-pop 粉丝，为 K-pop 粉丝。
