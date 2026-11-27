# Đào data — cách đếm và kết quả

> Phụ trách: Dương Minh Tân (T05, T19 trong `plan/index.html`). Bản đầu soạn cùng Claude Code, Tân kiểm lại bằng cách chạy script và đối chiếu tay (mục 3).
> Repo chỉ chứa số đã tổng hợp và vài mã lượt chat làm ví dụ — không chép lại nguyên file data.

## 1. Cách đếm — viết TRƯỚC khi chạy

*Khai thật:* phần này viết sau khi đã đọc từ điển cột và xem các trường có từ ngày nào (mục 2), **trước** khi chạy các phép đếm [C]–[H] dưới đây. Mọi ngưỡng (3 phút, 2 phút, 5 giây, 10 ký tự) đặt cứng ở đầu script, không chỉnh sau khi thấy kết quả.

- **Data dùng:** `data/preclass/` BTC cấp (đã ẩn danh) — `chat.csv` (1.260 lượt nhắn AI) và `events.csv` (loại `agent_replied`, `video_seeked`). Chat từ 05/11 đến 25/11/2026 (20 ngày có chat). Bản copy đặt ở `data-btc/preclass/` (đã có trong `.gitignore`).
- **Tập chính:** câu hỏi dưới video gửi trợ giảng AI = dòng `chat.csv` có `channel = video_question` và `addressed_agent_id = teaching_assistant` → **1.090 câu**. Không tính tin nhắn gửi bạn học AI, tin trả lời trong khung thảo luận, câu hỏi trong buổi lớp.
- **Nối câu hỏi với câu trả lời:** `chat.csv.id` = `events.csv.ref_id` của dòng `agent_replied`. Giờ trả lời = `occurred_at` của dòng `agent_replied`.

| Mã | Đếm gì | Mẫu số |
|---|---|---|
| A | Học viên đã nhắn AI ít nhất 1 lần | **436** học viên có hoạt động (không phải 721 tài khoản) |
| B | Câu hỏi dưới video gửi trợ giảng | 1.260 lượt nhắn AI |
| C | Câu trả lời có `missing_context = true` (AI tự báo thiếu ngữ cảnh bài) | câu trong tập chính có giá trị `missing_context` (bỏ ô trống) |
| C2 | …trong đó vẫn trả lời dài ≥ 100 ký tự | số câu ở C |
| D | Câu trả lời có `moc_trich_dan = []` (không dẫn mốc giây nào trong bài) | câu trong tập chính **có ghi** `moc_trich_dan` — trường này chỉ có **từ 13/11** |
| E | Cùng học viên hỏi tiếp **cùng video** trong ≤ 3 phút sau câu trả lời | câu trong tập chính có câu trả lời |
| F | Cùng học viên **tua lùi ≥ 5 giây** cùng video trong ≤ 2 phút sau câu trả lời (`video_seeked`, `to < from − 5`) | như E |
| G | E hoặc F | như E |
| H | Câu hỏi ≤ 10 ký tự (`do_dai_cau_hoi`) | tập chính |
| I | Số câu hỏi trợ giảng / học viên, chia nhóm 1 · 2–5 · 6–15 · ≥16 | học viên có ≥1 câu trong tập chính |
| J | Với mỗi nhóm ở I: số phiên / người / tháng và số câu / phiên (phiên = chuỗi câu của cùng học viên cách nhau ≤ 30 phút; quy tháng × 30/21) | học viên trong nhóm |

- **Script:** [`evidence/scripts/count_preclass.py`](scripts/count_preclass.py). Chạy lại:
  ```
  python evidence/scripts/count_preclass.py data-btc/preclass --examples
  ```

## 2. Đọc trước, đếm sau

Đã đọc 30 dòng đầu `chat.csv`, các dòng `agent_replied` và `video_seeked` đầu tiên của `events.csv`, `column_dictionary.csv`, `event_types.csv`. Các *kiểu* hành vi thấy được:

