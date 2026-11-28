// Khung mở đầu / kết thúc, vẽ ngay trong trang demo để dùng đúng font + màu của trang.
// Chạy: node cards.mjs <url> <outDir> "<tên model>"
import { chromium } from 'playwright-core';

const [URL, OUT, MODEL] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
await p.goto(URL); await p.waitForTimeout(1200);

const card = (html) => p.evaluate(html => {
  document.body.innerHTML = `<style>
    .vc{position:fixed;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 160px;background:var(--bg);color:var(--ink);font-family:var(--font-body, inherit)}
    .vc .eb{font-size:22px;color:var(--muted);letter-spacing:.02em;margin-bottom:28px}
    .vc h1{font-size:88px;line-height:1.05;margin:0 0 36px;font-family:var(--font-display, inherit)}
    .vc p{font-size:30px;line-height:1.45;margin:0 0 14px;color:var(--ink);max-width:1200px}
    .vc .m{color:var(--muted)} .vc code{font-family:'JetBrains Mono',monospace;font-size:26px;background:var(--surface);padding:3px 10px;border-radius:8px}
    .vc .k{display:inline-block;min-width:200px;font-weight:600;color:var(--accent, var(--ink))}
  </style><div class="vc">${html}</div>`;
}, html);

await card(`<div class="eb">Probably-Functional · AI20K K5 · Track A</div>
  <h1>Trợ giảng có căn cứ</h1>
  <p>Demo e2e: trình duyệt thật → <code>web/server.py</code> → <code>answer()</code> → model thật</p>
  <p class="m">Model: <code>${MODEL}</code> qua OpenRouter</p>`);
await p.waitForTimeout(400); await p.screenshot({ path: `${OUT}/intro.png` });

await card(`<div class="eb">Vừa xem</div>
  <p><span class="k">Câu thường</span>AI trả lời kèm mã đoạn, bấm mã mở đúng đoạn bài.</p>
  <p><span class="k">Câu khó</span>Chèn lệnh đòi lộ hướng dẫn: AI chọn từ chối.</p>
  <p class="m" style="margin-top:34px">Quay trực tiếp, không cắt ghép câu trả lời · Chạy lại: <code>python web/server.py</code></p>`);
await p.waitForTimeout(400); await p.screenshot({ path: `${OUT}/outro.png` });
await b.close();
