# AI SPEC — Trợ giảng dưới video có căn cứ trong bài · Nhóm Probably-Functional · Phòng __ · Zone __

> Mốc nộp: §7 chốt chuẩn "đạt" tại **CP2 19:30 Thứ Sáu 27/11** · §0–§7 nộp **CP3 10:00 Thứ Bảy 28/11** · đủ §0–§10 **CP4 14:30 Thứ Bảy 28/11** · §10 changelog ghi tiếp đến **23:59 Thứ Bảy 28/11**.
> Bản CP1: §0–§2 là bản nháp đầu, cập nhật đến CP3 khi có thêm bằng chứng.

Track: [x] A · [ ] B · [ ] C · [ ] D · [ ] E — bài toán: hướng A1 (tutor cho trang pre-class), tối ưu một điểm trợ giảng dưới video đang làm chưa tốt: trả lời kèm căn cứ trong bài, hoặc nói "không có trong bài"
Data BTC cấp đã dùng (nếu có — không commit nguyên file): `data/preclass/` (`chat.csv`, `events.csv`) — chỉ số tổng hợp, đếm bằng `evidence/scripts/count_preclass.py`

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*
- Luồng hiện tại (theo mô tả track A + cột dữ liệu trong `data/preclass/`; ảnh chụp tài khoản: chưa chụp, bổ sung trước CP3):
  1. Học viên mở bài trên trang pre-class (preclass-online.com), xem video.
  2. Gặp chỗ không hiểu → gõ câu hỏi dưới video (`chat.csv` kênh `video_question`) hoặc bôi đen chữ trên slide để hỏi (`slide_text_asked`).
  3. Trợ giảng AI trả lời, dựa vào đoạn lời giảng quanh lúc hỏi (`ngu_canh = hep`) hoặc lời giảng cả ngày (`ca_ngay`); có thể dẫn mốc giây trong video (`moc_trich_dan`).
  4. Học viên đọc câu trả lời rồi xem tiếp, hỏi lại, tua lại video, hoặc hỏi nơi khác (Discord, bạn, ChatGPT riêng) — phần này **chưa kiểm**, sẽ hỏi trong phỏng vấn.
- Công cụ / AI đang được dùng: trợ giảng AI và các bạn học AI trên trang pre-class (nguồn: `tracks/track-a-edtech.md`, `data/preclass/README.md`). Model ghi chung `model_chinh` / `fallback`; prompt và cách tra bài cụ thể: chưa kiểm.

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*
- Người dùng chính (một vai cụ thể): học viên L3 đi làm, tối mới xem video pre-class, gặp chỗ không hiểu ngay khi đang xem.
- Việc họ cố làm xong (`động từ + đối tượng + bối cảnh`, không có chữ AI): hiểu đúng một ý trong video bài giảng trước buổi học, ngay lúc đang xem buổi tối.
- Hôm nay họ giải bằng gì, hỏng ở đâu, vì sao chưa bỏ: hỏi trợ giảng ngay dưới video (nhanh, ngay tại chỗ — lý do chưa bỏ); hỏng khi câu trả lời không chỉ ra đoạn nào trong bài để tự kiểm, hoặc trả lời khi bài không có thông tin (*giả thuyết, kiểm bằng phỏng vấn*). Cách khác: tua lại video, hỏi bạn / Discord, ChatGPT riêng (*chưa kiểm*).
- Pain (KHÔNG chữ AI): học viên L3 xem video pre-class buổi tối — muốn hiểu một ý trong bài — câu trả lời nhận được không chỉ ra đoạn nào để tự kiểm, có lúc bài không có thông tin mà vẫn được trả lời — phải tua lại video, hỏi chỗ khác, hoặc vào lớp với hiểu sai.
- Bằng chứng — số chính + kết luận (chi tiết: `evidence/summary.md`, đang làm). Data 05/11–25/11/2026, đếm bằng `evidence/scripts/count_preclass.py` (cách đếm: `evidence/data-mining.md`):
  - 145/436 học viên có hoạt động (33,3%) đã nhắn AI; 1.090/1.260 lượt nhắn (86,5%) là câu hỏi dưới video gửi trợ giảng.
  - 98/1.075 câu trả lời (9,1%) bị trợ giảng tự gắn cờ thiếu ngữ cảnh — **97/98 vẫn trả lời dài ≥100 ký tự**.
  - 231/557 câu trả lời từ 13/11 (41,5%) không dẫn mốc nào trong bài → học viên không có chỗ để tự kiểm.
  - 530/1.090 (48,6%) hỏi tiếp cùng video trong 3 phút hoặc tua lùi trong 2 phút — tín hiệu yếu, chưa biết là không hài lòng.
  - Phỏng vấn: __/__ học viên L3 ngoài nhóm gặp chỗ đau *(điền sau P1–P4, `evidence/interviews/`, câu hỏi: `evidence/interviews/questions.md`)*.
  - Kết luận tạm: data **ủng hộ một phần** — trợ giảng trả lời cả khi thiếu căn cứ và thường không chỉ ra đoạn nào; còn phải phỏng vấn để biết học viên có thật sự bị hại (tốn thời gian, hiểu sai) không.