- Học viên hỏi **dồn nhiều câu liền nhau trên cùng một video**, cách nhau khoảng 1 phút (vd 5 câu trên `Day01/d01-r1-v02` trong 5 phút).
- Trợ giảng **luôn trả lời**, kể cả khi tự gắn cờ thiếu ngữ cảnh: câu trả lời thường dài 150–600 ký tự.
- Từ 13/11 trợ giảng bắt đầu ghi `moc_trich_dan` (mốc giây trong bài, vd `Day06/d06-r1-v01.txt@194`), nhưng nhiều câu để trống.
- Có câu hỏi chỉ 1–2 ký tự (gõ nhầm hoặc "?") mà vẫn nhận câu trả lời hơn 100 ký tự.
- Học viên tua video rất nhiều (4.322 dòng `video_seeked`), phần lớn là tua tới; tua lùi ngay sau khi hỏi ít gặp hơn.
- Các trường `verdict`, `reply_kind`, `prompt_version`, `ngu_canh`, `moc_trich_dan` **chỉ có ở một phần thời gian** → không so sánh trước / sau bằng các trường này.

## 3. Kết quả

| Mã | Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|---|
| A | Học viên có hoạt động đã nhắn AI | 145 / 436 | 33,3% | 2/3 học viên không dùng trợ giảng — vì sao: hỏi trong phỏng vấn |
| B | Câu hỏi dưới video gửi trợ giảng | 1.090 / 1.260 | 86,5% | Kênh chính của trợ giảng |
| C | Trả lời bị cờ thiếu ngữ cảnh | 98 / 1.075 | 9,1% | 15 câu không có cờ, bỏ khỏi mẫu số |
| C2 | …trong đó vẫn trả lời dài ≥ 100 ký tự | 97 / 98 | 99,0% | **Thiếu căn cứ nhưng vẫn trả lời** — đúng chỗ đau của lát cắt |
| D | Trả lời không dẫn mốc nào trong bài (từ 13/11) | 231 / 557 | 41,5% | Học viên không có chỗ để tự kiểm |
| E | Hỏi tiếp cùng video trong 3 phút | 490 / 1.090 | 45,0% | Tín hiệu yếu: có thể là hỏi tiếp tự nhiên, không chắc là không hài lòng |
| F | Tua lùi ≥ 5 giây trong 2 phút | 60 / 1.090 | 5,5% | |
| G | E hoặc F | 530 / 1.090 | 48,6% | Như E: tín hiệu yếu |
| H | Câu hỏi ≤ 10 ký tự | 70 / 1.090 | 6,4% | Nguồn câu thử loại "mơ hồ / thiếu thông tin" |
| I | Câu hỏi / học viên (143 người, 20 ngày) | 1 câu: 38 · 2–5: 46 · 6–15: 43 · ≥16: 16 | — | Trung vị 4, nhiều nhất 72. Dùng cho persona ở `cost/personas.yaml` |
| J | Persona chi phí theo nhóm ở I | 1 câu: 1,4 phiên/tháng × 1,0 câu · 2–5: 2,4 × 2,0 · 6–15: 3,3 × 4,0 · ≥16: 8,8 × 5,1 | — | Ngưỡng 30 phút đặt trước khi chạy (`SESSION_GAP`). Dùng cho `cost/personas.yaml` |

**Quy ra tháng** *(để dùng ở bảng impact)*: 1.090 câu / 21 ngày lịch × 30 ≈ **1.560 câu hỏi trợ giảng / tháng**; trong đó ~9,1% bị cờ thiếu ngữ cảnh ≈ **140 câu / tháng**; ~41,5% không dẫn mốc ≈ **650 câu / tháng** (giả định tỉ lệ từ 13/11 giữ nguyên).

**Đã đối chiếu tay** (Tân làm lại trước CP2):
- `C00581`: câu hỏi kế tiếp `C00499` của cùng học viên, cùng `Day01/d01-r1-v02`, 61 giây sau câu trả lời → đúng định nghĩa E ✓
- `C00983`: `missing_context = true`, trả lời 182 ký tự → đúng C2 ✓
- __ dòng khác: __

