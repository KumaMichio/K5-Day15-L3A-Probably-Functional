"""Đếm số tổng hợp từ data/preclass/ (data BTC cấp, KHÔNG commit nguyên file).

Chạy:  python evidence/scripts/count_preclass.py [đường-dẫn-tới-preclass] [--examples]
       mặc định: data-btc/preclass  (thư mục data-btc/ đã có trong .gitignore)

Chỉ in số đã tổng hợp. --examples in thêm vài mã lượt chat (C…) làm ví dụ, không in mã học viên.
Định nghĩa từng con số: evidence/data-mining.md mục 1.
"""
import csv
import json
import sys
import collections as C
from datetime import datetime, timedelta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # Windows console

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
D = ARGS[0] if ARGS else "data-btc/preclass"
SHOW_EXAMPLES = "--examples" in sys.argv

ACTIVE = 436                 # học viên có hoạt động (README data/preclass)
REASK_WINDOW = 180           # giây: hỏi lại cùng video trong 3 phút sau câu trả lời
REWIND_WINDOW = 120          # giây: tua lùi cùng video trong 2 phút sau câu trả lời
REWIND_MIN = 5               # giây: tua lùi ít nhất 5 giây mới tính
SHORT_Q = 10                 # ký tự: câu hỏi <= 10 ký tự coi là quá ngắn


def rows(name):
    with open(f"{D}/{name}", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def ts(s):
    return datetime.fromisoformat(s)


def pct(x, n):
    return f"{x}/{n} ({x / n:.1%})" if n else f"{x}/0"


chat = rows("chat.csv")
events = rows("events.csv")
data = {e["ref_id"]: json.loads(e["data"] or "{}") for e in events if e["type"] == "agent_replied"}
reply_at = {e["ref_id"]: ts(e["occurred_at"]) for e in events if e["type"] == "agent_replied"}

# ---- 0. Độ phủ
users = C.Counter(r["hv"] for r in chat)
days = sorted({r["asked_at"][:10] for r in chat})
print(f"Khoảng thời gian chat: {days[0]} → {days[-1]} ({len(days)} ngày có chat)")
print(f"[A] Học viên đã nhắn AI: {pct(len(users), ACTIVE)}  · tổng lượt nhắn: {len(chat)}")

# Tập chính: câu hỏi dưới video gửi trợ giảng AI
TA = [r for r in chat if r["channel"] == "video_question" and r["addressed_agent_id"] == "teaching_assistant"]
print(f"[B] Câu hỏi dưới video gửi trợ giảng: {pct(len(TA), len(chat))}")

# ---- 1. Thiếu ngữ cảnh
mc = [r for r in TA if data.get(r["id"], {}).get("missing_context") is not None]
mc_true = [r for r in mc if data[r["id"]]["missing_context"] is True]
print(f"[C] Trả lời bị cờ missing_context = true: {pct(len(mc_true), len(mc))}")
mc_answered = [r for r in mc_true if int(r["do_dai_tra_loi"] or 0) >= 100]
print(f"    trong đó vẫn trả lời dài >= 100 ký tự: {pct(len(mc_answered), len(mc_true))}")

# ---- 2. Không dẫn mốc trong bài (chỉ có từ 13/11)
cit = [r for r in TA if "moc_trich_dan" in data.get(r["id"], {})]
no_cit = [r for r in cit if not data[r["id"]]["moc_trich_dan"]]
print(f"[D] Trả lời không dẫn mốc nào trong bài (từ 13/11): {pct(len(no_cit), len(cit))}")

# ---- 3. Hỏi lại cùng video trong 3 phút sau câu trả lời
by_user = C.defaultdict(list)
for r in chat:
    by_user[r["hv"]].append(r)
for v in by_user.values():
    v.sort(key=lambda r: r["asked_at"])
reask = []
for r in TA:
    if r["id"] not in reply_at:
        continue
    t0 = reply_at[r["id"]]
    for o in by_user[r["hv"]]:
        t = ts(o["asked_at"])
        if o["id"] != r["id"] and o["transcript"] == r["transcript"] and t0 < t <= t0 + timedelta(seconds=REASK_WINDOW):
            reask.append(r)
            break
ta_with_reply = [r for r in TA if r["id"] in reply_at]
print(f"[E] Hỏi tiếp cùng video trong {REASK_WINDOW // 60} phút sau câu trả lời: {pct(len(reask), len(ta_with_reply))}")

# ---- 4. Tua lùi cùng video trong 2 phút sau câu trả lời
seeks = C.defaultdict(list)
for e in events:
    if e["type"] == "video_seeked":
        d = json.loads(e["data"] or "{}")
        if d.get("to") is not None and d.get("from") is not None and d["to"] < d["from"] - REWIND_MIN:
            seeks[(e["hv"], e["video"])].append(ts(e["occurred_at"]))
rewind = []
for r in ta_with_reply:
    vid = r["transcript"].split("/")[-1].removesuffix(".txt")
    t0 = reply_at[r["id"]]
    if any(t0 < t <= t0 + timedelta(seconds=REWIND_WINDOW) for t in seeks[(r["hv"], vid)]):
        rewind.append(r)
print(f"[F] Tua lùi >= {REWIND_MIN}s cùng video trong {REWIND_WINDOW // 60} phút sau câu trả lời: {pct(len(rewind), len(ta_with_reply))}")

either = {r["id"] for r in reask} | {r["id"] for r in rewind}
print(f"[G] Hỏi lại HOẶC tua lùi ngay sau câu trả lời: {pct(len(either), len(ta_with_reply))}")

# ---- 5. Câu hỏi quá ngắn
short = [r for r in TA if int(r["do_dai_cau_hoi"] or 0) <= SHORT_Q]
print(f"[H] Câu hỏi <= {SHORT_Q} ký tự: {pct(len(short), len(TA))}")

# ---- 6. Phân bố số lượt / học viên (cho persona chi phí)
ta_users = C.Counter(r["hv"] for r in TA)
b = C.Counter("1" if v == 1 else "2-5" if v <= 5 else "6-15" if v <= 15 else "16+" for v in ta_users.values())
print(f"[I] Số câu hỏi trợ giảng / học viên ({len(ta_users)} người, {len(days)} ngày):",
      {k: b[k] for k in ["1", "2-5", "6-15", "16+"]})
vals = sorted(ta_users.values())
print(f"    trung vị {vals[len(vals) // 2]} câu / người · nhiều nhất {vals[-1]}")

# ---- Ví dụ (mã lượt chat, không có mã học viên)
if SHOW_EXAMPLES:
    print("\nVí dụ:")
    pick = [("missing_context=true, vẫn trả lời dài", mc_answered),
            ("không dẫn mốc", no_cit),
            ("hỏi lại trong 3 phút", reask),
            ("tua lùi trong 2 phút", rewind),
            ("câu hỏi <= 10 ký tự", short)]
    for label, lst in pick:
        for r in lst[:2]:
            dd = data.get(r["id"], {})
            print(f"  {r['id']} · {label} · {r['transcript']} · hỏi {r['do_dai_cau_hoi']} ký tự · "
                  f"trả lời {r['do_dai_tra_loi']} ký tự · missing_context={dd.get('missing_context')} · "
                  f"moc_trich_dan={dd.get('moc_trich_dan', 'chưa ghi')}")
