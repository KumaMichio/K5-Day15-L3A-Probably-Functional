# Data card — dữ liệu bản chạy thử dùng

> Bản đầu CP2 (27/11/2026), đủ ở CP3. Phụ trách: Dương Minh Tân (issue #12). Chấm ở rubric R4.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ bản viết lại hoặc số đã tổng hợp.

## Dataset 1 · Nhật ký pre-class (data BTC cấp) — chỉ số tổng hợp

| | |
|---|---|
| Dùng để làm gì | Đào bằng chứng pain (`evidence/data-mining.md`) · chọn bài nào để viết lại (Dataset 2) · tỉ lệ cho persona chi phí (`cost/personas.yaml`) |
| Từ đâu | Data BTC cấp `data/preclass/` trong repo đề `VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon`. Bản copy để ở `data-btc/preclass/` (đã có trong `.gitignore`, **không commit**) |
| Xử lý những bước gì | BTC đã ẩn danh (không tên, email, mã gốc; không có câu chữ học viên viết, chỉ có độ dài) · nhóm chỉ đếm, không chép dòng nào · lọc tập chính: `chat.csv` có `channel = video_question` và `addressed_agent_id = teaching_assistant` (script: `evidence/scripts/count_preclass.py`) |
| Số dòng / số đoạn | `chat.csv` 1.260 lượt → tập chính 1.090 câu hỏi dưới video · `events.csv` 107.709 dòng · 436 học viên có hoạt động |
| Phiên bản / ngày lấy | Dữ liệu 05/11 → 25/11/2026 · lấy từ repo đề ngày 27/11/2026 |
| Nhãn | thật (đã ẩn danh) |
| Giới hạn | Không có nội dung câu hỏi / câu trả lời, nên không biết học viên hỏi gì cụ thể · một số trường chỉ có từ một ngày nhất định (`moc_trich_dan` từ 13/11, `learning_mode` từ 25/11) · chỉ 20 ngày, một khoá |

**Số câu hỏi trợ giảng theo ngày học** (tập chính, dùng để chọn bài cho Dataset 2): Day01 333 · Day03 140 · Day04 134 · Day02 113 · Day08 86 · Day05 78 · Day07 77 · Day09 54 · Day06 40 · Day13 17 · Day11 13 · Day10 5.

## Dataset 2 · Bài học có mã đoạn (`data/lessons/`) — `synthetic`

| | |
|---|---|
| Dùng để làm gì | Nguồn cho công cụ `search_lesson` / `get_passage` (`codebase/tools.py`) · căn cứ để trợ giảng trích mã đoạn · đặt căn cứ cho bộ câu thử `eval/benchmark.csv` |
| Từ đâu | **Nhóm tự viết lại** theo chủ đề của 3 bài pre-class, **không phải transcript thật** (data BTC không có transcript, và không chép tài liệu khoá) |
| Xử lý những bước gì | Chọn 3 bài theo số câu hỏi ở Dataset 1: Day01 (nhiều nhất, 333 câu), Day04 (134), Day07 (77, chủ đề RAG gần nhất với lát cắt) · viết mỗi bài 8 đoạn ngắn, mỗi đoạn một ý, 2–4 câu · gán mã `D<ngày>-L<bài>-P<đoạn>` |
| Số dòng / số đoạn | 3 bài · 24 đoạn: `d01-llm-foundation.json` (D01-L1-P01…P08) · `d04-prompt-tool-calling.json` (D04-L1-P01…P08) · `d07-retrieval-context.json` (D07-L1-P01…P08) |
| Phiên bản / ngày lấy | v1 · 27/11/2026 |
| Nhãn | `synthetic` |
| Giới hạn | Ngắn hơn nhiều so với bài thật (một bài thật có nhiều video) · nội dung là kiến thức chung về chủ đề, có thể khác cách giảng viên giảng · chỉ 3/13 ngày, câu hỏi về ngày khác sẽ ra "không có trong bài" · **cố ý không có** một số chủ đề gần (vd LoRA, transformer / attention, hạn nộp, lịch học) để thử đường "không có trong bài" |

**Cách sinh:** Claude Code soạn nháp theo yêu cầu "viết lại ngắn 3 bài, mỗi đoạn một ý, đúng hợp đồng `{lesson_id, title, video, passages: [{code, text}]}`"; không dùng seed (viết tay, không sinh ngẫu nhiên). **Người kiểm:** Dương Minh Tân — số đoạn đã đọc lại bằng tay: __ / 24 *(Tân điền sau khi đọc)*.

**Hợp đồng chung với `codebase/`:**
```
data/lessons/<bai>.json = {"lesson_id", "title", "video", "passages": [{"code", "text"}]}
search_lesson(query, k=3) -> [{"code", "text", "score"}]   # [] nếu đoạn tốt nhất có score < MIN_SCORE (0.3); đoạn sau giữ nếu score >= 1/3 đoạn đầu
get_passage(code)         -> {"code", "text"} | None
```
`score` = tỉ lệ trọng số idf các từ (và cặp âm tiết) của câu hỏi có trong đoạn. Tìm theo từ khoá, không dùng embedding: đủ cho 24 đoạn, chỉ dùng thư viện chuẩn. Tự kiểm: `python codebase/tools.py`.

**Độ phủ với bộ câu thử** (24 câu, PR #57, 27/11): mọi mã đoạn trong cột `expected` đều có trong `data/lessons/`; `search_lesson` tìm đủ đoạn cho 23/24 câu. Còn sót: B03 (câu hai ý, đoạn D07-L1-P01 chỉ đạt 0,094). 5 câu ra `[]` đúng ý đồ (B05, B07, B08, B20, B21: ngoài bài hoặc quá ngắn).

Data `synthetic` **không phải bằng chứng pain**: chỉ dùng làm nguồn cho bản chạy thử.
