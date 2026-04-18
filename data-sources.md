# K-Star Hub · 数据源获取完全指南

> 整理日期：2026/04/17
> 目的：给未来的技术团队和内容编辑看 — 所有 K-pop 日程数据该从哪里取、怎么取、频率多少、难度多大。

---

## 一、数据类型分级

按"自动化难度"从易到难排：

| 数据类型 | 自动化难度 | 推荐方案 | 更新频率 |
|---|---|---|---|
| 专辑/单曲发行（回归） | ⭐ 简单 | Spotify/Apple Music API | 每日 2 次 |
| 世界巡演已公布日期 | ⭐⭐ 中等 | Ticketmaster + Songkick API | 每日 1 次 |
| 音乐节阵容 | ⭐⭐⭐ 较难 | 官方网站 + 人工 | 每周 2 次 |
| 开票时间（Ticketing） | ⭐⭐⭐⭐ 困难 | 人工爬 + 粉丝投稿 | 每日人工 |
| Fan Meet 小型活动 | ⭐⭐⭐⭐ 困难 | Weverse + 人工 | 每日人工 |
| 打歌舞台/综艺 | ⭐⭐⭐⭐⭐ 极难 | 人工为主 | 每日人工 |

---

## 二、推荐的免费/低成本数据源

### 1. Spotify Web API ⭐ 强烈推荐

- **网址**：https://developer.spotify.com/documentation/web-api
- **能拿到什么**：艺人的所有专辑、EP、单曲发行日期、封面、曲目数
- **费用**：完全免费
- **额度**：180 次/分钟（K-pop Top 30 完全够用）
- **认证**：Client Credentials Flow（不需要用户授权）
- **难度**：★☆☆☆☆
- **更新时效**：官方上架后通常 1-2 小时内可抓到
- **对应脚本**：`spotify_sync.py`（已提供）

### 2. Apple Music API（iTunes Search API）

- **网址**：https://developer.apple.com/documentation/applemusicapi
- **iTunes Search**：https://itunes.apple.com/search?term=BTS&entity=album（免认证）
- **能拿到什么**：专辑信息 + 预售日期（Apple 通常比 Spotify 早 1-2 天开放预订）
- **费用**：免费（开发者账号 99 美元/年可用完整 Apple Music API）
- **难度**：★★☆☆☆

### 3. Ticketmaster Discovery API

- **网址**：https://developer.ticketmaster.com
- **能拿到什么**：北美、欧洲主要演唱会日期、场馆、票价段、开票时间
- **费用**：免费
- **额度**：5000 次/天
- **难度**：★★☆☆☆
- **盲点**：亚洲地区演唱会覆盖差（亚洲主要是 Interpark、Yes24、Melon Ticket，没有官方 API）

### 4. Songkick API

- **网址**：https://www.songkick.com/developer
- **能拿到什么**：全球演唱会聚合数据
- **费用**：免费（需申请 API key）
- **难度**：★★☆☆☆
- **优势**：覆盖面比 Ticketmaster 广一些

### 5. Bandsintown API

- **网址**：https://app.bandsintown.com/api/overview
- **能拿到什么**：艺人的巡演日期（演唱会数据聚合）
- **费用**：免费
- **难度**：★★☆☆☆

### 6. MusicBrainz API

- **网址**：https://musicbrainz.org/doc/MusicBrainz_API
- **能拿到什么**：非常完整的音乐元数据（专辑、艺人关系、成员变动）
- **费用**：完全免费
- **难度**：★★★☆☆（数据结构复杂）
- **优势**：唯一开源且可下载整个数据库的方案

---

## 三、K-pop 专业社区数据源（需人工或受限爬取）

### 7. Soompi / allkpop / KpopStarz（媒体）

- **用途**：最快的回归/巡演官宣新闻来源
- **怎么用**：订阅 RSS / 抓取官方 Twitter 账号
- **Twitter 账号**：@soompi, @allkpop, @koreaboo, @kculture
- **难度**：★★★☆☆（要做 NLP 抽取日期）
- **合规**：只抓事实信息（日期、标题），不复制原文

### 8. kprofiles.com / dbkpop.com

- **用途**：社区手工维护的月度回归清单
- **适合用作**：交叉验证，而不是主数据源
- **注意**：查看 robots.txt，尊重爬取频率

### 9. Kpopping.com

- **用途**：最完整的 K-pop 日历类社区
- **难度**：没有公开 API，抓取需谨慎

### 10. 官方 Weverse 账号

- **网址**：https://weverse.io
- **每个公司的账号**：BTS、SEVENTEEN、TXT、ENHYPEN 等 HYBE 系都在 Weverse
- **用途**：抓"通知"板块可以拿到官方一手消息
- **难度**：★★★★☆（需要账号+token）

