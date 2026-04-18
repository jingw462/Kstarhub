"""
K-Star Hub · Spotify 自动同步脚本
================================
功能：定时从 Spotify Web API 拉取指定 K-pop 团体的最新发行信息（专辑/单曲/EP），
      输出为 JSON 格式，可直接喂给你的网站后端或前端。

Spotify API 是免费的（每天 180 req/min 额度），是目前最稳定的
K-pop 回归数据自动化来源——官方公司上架后通常 1-2 小时内可以拉到。

【使用步骤】
1. 访问 https://developer.spotify.com/dashboard 创建应用，拿到 Client ID + Client Secret
2. 在本目录创建 .env 文件：
       SPOTIFY_CLIENT_ID=xxx
       SPOTIFY_CLIENT_SECRET=xxx
3. 安装依赖：
       pip install requests python-dotenv
4. 运行：
       python spotify_sync.py
5. 输出：releases.json（所有 release 按日期排序）

【推荐运行频率】
- 开发阶段：手动运行
- 生产阶段：每天凌晨 00:00 + 中午 12:00 KST 各跑一次即可
  （可用 cron / GitHub Actions / Railway 定时任务）
"""

import os
import json
import time
import base64
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID     = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
API_BASE      = "https://api.spotify.com/v1"
TOKEN_URL     = "https://accounts.spotify.com/api/token"
OUTPUT_FILE   = Path(__file__).parent / "releases.json"

# ===== 你要追踪的 K-pop 团体清单（附 Spotify Artist ID）=====
# 获取方式：在 Spotify 桌面版搜索团体 → 右键"复制艺人链接"
# 链接格式 https://open.spotify.com/artist/<ID>，<ID> 即 artist_id
KPOP_ARTISTS = {
    "BTS":         "3Nrfpe0tUJi4K4DXYWgMUX",
    "BLACKPINK":   "41MozSoPIsD1dJM0CLPjZF",
    "NewJeans":    "6HvZYsbFfjnjFrWF950C9d",
    "aespa":       "6qyi8X6MdP1lu6B1K6yh3h",
    "SEVENTEEN":   "7nqOGRxlXj7N2JYbgNEjYH",
    "Stray Kids":  "2dIgFjalVxs4ThymZ67YCE",
    "TWICE":       "7n2Ycct7Beij7Dj7meI4X0",
    "IVE":         "6RHTUrRF63xao58xh9FXYJ",
    "LE SSERAFIM": "4SpbR6yFEvexJuaBpgAU5p",
    "ATEEZ":       "2hRQKC0gqlZGPrmUKbcchR",
    "ENHYPEN":     "2r2r78NE05YjyHyVbVgqFn",
    "TXT":         "0ghlgldX5Dd6720Q3qFyQB",
    "ZEROBASEONE": "2UfieKgiaY7OtvPy4qpbbd",
    "ITZY":        "2KC9Qb60EaY0kW4eH68vr3",
    "BABYMONSTER": "35l9BRT7MXmM8bv2pAyd78",
    "KISS OF LIFE":"6f7IEZVOwKz4tJRAVuQd0s",
    "NCT 127":     "7f4ignuCJhLXfZ9giKT7rH",
    "ILLIT":       "4hjRcmNM18iyYANFdCITDH",
    "TREASURE":    "4Kt8LaMuqL5m1VXnLtd80e",
    "Red Velvet":  "1z4g3DjTBBZKhvAroFlhOM",
    "MAMAMOO":     "0XATRDCYuuGhk0oE7C0o5G",
    "NMIXX":       "2ZmXtt6Lp17B0FebiwJLkq",
    "P1Harmony":   "4IWBUUAFIplrNtaOHcJPRM",
    "&TEAM":       "5MfAxS5u1dzWLRGYEfPs17",
    "Cravity":     "2x37rMZvRFORx7nBRFzDWQ",
    "BOYNEXTDOOR": "6fpXZqMwMX7X7T8ikNChdp",
    "RIIZE":       "7hXAoKyLaOZ0d9geNxLewt",
    "(G)I-DLE":    "2AfmfGFbe0A0WsTYm0SDTx",
    "EXO":         "3cjEqqelV9zb4BYE3qDQ4O",
}


# ================ API HELPERS =================

def get_access_token():
    """用 Client Credentials Flow 拿 access token（不需要用户授权）"""
    auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    r = requests.post(
        TOKEN_URL,
        headers={"Authorization": f"Basic {auth}"},
        data={"grant_type": "client_credentials"},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def get_artist_releases(token: str, artist_id: str, limit: int = 20):
    """获取某个艺人最近的发行记录（album + single + EP）"""
    url = f"{API_BASE}/artists/{artist_id}/albums"
    params = {
        "include_groups": "album,single",
        "market": "KR",              # 韩区市场，拿到的是官方韩语发行
        "limit": limit,
        "offset": 0,
    }
    r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, params=params, timeout=10)
    r.raise_for_status()
    return r.json().get("items", [])


# ================ MAIN =================

def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        raise SystemExit("❌ 请先在 .env 配置 SPOTIFY_CLIENT_ID 和 SPOTIFY_CLIENT_SECRET")

    print("🔑 获取 access token...")
    token = get_access_token()

    all_releases = []
    today = datetime.now()
    cutoff = today - timedelta(days=180)   # 只保留近 6 个月 + 未来

    for name, artist_id in KPOP_ARTISTS.items():
        try:
            print(f"📡 同步 {name}...")
            releases = get_artist_releases(token, artist_id)
            for rel in releases:
                # 解析发行日（可能是 YYYY, YYYY-MM, YYYY-MM-DD 三种精度）
                rd = rel.get("release_date", "")
                precision = rel.get("release_date_precision", "day")
                try:
                    if precision == "year":
                        rd_obj = datetime.strptime(rd, "%Y")
                    elif precision == "month":
                        rd_obj = datetime.strptime(rd, "%Y-%m")
                    else:
                        rd_obj = datetime.strptime(rd, "%Y-%m-%d")
                except ValueError:
                    continue

                if rd_obj < cutoff:
                    continue

                all_releases.append({
                    "artist":       name,
                    "title":        rel["name"],
                    "type":         rel["album_type"],     # album / single / compilation
                    "release_date": rd,
                    "precision":    precision,
                    "total_tracks": rel["total_tracks"],
                    "spotify_url":  rel["external_urls"]["spotify"],
                    "image":        rel["images"][0]["url"] if rel["images"] else None,
                })
            time.sleep(0.2)   # 礼貌限速
        except Exception as e:
            print(f"⚠️ {name} 失败：{e}")

    # 按日期降序
    all_releases.sort(key=lambda x: x["release_date"], reverse=True)

    OUTPUT_FILE.write_text(
        json.dumps({
            "synced_at": datetime.now().isoformat(),
            "count":     len(all_releases),
            "releases":  all_releases,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n✅ 完成！共 {len(all_releases)} 条记录")
    print(f"📁 输出：{OUTPUT_FILE}")

    # 打印最近 10 条
    print("\n🔥 最近 10 条发行：")
    for r in all_releases[:10]:
        print(f"  {r['release_date']}  {r['artist']:<14}  [{r['type']:<6}]  {r['title']}")


if __name__ == "__main__":
    main()