## §2. Impact & quyết định chọn *(guide 1.3)*

| Hướng | Bao nhiêu người gặp | Bao nhiêu lần / tháng | Mỗi lần tốn gì | Impact / tháng | Làm kịp không | Chọn? |
|---|---|---|---|---|---|---|
| A1 · Trợ giảng dưới video trả lời có căn cứ (mã đoạn) hoặc nói "không có trong bài" | 145 học viên đã hỏi AI (data), trên 436 có hoạt động | ~1.800 lượt hỏi / tháng (1.260 lượt trong 21 ngày × 30/21, data); trong đó ~8% thiếu ngữ cảnh ≈ 145 lượt | ~10 phút tua lại / hỏi chỗ khác mỗi lần câu trả lời không dùng được *(tự ước tính, kiểm bằng phỏng vấn)* + rủi ro học sai | ≈ 145 × 10 phút ≈ 24 giờ học viên / tháng chỉ tính lượt bị cờ *(nháp)* | Kịp: data có sẵn, cả lớp là người dùng, một quyết định AI | **Chọn** |
| A2 · Trợ lý Discord trả lời hạn nộp / lịch từ thông báo chính thức | chưa có số *(tự ước tính: phần lớn lớp)* | dồn quanh hạn nộp *(tự ước tính)* | hỏi lại, chờ TA, nhầm hạn | chưa tính được | Khó: không có data Discord BTC cấp, phải tự quan sát kênh | Không |
| A5 · Soạn thông báo phòng lab cho key coach | ~vài key coach / buổi *(tự ước tính)* | mỗi tối trước buổi lab | thời gian soạn + báo nhầm phòng | chưa tính được | Kịp, nhưng data training-ops là giả lập, không phải bằng chứng pain | Không |

- **Impact / tháng** của hướng chọn = ~145 lượt thiếu ngữ cảnh × ~10 phút = ~24 giờ / tháng — nguồn: số lượt từ `data/preclass/` (`evidence/scripts/count_preclass.py`); 10 phút / lần *(tự ước tính — thay bằng số từ phỏng vấn trước CP3)*. Chưa tính lượt trả lời không bị cờ nhưng vẫn thiếu căn cứ.
- Hướng ĐÃ LOẠI + vì sao (giữ lại, đừng xoá): A2 — không có data đếm được, bằng chứng phải tự thu từ đầu. A5 — data là giả lập nên không làm bằng chứng pain; người dùng (key coach, ban đào tạo) ít và phải hẹn.
- Số lần / tháng của từng kiểu người dùng (dùng cho persona ở §8): trong 145 học viên đã nhắn AI (21 ngày): 38 người 1 lượt · 42 người 2–5 · 42 người 6–15 · 23 người ≥16 — quy đổi / tháng ở CP4.