**Kết luận đầu:** data **ủng hộ một phần** giả thuyết. Rõ nhất: khi thiếu ngữ cảnh trợ giảng vẫn trả lời (97/98), và 41,5% câu trả lời không chỉ ra mốc nào trong bài. Chưa chứng minh được học viên *khó chịu* vì điều đó — E/F/G chỉ là tín hiệu hành vi, cần phỏng vấn kiểm lại.

> **Lưu ý cho canvas / spec:** số đầu ở canvas dòng 4 và `spec.md` §1–§2 (101/1.245 = 8,1%) đếm trên *mọi* câu trả lời AI. Số ở đây (98/1.075 = 9,1%) chỉ đếm câu hỏi dưới video gửi trợ giảng, khớp đúng lát cắt. Nên cập nhật canvas và spec theo số này.

## 4. ≥5 ví dụ cụ thể (mã lượt chat đã ẩn danh, không đoán ai là ai)

Data không có câu chữ học viên viết, chỉ có độ dài. Trích từ `python evidence/scripts/count_preclass.py --examples`:

1. `C00983` · `Day01/d01-r1-v05` · hỏi 29 ký tự → trợ giảng tự gắn **thiếu ngữ cảnh** nhưng vẫn trả lời 182 ký tự.
2. `C00676` · `Day01/d01-r1-v01` · hỏi 48 ký tự → **thiếu ngữ cảnh**, vẫn trả lời 359 ký tự.
3. `C01187` · `Day06/d06-r1-v01` · hỏi 92 ký tự → trả lời 600 ký tự, **không dẫn mốc nào** trong bài.
4. `C00882` · `Day05/d05-r2-v06` · hỏi 18 ký tự → trả lời 220 ký tự, **không dẫn mốc**.
5. `C00581` · `Day01/d01-r1-v02` · hỏi 82 ký tự, nhận 388 ký tự → **hỏi tiếp cùng video sau 61 giây**.
6. `C00979` · `Day01/d01-r1-v01` · hỏi 29 ký tự, nhận 333 ký tự → **tua lùi video trong 2 phút**.
7. `C01056` · `Day01/d01-r1-v01` · câu hỏi **2 ký tự** → vẫn nhận câu trả lời 171 ký tự (không hỏi lại).

## 5. Giới hạn của data

- Data cho biết học viên **làm gì**, không cho biết **vì sao**. Không có câu chữ câu hỏi / câu trả lời, nên không kiểm được câu trả lời đúng hay sai, có bám bài hay không.
- `missing_context` là cờ **AI tự gắn**, không phải người kiểm. Có thể thiếu (AI thiếu ngữ cảnh mà không biết) hoặc thừa.
- `moc_trich_dan` chỉ có từ 13/11 (557/1.090 câu); D không đại diện cho 05–12/11.
- E (hỏi tiếp trong 3 phút) không phân biệt "hỏi tiếp vì tò mò" với "hỏi lại vì câu trả lời không dùng được". F dùng `occurred_at` theo đồng hồ máy học viên, có thể lệch vài giây so với giờ trả lời.
- 145 người đã hỏi là nhóm **chủ động**; 291 người chưa từng hỏi không có trong E–I.
- Dữ liệu 3 tuần đầu khoá; số câu hỏi giảm mạnh sau 17/11, nên quy ra tháng có thể cao hơn thực tế.

→ **Kiểm lại bằng phỏng vấn** (T08, T25 — Huệ điều phối), mỗi người hỏi:
- "Lần gần nhất bạn hỏi trợ giảng dưới video là khi nào? Bạn làm gì ngay sau khi đọc câu trả lời?" → kiểm E/F có phải là không hài lòng.
- "Bạn kiểm câu trả lời đúng hay sai bằng cách nào?" → kiểm D (không có mốc thì có khó tự kiểm không).
- Với người chưa từng hỏi: "Gặp chỗ không hiểu trong video thì bạn làm gì?" → giải thích A (2/3 không dùng).
