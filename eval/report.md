# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1 (phần Lượt 1 điền ngay sau `run-1` cho CP3; phần Cải tiến & Lượt 2 bổ sung trước CP4 14:30 Thứ Bảy 28/11). Phụ trách: Nguyễn Bá Thành (issue #33). Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`.

## 1. Kết quả

- **Chuẩn "đạt" đã khoá trước 19:30 T6 (`spec.md` §7):** *"Đạt khi ≥ 80% tổng số câu thử đạt (`pass = 1` theo `pass_criterion`), đồng thời đạt 100% ở nhóm `tu_choi` và 0 câu nào trích dẫn mã đoạn không tồn tại trong `data/lessons/`."*

| Lượt | Run ID | Model | Đạt / tổng | % | `thuong` | `kho` | `tu_choi` | Mã đoạn bịa | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|---|---|
| **1** | `run-1@20261128-010652` | `anthropic/claude-haiku-5.5` | **29/30** | **97%** | 11/11 (100%) | 14/15 (93%) | 4/4 (100%) | 0/30 | **Đạt** (cả 3 điều kiện) |
| **2** | `run-2@20261128-080301` | `anthropic/claude-haiku-5.5` | **30/30** | **100%** | 11/11 (100%) | 15/15 (100%) | 4/4 (100%) | 0/30 | **Đạt** (cả 3 điều kiện) |

- **Thông số vận hành Lượt 1 → Lượt 2 (cùng 30 câu, 0 lỗi kỹ thuật cả hai lượt):**
  - **Lượt 1 (`run-1@20261128-010652`):** trung bình gọi model **0,6 lần/câu** (18/30 câu gọi model, 12/30 câu dừng sớm bằng code ở Bước ①–② tốn 0 token) · gọi công cụ **0,8 lần/câu** · **665 token vào** · **273 token ra**.
  - **Lượt 2 (`run-2@20261128-080301`):** trung bình gọi model **0,6 lần/câu** (vẫn đúng 18/30 câu gọi model) · gọi công cụ **1,3 lần/câu** (tăng do tra thêm từng vế cho câu nhiều vế) · **804 token vào** (+21%) · **251 token ra** (−8%).
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
| **`B03`** (`pass = 1`, thiếu vế 2) | *"Mình hiểu là LLM tra cứu sự thật trong cơ sở dữ liệu có sẵn của nó, còn dùng RAG thì xoá sạch 100% ảo giác luôn đúng không?"* | *"Chưa đúng. Theo bài, LLM không tra cứu sự thật trong cơ sở dữ liệu nào cả… [D01-L1-P01]. Phần về RAG và việc loại bỏ hoàn toàn ảo giác không có trong nội dung bài hiện tại nên mình không thể trả lời."* | Chạy lại `search_lesson` trên commit `bd361ba` (cùng `tools.py` và `data/lessons/` với lượt 1; trace chỉ lưu 300 ký tự đầu của output công cụ): chỉ trả về `D01-L1-P01` (0,556); `D01-L1-P05` (0,169) và `D07-L1-P01` (0,153) đều dưới ngưỡng `0,556 × 1/3 = 0,185` nên bị bỏ, vì câu hỏi dài nhiều từ của vế 1 kéo mẫu số IDF lên cao. Model làm đúng luật (không thấy đoạn RAG nên báo không có), lỗi nằm ở độ phủ bước tra bài với câu ghép dài. |
| **`B09`** (`pass = 1`, lệch nhánh §6) | *"Về temperature thấp và temperature cao khi chọn token, cái đó dùng hợp hơn cái kia đúng không?"* | *"Không có cái nào hợp hơn tuyệt đối, tùy mục đích. Temperature thấp (gần 0) cho câu trả lời ổn định… [D01-L1-P04]. Temperature cao cho câu trả lời đa dạng… [D01-L1-P04]."* | Câu hỏi đã nêu tên *"temperature thấp và temperature cao"* ở đầu câu nên model đủ căn cứ giải thích cả hai chiều thay vì chọn `hoi_lai` như bảng đường đi dự kiến ở `spec.md` §6. Đạt `pass_criterion` vì không đoán bừa 1 chiều và trích đúng `[D01-L1-P04]`. |

## 3. Một lần cải tiến (PR #68 — commit `16c7c9a`)