### 11. 娱乐公司官网（一手信息）

| 公司 | 官网 | 旗下主要团体 |
|---|---|---|
| HYBE | hybecorp.com | BTS, TXT, ENHYPEN, LE SSERAFIM, NewJeans |
| SM | smentertainment.com | aespa, NCT, Red Velvet, RIIZE, EXO |
| YG | ygfamily.com | BLACKPINK, TREASURE, BABYMONSTER |
| JYP | jype.com | TWICE, Stray Kids, ITZY, NMIXX |
| Starship | starship-ent.com | IVE, Cravity, MONSTA X |
| KQ | kqent.com | ATEEZ |
| WAKEONE | wakeone.co.kr | ZEROBASEONE, izna |

---

## 四、开票时间 — 最头疼的一块

**为什么难**：每个区域每个票务平台格式完全不一样，开票时间经常只提前 1-2 天公布。

### 各区主要票务平台

| 地区 | 平台 | API 情况 |
|---|---|---|
| 韩国 | Interpark Ticket | 无公开 API，需爬 |
| 韩国 | Yes24 Ticket | 无公开 API，需爬 |
| 韩国 | Melon Ticket | 无公开 API |
| 日本 | Ticket Pia, e+, Rakuten | 无公开 API |
| 北美 | Ticketmaster | ✅ 有 API |
| 北美 | AXS | 无公开 API |
| 东南亚 | Klook | ⚠️ 有 API 但仅限合作伙伴 |
| 中国 | 大麦、猫眼 | 无公开 API |
| 欧洲 | Ticketmaster UK, Eventim | Ticketmaster 有 API |

### 现实策略

1. **北美票务** → 接 Ticketmaster API 自动拿
2. **亚洲票务** → 人工监控 + 粉丝投稿 + 官方 Twitter 通知
3. **开票前 7 天内的新开票** → 人工兼职编辑每日手动录入

---

## 五、推荐的数据架构

```
[定时任务]
  ├── Spotify Sync（每天 2 次）         → 回归数据
  ├── Ticketmaster Sync（每天 1 次）    → 北美演唱会
  ├── Songkick Sync（每天 1 次）        → 全球演唱会
  └── RSS Parser（每小时 1 次）         → Soompi/allkpop 官宣新闻

      ↓

[数据库 PostgreSQL]
  tables:
    artists, groups, events, venues,
    ticket_sales, festivals, sources

      ↓

[审核后台（你提供的 kpop-admin.html 演进版）]
  - 自动抓取数据进入"待审核"队列
  - 编辑确认后发布到前台
  - 人工补录自动抓不到的（开票时间、Fan Meet）

      ↓

[用户前台（主站 kpop-calendar.html）]
  - 读取 API → 展示
  - 支持时区切换 / 订阅 / 推送
```

---

## 六、冷启动阶段的建议工作流

**第 1-4 周（验证期）**
- 只跑 Spotify 脚本（全自动）
- Top 20 团体，人工每天花 30 分钟补录演唱会和开票
- 每周发 1 次"本周重要日程"邮件/社群推送

**第 5-12 周（增长期）**
- 接 Ticketmaster + Songkick API
- 招 1-2 个兼职编辑（可以是在校粉丝），日更
- 上线"粉丝投稿"功能，开始众包

**第 13-24 周（规模化）**
- 扩展到 Top 100 团体
- 上线自动化 RSS 抓取 + NLP 日期抽取
- 投稿信用系统上线（老用户权重高）

---

## 七、法律与合规提示

1. **团体/艺人名称**：可以直接使用（事实引用）
2. **专辑/歌曲名称**：可以直接使用（事实引用）
3. **演唱会名称、场馆名称、日期**：都可以使用
4. **艺人照片**：❌ 不要用（肖像权 + 版权）
5. **专辑封面**：⚠️ 小尺寸缩略图 + 原始来源链接可能 OK，但最安全是不用
6. **Logo**：⚠️ 小尺寸引用可能 OK，建议不用
7. **官方 IP 角色**（BT21、TinyTAN、SKZOO 等）：❌ 绝对不要用
8. **爬取**：遵守每个站点的 robots.txt，限频率（每秒 1 次以内），加 User-Agent 说明身份
9. **API 使用**：遵守每个 API 的 Terms of Service，Spotify/Apple 都不允许你缓存完整专辑列表用于商业推广

---

## 八、附：真正商业化的选择

如果做大到需要非常完整的数据，可以考虑**付费数据服务**：

- **Pollstar**（巡演数据权威）: 商业订阅，月费 $300+
- **Billboard Boxscore**（巡演票房）: 商业订阅
- **Luminate (原 MRC Data)**: K-pop 销量/streaming 数据，付费

冷启动不需要，规模做起来后再考虑。

---

**祝你的 K-Star Hub 顺利上线！**
