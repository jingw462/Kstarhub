#!/usr/bin/env node
// K-Star Hub · Daily auto-updater
// Runs via GitHub Actions. Zero dependencies (pure Node 20 stdlib).
//
// What it does:
//   1. Fetches RSS feeds from Soompi + allkpop
//   2. Filters headlines that mention any of our 33 tracked groups
//   3. Writes news.json (consumed by index.html at runtime)
//   4. Bumps the "updated on" date in index.html banners (all 4 languages)
//
// Fails gracefully: if a feed is down, it skips that one and keeps going.

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

// ==================== CONFIG ====================

const FEEDS = [
  { name: 'Soompi',  url: 'https://www.soompi.com/feed' },
  { name: 'allkpop', url: 'https://www.allkpop.com/feed' },
  { name: 'Reddit · r/kpop', url: 'https://www.reddit.com/r/kpop/.rss' },
];

// Keywords matched against article titles (case-insensitive). Ordered longest-first
// so "LE SSERAFIM" matches before "LE" in aspirational edge cases.
const GROUP_KEYWORDS = [
  'ZEROBASEONE','BOYNEXTDOOR','BABYMONSTER','LE SSERAFIM','BLACKPINK',
  'KISS OF LIFE','Red Velvet','P1Harmony','Stray Kids','MAMAMOO',
  'SEVENTEEN','TREASURE','ENHYPEN','NewJeans','Cravity','(G)I-DLE',
  'CORTIS','NCT 127','NMIXX','&TEAM','ATEEZ','ILLIT','RIIZE','aespa',
  'KARD','AKMU','TWICE','izna','BTS','TXT','EXO','IVE','ITZY',
];

const MAX_ITEMS = 40; // cap output to avoid a bloated json file

// ==================== RSS PARSER (zero deps) ====================

function stripCdata(s) {
  return (s || '').replace(/^\s*<!\[CDATA\[/, '').replace(/\]\]>\s*$/, '').trim();
}

function decodeEntities(s) {
  return (s || '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#x27;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&apos;/g, "'");
}

function stripHtml(s) {
  return (s || '').replace(/<[^>]+>/g, '').trim();
}

function extractTag(raw, tag) {
  // Handles <tag>...</tag>, <tag attr="x">...</tag>, and self-closing <tag href="..."/>
  const selfClose = new RegExp(`<${tag}[^>]*?href=["']([^"']+)["'][^>]*/?>`, 'i');
  const selfMatch = raw.match(selfClose);
  if (selfMatch) return selfMatch[1];
  const re = new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)<\\/${tag}>`, 'i');
  const m = raw.match(re);
  return m ? stripCdata(m[1]) : '';
}

function parseRss(xml) {
  const items = [];
  // Works for both RSS 2.0 <item> and Atom <entry>
  const tagRegex = /<(item|entry)\b[\s\S]*?<\/\1>/gi;
  const matches = xml.match(tagRegex) || [];
  for (const raw of matches) {
    const title       = decodeEntities(stripHtml(extractTag(raw, 'title')));
    const linkRaw     = extractTag(raw, 'link');
    const link        = linkRaw || extractTag(raw, 'guid');
    const pubDate     = extractTag(raw, 'pubDate') || extractTag(raw, 'updated') || extractTag(raw, 'published');
    const description = decodeEntities(stripHtml(extractTag(raw, 'description'))).slice(0, 240);
    if (title && link) items.push({ title, link, pubDate, description });
  }
  return items;
}

function matchGroups(title) {
  const upper = title.toUpperCase();
  const hits = [];
  for (const kw of GROUP_KEYWORDS) {
    if (upper.includes(kw.toUpperCase())) hits.push(kw);
  }
  return hits;
}

// ==================== MAIN ====================

async function fetchFeed(feed) {
  console.log(`→ Fetching ${feed.name}`);
  try {
    const res = await fetch(feed.url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; KStarHubBot/1.0; +https://jingw462.github.io/Kstarhub/)',
        'Accept': 'application/rss+xml, application/atom+xml, application/xml, text/xml, */*',
      },
      signal: AbortSignal.timeout(20_000),
    });
    if (!res.ok) {
      console.warn(`  ✗ ${feed.name} returned ${res.status}`);
      return [];
    }
    const xml = await res.text();
    const items = parseRss(xml);
    console.log(`  ✓ ${feed.name} · ${items.length} items`);
    return items.map(it => ({ ...it, source: feed.name }));
  } catch (e) {
    console.warn(`  ✗ ${feed.name} failed: ${e.message}`);
    return [];
  }
}

async function updateNewsJson() {
  const all = [];
  for (const feed of FEEDS) {
    const items = await fetchFeed(feed);
    for (const it of items) {
      const groups = matchGroups(it.title);
      if (!groups.length) continue;
      const dateIso = it.pubDate ? new Date(it.pubDate).toISOString() : new Date().toISOString();
      all.push({
        source: it.source,
        title: it.title,
        link: it.link,
        date: dateIso,
        description: it.description,
        groups,
      });
    }
  }

  // Deduplicate by link, sort newest first
  const byLink = new Map();
  for (const n of all) if (!byLink.has(n.link)) byLink.set(n.link, n);
  const sorted = [...byLink.values()].sort((a, b) => new Date(b.date) - new Date(a.date));
  const top = sorted.slice(0, MAX_ITEMS);

  const payload = {
    generatedAt: new Date().toISOString(),
    count: top.length,
    items: top,
  };

  const outPath = path.join(ROOT, 'news.json');
  await fs.writeFile(outPath, JSON.stringify(payload, null, 2));
  console.log(`\n✔ Wrote ${top.length} items to news.json`);
  return payload;
}

async function bumpBannerDate() {
  const htmlPath = path.join(ROOT, 'index.html');
  let html;
  try {
    html = await fs.readFile(htmlPath, 'utf8');
  } catch (e) {
    console.warn('Could not read index.html:', e.message);
    return;
  }
  const today = new Date().toISOString().slice(0, 10).replace(/-/g, '/'); // 2026/04/21
  const before = html;
  html = html
    .replace(/更新于 \d{4}\/\d{2}\/\d{2}/g, `更新于 ${today}`)
    .replace(/Updated \d{4}\/\d{2}\/\d{2}/g, `Updated ${today}`)
    .replace(/\d{4}\/\d{2}\/\d{2} 업데이트/g, `${today} 업데이트`)
    .replace(/Actualizado \d{4}\/\d{2}\/\d{2}/g, `Actualizado ${today}`);
  if (html === before) {
    console.log('Banner date unchanged.');
    return;
  }
  await fs.writeFile(htmlPath, html);
  console.log(`✔ Bumped banner date to ${today}`);
}

async function main() {
  console.log('╔══════════════════════════════════╗');
  console.log('║   K-Star Hub · Daily updater     ║');
  console.log('╚══════════════════════════════════╝\n');
  await updateNewsJson();
  await bumpBannerDate();
  console.log('\nDone.');
}

main().catch(e => {
  console.error('Fatal:', e);
  process.exit(1);
});
