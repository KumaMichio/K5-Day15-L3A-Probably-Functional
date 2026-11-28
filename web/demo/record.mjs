// Quay demo e2e: Chrome thật, server thật (web/server.py), model thật. Ghi mốc thời gian từng thao tác → marks.json
// Chạy: node record.mjs [url] [outDir]
import { chromium } from 'playwright-core';
import fs from 'node:fs';

const URL = process.argv[2] || 'http://127.0.0.1:8000/';
const OUT = process.argv[3] || 'out';
const Q1 = 'Hybrid search kết hợp những cách tìm kiếm nào?';
const W = 1600, H = 900;

// video phải là AI thật: server ở chế độ giả thì dừng, không quay
const health = await (await fetch(new globalThis.URL('/api/health', URL))).json();
if (health.provider === 'fake') { console.error('server đang chạy model GIẢ:', health); process.exit(2); }
console.log('model:', health.provider, health.model);
fs.mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch({ executablePath: process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
const ctx = await browser.newContext({ viewport: { width: W, height: H }, recordVideo: { dir: OUT, size: { width: W, height: H } } });
const t0 = Date.now();
const page = await ctx.newPage();
const marks = {};
const mark = k => { marks[k] = (Date.now() - t0) / 1000; console.log(k, marks[k]); };
const bots = () => page.locator('[data-log] .msg--bot').count();
const waitBot = async n => { await page.waitForFunction(n => document.querySelectorAll('[data-log] .msg--bot').length > n, n, { timeout: 90000 }); };

await page.goto(URL);
await page.evaluate(() => document.querySelector('#hoi-thu').scrollIntoView({ block: 'start' }));
await page.waitForFunction(() => document.querySelector('[data-app]')?.dataset.mode === 'live', null, { timeout: 10000 });
await page.waitForTimeout(1500);           // chờ hiệu ứng vào trang xong
mark('start');
await page.waitForTimeout(1200);

// Câu thường: gõ thật, Enter
await page.click('[data-input]');
await page.keyboard.type(Q1, { delay: 45 });
await page.waitForTimeout(300);
let n = await bots();
await page.keyboard.press('Enter');
mark('ask1');
await waitBot(n);
mark('ans1');
await page.waitForTimeout(2600);

// Bấm mã đoạn đầu tiên trong câu trả lời → mở đúng đoạn bài
const code = page.locator('[data-log] .msg--bot').last().locator('button.code').first();
await code.hover(); await page.waitForTimeout(300);
await code.click();
mark('open');
await page.waitForTimeout(3000);

// Câu khó: chèn lệnh đòi in system prompt
const chip = page.locator('[data-samples] [data-sample="chen-lenh"]');
await chip.hover(); await page.waitForTimeout(300);
n = await bots();
await chip.click();
mark('ask2');
await waitBot(n);
mark('ans2');
await page.waitForTimeout(3800);
mark('end');

// ghi lại thông tin màn hình để kiểm: model + token ở panel
marks.meter = await page.locator('[data-meter]').innerText();
marks.step3 = await page.locator('[data-step-id="3"]').innerText();
const video = page.video();
await ctx.close(); await browser.close();
fs.renameSync(await video.path(), `${OUT}/raw.webm`);
fs.writeFileSync(`${OUT}/marks.json`, JSON.stringify(marks, null, 1));
console.log(JSON.stringify(marks));
