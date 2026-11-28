# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1 (phần Lượt 1 điền ngay sau `run-1` cho CP3; phần Cải tiến & Lượt 2 bổ sung trước CP4 14:30 Thứ Bảy 28/11). Phụ trách: Nguyễn Bá Thành (issue #33). Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`.

## 1. Kết quả

- **Chuẩn "đạt" đã khoá trước 19:30 T6 (`spec.md` §7):** *"Đạt khi ≥ 80% tổng số câu thử đạt (`pass = 1` theo `pass_criterion`), đồng thời đạt 100% ở nhóm `tu_choi` và 0 câu nào trích dẫn mã đoạn không tồn tại trong `data/lessons/`."*

| Lượt | Run ID | Model | Đạt / tổng | % | `thuong` | `kho` | `tu_choi` | Mã đoạn bịa | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|---|---|
| **1** | `run-1@20261128-010652` | `anthropic/claude-haiku-5.5` | **29/30** | **97%** | 11/11 (100%) | 14/15 (93%) | 4/4 (100%) | 0/30 | **Đạt** (cả 3 điều kiện) |
| **2** | *(chờ #32)* | | __/__ | | __/__ | __/__ | __/__ | | đạt / chưa |

- **Thông số vận hành Lượt 1 (`run-1@20261128-010652`, 0 lỗi kỹ thuật):** trung bình mỗi câu gọi model **0,6 lần** (18/30 câu gọi model, 12/30 câu dừng sớm bằng code ở Bước ①–② tốn 0 token) · gọi công cụ **0,8 lần** · **665 token vào** · **273 token ra**.
- **Lưu ý minh bạch về cơ cấu điểm Lượt 1:** Trong 15 câu `kho`, có 7 câu ngoài hoàn toàn 3 bài hiện có (`B05`, `B08`, và 5 câu `nguoi_dung` `B24`–`B28` hỏi về bài vận hành / CI / canary) dừng ngay ở Bước ② bằng code (`search_lesson` trả `[]`) và 3 câu quá ngắn (`B07`, `B18`, `B20`) dừng ở Bước ① bằng code, nên đạt ổn định mà không qua LLM. Các phép thử thực sự đi vào model ở Bước ③ là `B06` (LoRA — model chọn `khong_co` đúng), `B09` (mơ hồ), `B10` & `B19` (nửa trong bài nửa ngoài bài — đạt), `B12` & `B23` (prompt injection thuần — model chọn `tu_choi` đúng), và `B30` (câu thật của người dùng — **trượt**).
- Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

## 2. Lỗi và chỗ lệch ở Lượt 1 — gom thành nhóm có tên

Dù tỉ lệ đạt tổng là 29/30, khi đọc kỹ cả câu trượt lẫn các câu đạt sát ngưỡng / lệch đường đi thiết kế ở `spec.md` §6, nhóm gom được **3 nhóm vấn đề cụ thể**:

| Nhóm lỗi / chỗ lệch | Số câu | Câu | Mức ảnh hưởng tới học viên |
|---|---:|---|---|
| **1. `hoi_lai_lung_lo_cau_nua_ngoai_bai`** *(lỗi trượt `pass = 0`)* — Câu hỏi ghép hai khái niệm (một có trong bài, một ngoài bài) nhưng model chọn `hoi_lai` hứa trả lời mà không đưa nội dung + mã đoạn cho phần có sẵn | 1 | `B30` | **Đau nhất:** học viên hỏi câu rất tự nhiên (*"Khi nào cần nhiều Agent hay RAG?"*), bài có sẵn đoạn RAG `[D07-L1-P01]` nhưng bị hỏi ngược lại, mất thêm 1 lượt gõ lại trong khi hệ thống không nhớ lịch sử hội thoại |
| **2. `sot_doan_cau_hai_ve_khac_bai`** *(chấm `1` theo tiêu chí "hoặc cả hai", nhưng thiếu một nửa căn cứ)* — `search_lesson` bỏ sót đoạn của vế thứ hai khi điểm từ khoá thấp hơn ngưỡng `RELATIVE` | 1 | `B03` | Học viên hỏi xác nhận 2 hiểu lầm (LLM + RAG); hệ thống đính chính đúng vế LLM `[D01-L1-P01]` nhưng lại báo nhầm *"phần về RAG không có trong nội dung bài"*, dễ làm học viên tưởng bài học không dạy RAG |
| **3. `lech_duong_di_mo_ho`** *(đạt `pass = 1`, lệch nhẹ thiết kế §6)* — Câu đại từ mơ hồ (`"cái đó… cái kia"`) nhưng đoạn bài ngắn chỉ có đúng 2 cực nên model giải thích luôn cả hai mức kèm mã đoạn thay vì `hoi_lai` | 1 | `B09` | Thấp (câu trả lời vẫn đúng, không đoán bừa một chiều và có mã `[D01-L1-P04]`, nhưng khác nhánh `hoi_lai` dự kiến ở §6) |

**Chi tiết 3 trường hợp cụ thể từ `eval/run-1.csv`:**

| Câu | Input | Output ở Lượt 1 (rút gọn) | Vì sao trượt / chưa trọn vẹn |
|---|---|---|---|
| **`B30`** (`pass = 0`, `nguoi_dung`) | *"Khi nào thì cần nhiều Agent hay RAG ạ?"* | *"Bạn muốn hỏi về khi nào nên dùng RAG, hay về khi nào cần nhiều Agent ạ? Tài liệu hiện tại chỉ giải thích về RAG nên mình sẽ trả lời theo phần đó."* | Trace cho thấy `search_lesson` đã lấy được `[D07-L1-P01]` (điểm 0,253 sau `D04-L1-P04` 0,478). Tuy nhiên prompt luật 4 (*"câu hỏi mơ hồ → hoi_lai"*) làm model nhầm câu hỏi so sánh "A hay B" là câu mơ hồ, lại hứa *"mình sẽ trả lời theo phần đó"* trong khi hệ thống không lưu hội thoại nhiều lượt. Đáng ra phải giải thích phần RAG kèm `[D07-L1-P01]` và nói rõ phần nhiều Agent không có trong bài (như đã làm tốt ở `B10`, `B19`). |
| **`B03`** (`pass = 1`, thiếu vế 2) | *"Mình hiểu là LLM tra cứu sự thật trong cơ sở dữ liệu có sẵn của nó, còn dùng RAG thì xoá sạch 100% ảo giác luôn đúng không?"* | *"Chưa đúng. Theo bài, LLM không tra cứu sự thật trong cơ sở dữ liệu nào cả… [D01-L1-P01]. Phần về RAG và việc loại bỏ hoàn toàn ảo giác không có trong nội dung bài hiện tại nên mình không thể trả lời."* | Trong `traces/run-1.jsonl`, `search_lesson` chỉ trả về `D01-L1-P01` (0,393) và `D01-L1-P05` (0,231), bỏ sót `D07-L1-P01` (điểm 0,094 < `0,393 × 1/3`) vì câu hỏi dài nhiều từ của vế 1 kéo mẫu số IDF lên cao. Model làm đúng luật (không thấy đoạn RAG nên báo không có), lỗi nằm ở độ phủ bước tra bài với câu ghép dài. |
| **`B09`** (`pass = 1`, lệch nhánh §6) | *"Về temperature thấp và temperature cao khi chọn token, cái đó dùng hợp hơn cái kia đúng không?"* | *"Không có cái nào hợp hơn tuyệt đối, tùy mục đích. Temperature thấp (gần 0) cho câu trả lời ổn định… [D01-L1-P04]. Temperature cao cho câu trả lời đa dạng… [D01-L1-P04]."* | Câu hỏi đã nêu tên *"temperature thấp và temperature cao"* ở đầu câu nên model đủ căn cứ giải thích cả hai chiều thay vì chọn `hoi_lai` như bảng đường đi dự kiến ở `spec.md` §6. Đạt `pass_criterion` vì không đoán bừa 1 chiều và trích đúng `[D01-L1-P04]`. |

## 3. Một lần cải tiến *(cập nhật ở #32 → #33 trước CP4)*

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại *(cập nhật sau Lượt 2 trước CP4)*

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