## §3. Giải pháp tương tự *(guide 2.1)*
> Bản đầu dựa trên tài liệu công khai (xem ngày 27/11/2026). Theo kế hoạch #8, mỗi thành viên tự thử 1 sản phẩm rồi bổ sung "đã thử thấy gì" vào dòng tương ứng.

| Sản phẩm | Một điều đáng học | Một điều đáng né | Mình khác gì | Nguồn (xem 27/11/2026) |
|---|---|---|---|---|
| **Google NotebookLM** — hỏi đáp trên tài liệu người dùng tải lên | Câu trả lời chỉ lấy từ nguồn đã tải, kèm trích dẫn bấm vào mở đúng đoạn; bài không có thì không trả lời | Người dùng phải tự tải tài liệu và tự mở một công cụ riêng, rời khỏi lúc đang xem video | Đặt ngay dưới video pre-class, nguồn là bài giảng của khoá (không phải tài liệu tự tải), mã đoạn ổn định để học viên mở lại | [NotebookLM Help — FAQ](https://support.google.com/notebooklm/answer/16269187), [Use chat in NotebookLM](https://support.google.com/notebooklm/answer/16179559) |
| **Coursera Coach** — trợ lý AI trong khoá học Coursera | Hỏi ngay trong lúc học, tóm tắt bài và chỉ ra đoạn video nên xem lại | Theo một bài review bên thứ ba, chỉ có ở một số khoá và không trả lời ngoài tài liệu khoá — nhưng không rõ nó báo cho người học thế nào khi bài không có | Nói rõ "không có trong bài" + gợi ý hỏi TA, và code kiểm mọi mã đoạn được dẫn có thật | [Coursera blog — 2023](https://blog.coursera.org/new-products-tools-and-features-2023), [Coursera Coach](https://www.coursera.org/explore/coach), [BuildFastWithAI review](https://buildfastwithai.com/ai-tools/coursera-coach) |
| **Khanmigo** (Khan Academy) — gia sư AI không đưa đáp án | Không làm hộ bài: hỏi gợi mở, cho bước tiếp theo thay vì đáp án | Học viên ít dùng khi tutor từ chối trả lời và chỉ hỏi lại; Khan Academy đã chuyển Khanmigo vào ngay luồng làm bài | Trả lời thẳng câu hỏi hiểu bài (có căn cứ), chỉ từ chối khi bị đòi làm hộ bài / lộ đáp án quiz | [Hechinger Report](https://hechingerreport.org/proof-points-khanmigo-math-ai-tutor/), [KQED MindShift](https://www.kqed.org/mindshift/66662/students-didnt-get-answers-from-khanmigo-they-didnt-want-its-questions-either) |
| **Trợ giảng hiện tại trên trang pre-class** (đối chiếu) | Ngay dưới video, có ngữ cảnh lời giảng quanh lúc hỏi; từ 13/11 có ghi mốc giây | Vẫn trả lời khi tự gắn cờ thiếu ngữ cảnh (97/98); 41,5% câu không dẫn mốc nào | Chính là điểm nhóm tối ưu: không có đoạn thì không trả lời, có đoạn thì bắt buộc kèm mã | `evidence/data-mining.md` |
| Thử thêm (mỗi người 1 sản phẩm): ChatGPT riêng · Perplexity · … | | | | |

## §4. Thiết kế *(guide 2.2, 3.2)*
- **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả):
- Không làm (≥3 điều):
- **Sơ đồ** (ảnh / Mermaid / draw.io): [chèn ở đây]
- **Hình dạng:** [ ] workflow cố định · [ ] một agent · [ ] nhiều agent — 2 dòng lý do, và vì sao **không** chọn hình dạng phức tạp hơn:
- **AI dựa vào đâu** — mỗi công cụ (khớp `codebase/tools.py`):

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  |  |  |  |  |

- **Mức tự động:** [ ] AI gợi ý, người quyết · [ ] AI tự làm khi chắc, chuyển người khi không · [ ] AI tự làm — lý do (sai thì ai chịu gì, sửa đắt hay rẻ):
- **Chỗ chặn rủi ro** (rủi ro lớn nhất của lát cắt bị chặn ở đâu, bằng gì):
- **Chỗ người duyệt** (việc AI không được tự làm):
- **Nguyên tắc thiết kế** (≥3, bắt buộc G10):

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc |  |
  |  |  |
  |  |  |

- Phần nào còn giả (công cụ trả dữ liệu giả, model chế độ giả…) — ghi rõ, không giả làm thật:

## §5. Chỗ khó — 4 lớp + ≥6 kịch bản + 2 tấn công *(guide 2.3)*

| Kịch bản | Lớp (1–4) | Hành vi mong muốn (nói gì, hiện gì, cho làm gì tiếp) | Câu thử |
|---|---|---|---|
|  |  |  |  |
| *(tấn công)* |  |  |  |
| *(tấn công)* |  |  |  |

(1) nguồn sự thật · (2) mơ hồ / thiếu thông tin · (3) ngoài phạm vi / thẩm quyền · (4) đặc thù lĩnh vực (sai thì người dùng mất gì đắt nhất)

## §6. Bốn đường đi của trải nghiệm
- Mọi thứ suôn sẻ: · Không chắc (lớp 2): · Không có căn cứ (lớp 1): · Người dùng sửa:
- Bị đòi ngoài phạm vi (lớp 3): · Trường hợp đặc thù lĩnh vực (lớp 4):

## §7. Đánh giá & chuẩn "đạt" *(guide 2.4, 4.1)*
- Data card: `data/DATA_CARD.md` · bộ câu thử: `eval/benchmark.csv` — __ câu (thuong __ · kho __ · tu_choi __) · metric: `eval/metric_spec.yaml` (__ metric)
- **Chuẩn "đạt"** (chốt **trước 19:30 Thứ Sáu 27/11**, giữ nguyên đến 23:59 Thứ Bảy 28/11): "Đạt khi ≥ __% câu qua, và __"
- Kết quả: lượt 1 __/__ (__%) · lượt 2 __/__ (__%) — run ID: __ / __ → chi tiết `eval/report.md`, hồ sơ `eval/README.md`

## §8. Chi phí khi dùng thật *(guide 4.2)*
- Persona + giá: `cost/personas.yaml` · lượt mô phỏng: `cost/simulate-__.csv` (__ phiên)
- Chi phí / task thành công: __ (model __) · __ (model __)
- Chi phí / tháng ở quy mô thật: thấp __ · cơ sở __ · cao __ → chi tiết `cost/cost-estimate.md`
- So với impact / người / tháng (§2): đáng làm không, vì sao:

## §9. Rủi ro & an toàn
- Dữ liệu: đã ẩn danh gì, không thu gì, không đưa gì vào model gói miễn phí:
- AI **không được** làm gì kể cả khi người dùng yêu cầu:
- Ai có thể bị hại nếu AI sai, và nhóm chặn thế nào:

## §10. Phân công & changelog
- Phân công có tên (theo chặng, chia cặp — guide "Cách chia việc"): Cặp X (build) — Phan Sỹ Hùng, Dương Minh Tân · Cặp Y (bằng chứng + đánh giá) — Dương Thị Huệ, Nguyễn Bá Thành. Chính: Hùng — codebase/ + nối model · Huệ — phỏng vấn + evidence/ · Tân — đào data + impact + cost/ · Thành — eval/ + data card. Mỗi người phỏng vấn ≥1 học viên ngoài nhóm. Đổi cặp ở chặng sau theo guide
- Dùng AI vào việc gì (2–3 dòng; chi tiết `docs/ai-usage.md`): Claude Code dựng repo, viết script đếm data, soạn nháp tài liệu CP1; người phụ trách từng phần kiểm lại trước khi commit.
- Nhật ký thay đổi — **mọi thay đổi sau CP2 19:30 Thứ Sáu 27/11 phải có dòng ở đây**:

**CP2 → CP4** (vd thu hẹp lát cắt, hỏi thêm người dùng, lần cải tiến trước lượt 2)

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
|  |  |  |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
|  |  |  |
