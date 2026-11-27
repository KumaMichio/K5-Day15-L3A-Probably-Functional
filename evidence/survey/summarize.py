"""Đếm kết quả Google Form khảo sát pre-class (tạo bằng create_form.gs) — phụ trách: Dương Thị Huệ.

Cách dùng:
    1. Google Form → Câu trả lời → Tải xuống CSV (hoặc Xem trong Trang tính → Tải xuống → CSV).
    2. Lưu file tải về thành evidence/survey/raw-responses.csv  (tên raw-* đã nằm trong .gitignore, KHÔNG commit).
    3. python evidence/survey/summarize.py evidence/survey/raw-responses.csv --clean evidence/survey/results.csv

In ra x/n cho từng lựa chọn, chỉ đếm người đúng vai (học viên L3A / L3B).
--clean ghi bản đã ẩn danh: bỏ cột dấu thời gian chính xác (giữ ngày) và cột liên hệ.
Chỉ dùng thư viện chuẩn.
"""
import argparse
import csv
import sys
from collections import Counter

# Tiền tố tiêu đề câu hỏi — khớp create_form.gs. Đổi tiêu đề trong form thì sửa ở đây.
ROLE = "Bạn là"
TARGET_ROLES = {"Học viên L3A", "Học viên L3B"}
CONTACT = "Nếu có: cách liên hệ"
TIMESTAMP = ("Dấu thời gian", "Timestamp")

# Câu chọn nhiều: liệt kê đủ lựa chọn, vì Google nối các lựa chọn bằng ", " mà vài lựa chọn có dấu phẩy.
CHECKBOX = {
    "Lần gần nhất gặp chỗ chưa hiểu trong video, bạn đã làm gì?": [
        "Tua lại video", "Hỏi trợ giảng AI ngay dưới video", "Hỏi bạn học / nhóm", "Hỏi trên Discord",
        "Hỏi ChatGPT / AI khác bên ngoài", "Tự tìm trên Google / tài liệu", "Bỏ qua, xem tiếp",
    ],
    "Nếu bạn từng hỏi trợ giảng AI dưới video": [
        "Chưa từng hỏi trợ giảng", "Hiểu luôn, xem tiếp", "Hỏi lại / hỏi tiếp trợ giảng",
        "Tua lại video để kiểm", "Hỏi chỗ khác để kiểm", "Không chắc đúng nhưng vẫn xem tiếp",
    ],
}
# Câu trả lời tự do: in nguyên văn để chọn trích dẫn cho evidence/summary.md.
FREE_TEXT = ("Bạn kiểm câu trả lời", "Điều gì khó chịu nhất", "Trong 1 tuần qua")


def find_col(headers, prefix):
    for h in headers:
        if h.strip().startswith(prefix):
            return h
    return None


def split_checkbox(cell, options):
    """Tách ô chọn nhiều theo danh sách lựa chọn đã biết; phần còn lại là 'Mục khác'."""
    picked, rest = [], cell
    for opt in sorted(options, key=len, reverse=True):
        if opt in rest:
            picked.append(opt)
            rest = rest.replace(opt, "")
    rest = rest.strip(" ,")
    if rest:
        picked.append("Khác: " + rest)
    return picked


def pct(x, n):
    # Dưới 10 người chỉ ghi x/n (evidence/survey/TEMPLATE.md)
    return f"{x}/{n}" if n < 10 else f"{x}/{n} ({100 * x / n:.1f}%)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--clean", help="ghi bản đã ẩn danh ra file này (vd evidence/survey/results.csv)")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # PowerShell / cmd mặc định cp1252 làm vỡ tiếng Việt

    with open(args.csv_path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("File không có câu trả lời nào.")
    headers = list(rows[0].keys())

    role_col = find_col(headers, ROLE)
    contact_col = find_col(headers, CONTACT)
    ts_col = next((c for p in TIMESTAMP if (c := find_col(headers, p))), None)

    roles = Counter(r[role_col] for r in rows) if role_col else Counter()
    target = [r for r in rows if not role_col or r[role_col] in TARGET_ROLES]
    n = len(target)

    print(f"Tổng câu trả lời: {len(rows)} · đúng vai (học viên L3A/L3B): {n}")
    for k, v in roles.most_common():
        print(f"  - {k}: {v}")
    if n < 20:
        print(f"  ⚠️ Chưa đủ ngưỡng khảo sát (≥20 người đúng vai), còn thiếu {20 - n}.")
    print()

    skip = {role_col, contact_col, ts_col}
    for col in headers:
        if col in skip:
            continue
        print(f"## {col}")
        answers = [r[col].strip() for r in target if r[col].strip()]
        cb = next((opts for p, opts in CHECKBOX.items() if col.startswith(p)), None)
        if col.startswith(FREE_TEXT):
            for a in answers:
                print(f'  - "{a}"')
        elif cb is not None:
            cnt = Counter(o for a in answers for o in split_checkbox(a, cb))
            for opt, x in cnt.most_common():
                print(f"  - {opt}: {pct(x, n)}")
        else:
            for opt, x in Counter(answers).most_common():
                print(f"  - {opt}: {pct(x, n)}")
        print(f"  (bỏ trống: {n - len(answers)})\n")

    if args.clean:
        out_cols = [h for h in headers if h != contact_col]
        with open(args.clean, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=out_cols, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                r = dict(r)
                if ts_col and r.get(ts_col):
                    r[ts_col] = r[ts_col].split(" ")[0]  # chỉ giữ ngày
                w.writerow(r)
        print(f"Đã ghi bản ẩn danh: {args.clean} (đã bỏ cột liên hệ, giờ gửi chỉ còn ngày).")
        print("Kiểm bằng mắt các câu tự do trước khi commit: ai đó có thể tự ghi tên trong câu trả lời.")


if __name__ == "__main__":
    main()
