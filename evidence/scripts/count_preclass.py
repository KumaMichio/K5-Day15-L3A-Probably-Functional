"""Đếm số tổng hợp từ data/preclass/ (data BTC cấp, KHÔNG commit nguyên file).

Chạy:  python evidence/scripts/count_preclass.py <đường-dẫn-tới-data/preclass>
       vd: python evidence/scripts/count_preclass.py data-btc/preclass

Chỉ in số đã tổng hợp, không in mã học viên.
Cách đếm (ghi trước khi chạy):
  - Mẫu số học viên: 436 người có hoạt động (README data/preclass), không phải 721 tài khoản.
  - Lượt hỏi AI: mỗi dòng chat.csv là một lượt học viên nhắn AI.
  - Thiếu ngữ cảnh: events.csv type = agent_replied, khoá data.missing_context;
    mẫu số = các lượt có giá trị true/false (bỏ dòng trống).
"""
import csv, json, sys, collections as C

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # Windows console

d = sys.argv[1] if len(sys.argv) > 1 else "data-btc/preclass"
ACTIVE = 436

def rows(name):
    return list(csv.DictReader(open(f"{d}/{name}", encoding="utf-8-sig")))

ch = rows("chat.csv")
per = C.Counter(r["hv"] for r in ch)
print(f"Học viên đã nhắn AI: {len(per)}/{ACTIVE} ({len(per)/ACTIVE:.1%})")
print(f"Tổng lượt nhắn: {len(ch)}")
print("Theo kênh:", dict(C.Counter(r["channel"] for r in ch)))
print("Theo AI được nhắn:", dict(C.Counter(r["addressed_agent_id"] for r in ch)))
b = C.Counter("1" if v == 1 else "2-5" if v <= 5 else "6-15" if v <= 15 else "16+" for v in per.values())
print("Số lượt / học viên (đã nhắn):", {k: b[k] for k in ["1", "2-5", "6-15", "16+"]})
ql = sorted(int(r["do_dai_cau_hoi"] or 0) for r in ch)
print(f"Độ dài câu hỏi: trung vị {ql[len(ql)//2]} ký tự; <=10 ký tự: {sum(q <= 10 for q in ql)}/{len(ql)}")

rep = [e for e in rows("events.csv") if e["type"] == "agent_replied"]
mc = C.Counter(json.loads(e["data"] or "{}").get("missing_context") for e in rep)
den = mc[True] + mc[False]
print(f"Lượt trả lời bị cờ missing_context=true: {mc[True]}/{den} ({mc[True]/den:.1%}); trống: {mc[None]}")
