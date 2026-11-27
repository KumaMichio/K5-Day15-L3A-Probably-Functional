# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 4 kiểu theo số câu hỏi trợ giảng / học viên trong data pre-class — hỏi ít 26,6% (1,4 phiên/tháng × 1 câu) · hỏi vừa 32,2% (2,4 × 2) · hỏi nhiều 30,1% (3,3 × 4) · hỏi dồn 11,2% (8,8 × 5). Nguồn: `evidence/scripts/count_preclass.py` [I], [J], cách đếm ở `evidence/data-mining.md`.
- **Số người dùng thật** 3 kịch bản: thấp 143 · cơ sở 218 · cao 436. Nguồn: thấp = số học viên đã hỏi trợ giảng dưới video (data); cơ sở = 50% của 436 học viên có hoạt động *(tự ước tính)*; cao = cả 436 học viên có hoạt động (README `data/preclass`).
- **Giá** 3 model, từ `further-reading/model-prices.md` của repo đề (BTC tra 25/11/2026): Claude Haiku 5.5 (Nhỏ) 0,10 / 0,50 · Claude Sonnet 5.5 (Lớn) 2,00 / 10,00 · gemini-3.1-flash-lite (Nhỏ) 0,25 / 1,50 USD / 1M token vào / ra.
- **Tỉ lệ đạt** dùng để tính: __/__ (__%) — lượt `run-2` *(chờ #32; chạy `python run.py simulate --rate-from eval/run-2.csv`)*
- Đo token trên model __ *(model Hùng nối ở #11)*, tính giá Claude Haiku 5.5 và Claude Sonnet 5.5 (+ gemini-3.1-flash-lite)

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-__.csv` · run ID __ · __ phiên · seed __

*(dán bảng từ `cost/simulate-N-summary.md`)*

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): __
- Chi phí / người / tháng (cơ sở, model __): __
- **Kết luận một dòng — đáng làm không:** __

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm
