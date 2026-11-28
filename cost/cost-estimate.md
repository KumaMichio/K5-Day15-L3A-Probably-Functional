# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 4 kiểu theo số câu hỏi trợ giảng / học viên trong data pre-class — hỏi ít 26,6% (1,4 phiên/tháng × 1 câu) · hỏi vừa 32,2% (2,4 × 2) · hỏi nhiều 30,1% (3,3 × 4) · hỏi dồn 11,2% (8,8 × 5). Nguồn: `evidence/scripts/count_preclass.py` [I], [J], cách đếm ở `evidence/data-mining.md`.
- **Số người dùng thật** 3 kịch bản: thấp 143 · cơ sở 218 · cao 436. Nguồn: thấp = số học viên đã hỏi trợ giảng dưới video (data); cơ sở = 50% của 436 học viên có hoạt động *(tự ước tính)*; cao = cả 436 học viên có hoạt động (README `data/preclass`).
- **Giá** 3 model, từ `further-reading/model-prices.md` của repo đề (BTC tra 25/11/2026): Claude Haiku 5.5 (Nhỏ) 0,10 / 0,50 · Claude Sonnet 5.5 (Lớn) 2,00 / 10,00 · gemini-3.1-flash-lite (Nhỏ) 0,25 / 1,50 USD / 1M token vào / ra.
- **Tỉ lệ đạt** dùng để tính: **30/30 (100%)**, lượt `run-2@20261128-080301` (`python run.py simulate --rate-from eval/run-2.csv`)
- **Đo token trên model** `anthropic/claude-haiku-5.5` (Claude Haiku 5.5 qua OpenRouter; giá OpenRouter bằng giá Anthropic trong bảng, xem https://openrouter.ai/api/v1/models ngày 28/11/2026). **Tính giá** Claude Haiku 5.5, Claude Sonnet 5.5 và gemini-3.1-flash-lite. Model khác có bộ tách token khác nên số token thật có thể lệch (nhất là gemini).

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-102706` · **50 phiên** · seed 42 · 0 phiên lỗi · trung bình 2,7 câu hỏi / phiên. Bảng chép từ `cost/simulate-1-summary.md`.

**Token đo được theo persona** (chạy thật qua `codebase/agent.py`):

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| hoi_it | 13 | 1 | 595 | 133 | 0.5 | 1.1 |
| hoi_vua | 14 | 2 | 1655 | 514 | 1.2 | 3.5 |
| hoi_nhieu | 19 | 4 | 3384 | 1073 | 2.5 | 5.5 |
| hoi_don | 4 | 5 | 4740 | 1293 | 3.5 | 7.2 |

**Chi phí** (USD):

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (143) | / tháng — cơ sở (218) | / tháng — cao (436) | / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|
| **Claude Haiku 5.5** (model đang dùng) | $0.00057 | **$0.00057** | $0.33 | $0.51 | $1.02 | $0.0023 |
| Claude Sonnet 5.5 | $0.0115 | $0.0115 | $6.68 | $10.19 | $20.38 | $0.0467 |
| gemini-3.1-flash-lite | $0.0016 | $0.0016 | $0.93 | $1.42 | $2.85 | $0.0065 |

- Gọi model trung bình < 1 lần / câu vì câu quá ngắn, xin làm hộ bài và câu ngoài bài dừng bằng code ở bước ①–②, không tốn token.
- Tỉ lệ đạt 100% đo trên 30 câu thử, ngoài thực tế có thể thấp hơn. Nếu tỉ lệ đạt chỉ bằng ngưỡng chuẩn "đạt" 80% (`spec.md` §7), chi phí / task thành công với Haiku 5.5 là $0.00057 ÷ 0,8 ≈ **$0.00071** — vẫn dưới 0,1 cent.

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- **Impact / người / tháng** (`spec.md` §2): ≈ **10 phút học viên / người / tháng** (≈ 140 câu thiếu ngữ cảnh × ~10 phút ≈ 23 giờ / tháng trên 143 người hỏi).
- **Chi phí / người / tháng** (cơ sở 218 người, Claude Haiku 5.5): **$0.0023**. Kể cả dùng Claude Sonnet 5.5 (đắt nhất trong bảng): $0.0467.
- **Kết luận một dòng — đáng làm không:** đáng làm — tiền model cho cả khoá ở kịch bản cao (436 người) chỉ khoảng **$1 / tháng** với Haiku 5.5, để đổi lấy ~10 phút / người / tháng không bị trả lời thiếu căn cứ. Chi phí thật nằm ở **người soạn và duyệt bài có mã đoạn** (`data/lessons/` hiện là bài tự dựng), không nằm ở tiền model *(chưa ước tính giờ công, xem mục 4)*.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm
