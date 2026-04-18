# 🚀 部署指南：把 K-Star Hub 发布到 GitHub（免费，5 分钟）

> 这个指南专门为不熟悉 Git 的人写的。全程用浏览器操作，不需要命令行。

---

## 🎯 总览：你会得到什么

- **一个公开的网址**：`https://你的用户名.github.io/kstarhub/`，分享给朋友即可访问
- **完全免费**：GitHub Pages 对公开仓库永久免费
- **自动 HTTPS**：GitHub 会自动给你配 SSL 证书
- **全球 CDN**：访问速度快
- **Claude 持续更新**：未来随时可以回来找 Claude 更新数据

---

## 📝 Step 1：注册 GitHub 账号（如果还没有）

1. 打开 https://github.com
2. 点右上角 **Sign up**
3. 用邮箱注册，记住你的用户名（下面都会用到）

---

## 📦 Step 2：创建仓库（Repository）

1. 登录后点右上角 **+** → **New repository**
2. 填写：
   - **Repository name**：`kstarhub`（或你喜欢的名字）
   - **Description**：`K-pop idol comeback & concert calendar`
   - 选 **Public** ✅（必须公开，GitHub Pages 免费版要求）
   - ☐ 不勾 "Add a README file"（我们已经写好了）
3. 点 **Create repository**

---

## 📤 Step 3：上传文件（浏览器拖拽，最简单）

1. 在刚创建的空仓库页面，点中间的链接 **"uploading an existing file"**
2. 从你电脑上找到这些文件，**全选后拖进网页**：
   ```
   index.html
   admin.html
   spotify_sync.py
   data-sources.md
   README.md
   .gitignore
   ```
3. 滚动到底部，在 "Commit changes" 填：
   - **Commit message**：`Initial upload of K-Star Hub`
4. 点 **Commit changes**

✅ 上传完成！你的代码现在已经在 GitHub 上了。

---

## 🌐 Step 4：开启 GitHub Pages（让网站公开可见）

1. 在仓库页面，点顶部的 **Settings**（齿轮图标）
2. 左侧菜单滚到 **Pages**
3. 在 **Source** 下选择：
   - Branch: `main`
   - Folder: `/ (root)`
4. 点 **Save**
5. 等 1-2 分钟，页面顶部会出现：
   ```
   ✅ Your site is live at https://你的用户名.github.io/kstarhub/
   ```

🎉 **这个 URL 就是你的公开网址！** 复制发给朋友，他们就能看到你的 app 了。

---

## ✏️ Step 5：分享给朋友

把这两个链接发给朋友：

```
🏠 主站：    https://你的用户名.github.io/kstarhub/
🛠️ 后台：    https://你的用户名.github.io/kstarhub/admin.html
```

朋友不需要登录任何账号，打开就能看。手机浏览器也完全支持。

---

## 🔄 Step 6：怎么持续更新（和 Claude 一起）

### 方案 A：简单方案 · 浏览器直接编辑（推荐新手）

**适合**：小改动，比如加一条新日程、改个文字、加个团体

1. 回到 Cowork 找 Claude 说："帮我更新 xxx"
2. Claude 会生成新的文件给你
3. 下载文件到电脑
4. 去 GitHub 仓库，点击要替换的文件（比如 `index.html`）
5. 右上角有个 **铅笔图标 ✏️**（Edit）旁边有 **"..."** → 选 **"Upload files"** → 拖入新文件覆盖
6. 提交 Commit，1-2 分钟后自动更新上线

### 方案 B：进阶方案 · GitHub Desktop（推荐长期运营）

**适合**：经常更新，不想每次都浏览器操作

1. 下载 [GitHub Desktop](https://desktop.github.com/)（免费，有中文）
2. 登录你的 GitHub 账号
3. **Clone** 你的 kstarhub 仓库到电脑上某个文件夹
4. 以后每次找 Claude 更新：
   - 让 Claude 直接把文件保存到这个文件夹
   - 打开 GitHub Desktop，会看到变更
   - 点 **Commit** → **Push**，自动上线

### 方案 C：自动化方案 · GitHub Actions（进阶）

**适合**：想让 Spotify 同步脚本每天自动跑

在仓库里创建 `.github/workflows/sync.yml`，让 GitHub 每天自动跑 `spotify_sync.py`，更新回归数据。

示例（需要进阶技术）：
```yaml
name: Daily Spotify Sync
on:
  schedule:
    - cron: '0 0 * * *'   # 每天 UTC 00:00
  workflow_dispatch:
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install requests python-dotenv
      - env:
          SPOTIFY_CLIENT_ID: ${{ secrets.SPOTIFY_CLIENT_ID }}
          SPOTIFY_CLIENT_SECRET: ${{ secrets.SPOTIFY_CLIENT_SECRET }}
        run: python spotify_sync.py
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "🤖 Auto-sync releases"
```

在仓库的 **Settings → Secrets and variables → Actions** 添加 Spotify 凭证。

---

## 💡 和 Claude 一起持续更新的最佳工作流

### 每周维护（5 分钟）

找 Claude 说：
> "帮我搜索本周新公布的 K-pop 回归和演唱会信息，更新 index.html 的 events 数组"

Claude 会：
1. 用网络搜索工具找最新公告
2. 更新 events 数组
3. 告诉你改了哪些

你下载新的 `index.html`，上传覆盖，1 分钟后上线。

### 新功能迭代

随时找 Claude 说：
> "给 K-Star Hub 加一个：按城市筛选演唱会"
> "加一个：抢票倒计时功能"
> "把卡通形象换成更可爱的风格"

Claude 会直接改代码，你 push 就行。

### 数据自动化（终极目标）

配好 GitHub Actions 后，每天 Spotify API 会自动同步新专辑，你什么都不用管。演唱会和音乐节信息还是需要人工或找 Claude 帮你定期搜索。

---

## 🛠️ 常见问题

**Q：GitHub Pages 会不会收费？**
A：公开仓库永久免费。每月 100GB 流量对个人项目够用了。

**Q：能用自定义域名吗？**
A：可以。在 Pages 设置里绑定 `kstarhub.com` 之类的域名（需自己买域名约 $10/年）。

**Q：朋友能帮我改吗？**
A：可以。让他们 fork 仓库 → 改 → 发 Pull Request 给你审核。

**Q：数据存在哪里？**
A：当前版本是硬编码在 `index.html` 里（JSON 格式）。规模化后应该放数据库。

**Q：上线后还能保密吗？**
A：公开仓库所有人可见。如果想私密，需要 Pro 账号（$4/月）启用私有仓库 Pages。

**Q：我忘了用户名怎么办？**
A：登录 github.com，右上角头像 → Your profile，URL 里就是你的用户名。

---

## 🎯 下一步建议

1. **现在**：先按上面 Step 1-4 部署起来，拿到公开 URL
2. **一周内**：让朋友试用，收集反馈
3. **一个月内**：配好 Spotify 自动同步（方案 C），减少维护成本
4. **更长期**：接后端数据库（Supabase 免费额度够用）、做登录系统、加推送提醒

遇到问题随时回来找 Claude！
