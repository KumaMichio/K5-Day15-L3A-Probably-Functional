# Tóm tắt mô phỏng simulate-1@20261128-102706

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| hoi_it | 13 | 1 | 595 | 133 | 0.5 | 1.1 |
| hoi_vua | 14 | 2 | 1655 | 514 | 1.2 | 3.5 |
| hoi_nhieu | 19 | 4 | 3384 | 1073 | 2.5 | 5.5 |
| hoi_don | 4 | 5 | 4740 | 1293 | 3.5 | 7.2 |

Tỉ lệ đạt dùng để tính: 30/30 (100%) — lượt run-2@20261128-080301

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (143 người) | Chi phí / tháng — cơ sở (218 người) | Chi phí / tháng — cao (436 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| claude-haiku-5-5 (vào 0.1 · ra 0.5 $/1M) | $0.00057 | $0.00057 | $0.00021 | $0.3342 | $0.5094 | $1.02 | $0.0023 |
| claude-sonnet-5-5 (vào 2.0 · ra 10.0 $/1M) | $0.0115 | $0.0115 | $0.0042 | $6.68 | $10.19 | $20.38 | $0.0467 |
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0016 | $0.0016 | $0.00059 | $0.9346 | $1.42 | $2.85 | $0.0065 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.7) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: anthropic/claude-haiku-5.5. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