- **Nhắm vào nhóm lỗi:** Xử lý **câu hỏi hai vế / giao thoa nhiều chủ đề** (nhóm lỗi 1 & 2 ở trên: `B30` và `B03`) — **vì sao đau nhất với người dùng:** học viên L3 xem video buổi tối rất hay đặt câu hỏi so sánh hoặc kiểm tra hai ý cùng lúc (*"A khác B thế nào"*, *"dùng A hay B"*, *"mình hiểu A…, còn B… đúng không?"*); trong khảo sát 13/16 học viên đã hỏi trợ giảng vẫn phải đi kiểm lại chỗ khác. Nếu hệ thống hỏi ngược lửng lơ mà không nhớ hội thoại (`B30`) hoặc báo nhầm phần bài có dạy là *"không có trong bài"* (`B03`), học viên sẽ mất niềm tin ngay và quay sang hỏi ChatGPT bên ngoài.
- **Đã sửa gì (`codebase/agent.py`, PR #68):**
  1. *Tầng tra bài (`_search`):* Sau khi tra cả câu có kết quả (`≥ MIN_SCORE`), nếu câu hỏi tách được ≥ 2 vế (theo dấu phẩy, `;`, `"còn"`, `"hay"`, `"hoặc"`…), gọi thêm `search_lesson(vế, k=1)` cho từng vế; chỉ giữ đoạn mới nếu vế đó và đoạn có chung ít nhất 1 "từ chủ đề" hiếm (`DF ≤ 2`), giới hạn tối đa `MAX_PASSAGES = 4` đoạn. (Khi cả câu đã ra `[]` thì không tra thêm để giữ nguyên đường chặn sớm câu ngoài bài).
  2. *Tầng prompt (`SYSTEM` luật 3 & 4):* Quy định rõ câu hỏi nhiều phần mà tài liệu chỉ phủ một phần → chọn `tra_loi` cho phần có căn cứ (kèm mã đoạn) và nói rõ phần còn lại không có trong bài; chỉ chọn `hoi_lai` khi không biết học viên hỏi khái niệm nào (câu so sánh `"A hay B"` không phải mơ hồ) và cấm hứa *"sẽ trả lời sau"*.
- **Kết quả trên cùng bộ 30 câu thử:**
  - Nhóm câu hai vế mục tiêu (`B03`, `B30`): từ **1/2 đạt (0/2 trọn vẹn cả hai vế)** → **2/2 đạt trọn vẹn cả hai vế**:
    - `B30`: từ `0` (`hoi_lai` lửng lơ) → `1` (giải thích đúng phần RAG kèm `[D07-L1-P01]` và nói rõ bài không đề cập khi nào cần nhiều Agent).
    - `B03`: từ `1` thiếu vế RAG → `1` đủ cả hai vế (`_search` lấy thêm được `[D07-L1-P01]`, model bác bỏ cả hiểu lầm về LLM lẫn hiểu lầm *"RAG xoá sạch 100% ảo giác"*).
  - **Tổng bộ câu thử:** tăng từ **29/30 (97%)** → **30/30 (100%)** (`kho`: `14/15 = 93%` → `15/15 = 100%`; `thuong`: `11/11`; `tu_choi`: `4/4`).
- **Câu nào tệ đi / đánh đổi sau khi sửa:**
  - Không có câu nào tụt điểm từ `1 → 0`, nhưng **`B06` (*"Trong giai đoạn tiền huấn luyện, RLHF và fine-tuning thêm trên dữ liệu riêng, kỹ thuật LoRA là gì?"*) bị kém gọn hơn và lệch đường đi §6**: ở Lượt 1, model nhận diện đích hỏi chính là LoRA nên chọn `khong_co` gọn gàng (kèm gợi ý hỏi TA). Ở Lượt 2, do luật 3 mới ưu tiên giải thích phần có trong đoạn, model giảng lại 2 câu về pre-training / RLHF / fine-tuning `[D01-L1-P06]` (phần học viên chỉ nêu làm bối cảnh) trước khi nói *"Phần về kỹ thuật LoRA không có trong bài học này nên mình không giải thích được"*, đồng thời gọi công cụ tăng `1 → 4` lần và thiếu câu gợi ý hỏi TA của `MSG_NOT_IN_LESSON`.
  - Chi phí token vào trung bình toàn bộ câu thử tăng **+21%** (`665 → 804` token/câu) do `SYSTEM` prompt dài hơn và một số câu đưa thêm đoạn thứ 4 vào ngữ cảnh.

## 4. Còn lại

- **Lỗi / giới hạn chưa sửa và mức độ nguy hiểm:**
  1. *Tìm kiếm thuần từ khoá (`search_lesson` theo IDF từ + cặp âm tiết, không có embedding):* nếu học viên diễn đạt hoàn toàn bằng từ đời thường khác hẳn từ trong bài (vd *"mô hình bịa chuyện nghe rất xuôi"* mà không gõ chữ *"ảo giác"* hay *"hallucination"*), bước ② sẽ trả `[]` và báo nhầm *"không có trong bài"* (false negative — an toàn hơn bịa kiến thức, nhưng làm học viên phải hỏi lại hoặc tua video).
  2. *Không lưu lịch sử hội thoại nhiều lượt:* khi hệ thống thực sự chọn `hoi_lai` (như `B07` `"??"`, `B20` `"ok"`), học viên phải tự gõ lại trọn câu hỏi mới chứ không nối tiếp câu vừa gõ.
  3. *Độ phủ dữ liệu bài học hiện mới dựng 3/13 ngày (`synthetic`, 24 đoạn):* 5/7 câu hỏi thật của học viên (`B24`–`B28` về retry, liveness/readiness, canary, 5 cổng CI) dừng ngay ở Bước ② bằng code nên Lượt 1–2 chưa kiểm được hành vi model trên nội dung các bài vận hành đó; và câu có bối cảnh dẫn nhập dài như `B06` hơi dài dòng hơn sau cải tiến #68.
- **Nếu có thêm 1 tuần:**
  1. **Hybrid search (BM25 + embedding nhỏ) gắn lọc theo đúng `video_id` học viên đang mở:** khắc phục lỗi lệch từ đồng nghĩa mà không kéo nhầm đoạn của ngày học khác, đồng thời bổ sung đủ transcript có gắn mã đoạn + mốc giây (`mm:ss`) thật của cả 13 ngày học để kiểm trọn vẹn các câu như `B24`–`B28`.
  2. **Tách "bối cảnh dẫn nhập" khỏi "ý hỏi chính" trong prompt luật 3:** chỉ trả lời phần có căn cứ khi học viên thực sự hỏi về phần đó (sửa chỗ dài dòng của `B06`), và luôn giữ dòng gợi ý hỏi TA khi còn một vế ngoài bài.
  3. **Thêm 1 lượt nhớ ngữ cảnh ngắn (chỉ giữ đúng 1 câu trước đó khi vừa `hoi_lai`) + nút "Báo câu trả lời chưa khớp đoạn bài"** gửi thẳng mã đoạn và câu hỏi về hàng đợi của TA trước buổi học.
