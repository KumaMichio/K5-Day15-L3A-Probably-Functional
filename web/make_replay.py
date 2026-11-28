"""Đóng gói một lượt chạy thành web/replay.js để trang chạy được khi không có server / mất mạng.

Chạy:  python web/make_replay.py                      (mặc định lượt 2)
       python web/make_replay.py traces/run-1.jsonl eval/run-1.csv

Chỉ đọc trace + CSV đã chạy (không sửa) và 24 đoạn trong data/lessons/. Trace không chứa key (đã kiểm ở PR lượt 1).
"""
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEEP = ("kind", "name", "text", "model", "tokens_in", "tokens_out", "latency_s", "error", "t")


def main():
    args = sys.argv[1:]
    trace_path = os.path.join(ROOT, args[0] if args else "traces/run-2.jsonl")
    csv_path = os.path.join(ROOT, args[1] if len(args) > 1 else "eval/run-2.csv")

    rows = {r["id"]: r for r in csv.DictReader(open(csv_path, encoding="utf-8-sig"))}
    cases, run_id = {}, ""
    for line in open(trace_path, encoding="utf-8"):
        e = json.loads(line)
        run_id = run_id or e.get("run_id", "")
        cid = e.get("case")
        if not cid or e["kind"] in ("bench", "final"):
            continue
        c = cases.setdefault(cid, {"events": [], "searched": False})
        c["searched"] |= e["kind"] == "tool" and e.get("name") == "search_lesson"
        c["events"].append({k: e[k] for k in KEEP if k in e})

    # trace cắt output công cụ ở 300 ký tự và câu nhiều vế tra nhiều lần (#68) → lấy đoạn bằng đúng _search
    # của agent (như web/server.py); chỉ đọc file nên ra đúng các đoạn model đã nhận nếu codebase/ không đổi sau lượt chạy
    sys.path.insert(0, os.path.join(ROOT, "codebase"))
    from agent import _search

    replay = []
    for cid, r in rows.items():
        c = cases.get(cid, {"events": [], "searched": False})
        passages = [{"code": p["code"], "score": p["score"]} for p in _search(r["input"])] if c["searched"] else []
        replay.append({"id": cid, "type": r["type"], "q": r["input"], "output": r["output"],
                       "model": r.get("model", ""), "events": c["events"], "passages": passages})

    lessons = {}
    for name in sorted(os.listdir(os.path.join(ROOT, "data", "lessons"))):
        if name.endswith(".json"):
            data = json.load(open(os.path.join(ROOT, "data", "lessons", name), encoding="utf-8"))
            for p in data["passages"]:
                lessons[p["code"]] = {"code": p["code"], "text": p["text"], "lesson": data["title"]}

    out = os.path.join(ROOT, "web", "replay.js")
    with open(out, "w", encoding="utf-8") as f:
        f.write("// Sinh bởi web/make_replay.py từ %s — không sửa tay.\n" % os.path.basename(trace_path))
        f.write("window.REPLAY = %s;\n" % json.dumps({"run_id": run_id, "cases": replay}, ensure_ascii=False))
        f.write("window.LESSONS = %s;\n" % json.dumps(lessons, ensure_ascii=False))
    assert len(replay) == len(rows), "thiếu câu khi đóng gói"
    print("Đã ghi web/replay.js: %d câu (%s), %d đoạn bài" % (len(replay), run_id, len(lessons)))


if __name__ == "__main__":
    main()
