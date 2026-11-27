# CLAUDE.md — luật cho Claude Code (và mọi coding agent) trong repo này

@AGENTS.md

Repo nộp bài hackathon AI20K K5 · L3A · Track A (hướng A1) của nhóm Probably-Functional. Luật chung của repo (lệnh, cấu trúc code, những gì không được sửa) nằm ở `AGENTS.md`, đã được import ở trên. File này thêm **quy trình git** và **phân quyền file**. Kế hoạch và phân công: `plan/index.html` (15 việc = 15 issue trên GitHub).

## 1. Ai là ai

Đọc `git config user.name` để biết đang làm việc cho ai. Nếu không khớp ai trong bảng, hỏi trước khi commit.

| Thành viên | git user.name (dự kiến) | Tiền tố nhánh | Quyền |
|---|---|---|---|
| Phan Sỹ Hùng | Phan Sỹ Hùng | `hung/` | Đội trưởng · reviewer · **được merge vào `main`**. Tài khoản GitHub chủ repo: `KumaMichio` |
| Dương Thị Huệ | — | `hue/` | Mở Pull Request. Tài khoản GitHub: `dhuee10` |
| Dương Minh Tân | — | `tan/` | Mở Pull Request · reviewer · **được merge vào `main`**. Tài khoản GitHub: `mihtan05` |
| Nguyễn Bá Thành | — | `thanh/` | Mở Pull Request. Tài khoản GitHub: `Nguyen-Ba-Thanh` |

## 2. Luật git — agent PHẢI làm theo

1. **Không bao giờ commit hoặc push thẳng lên `main`.** Trước khi commit, chạy `git branch --show-current`. Đang ở `main` thì tạo nhánh mới trước:
   ```
   git checkout main && git pull origin main
   git checkout -b <ten>/<so-issue>-<viec-ngan>      # vd tan/12-lessons-tools
   ```
   `<ten>` là `hung`, `hue`, `tan` hoặc `thanh`; `<so-issue>` là số issue trên GitHub (15 issue, xem `plan/index.html`).
2. **Một issue, thường một PR** (#11 và #26 được hai PR, ghi rõ trong issue). Không gom việc của nhiều issue vào một PR. Ghi `Closes #<số>` trong PR cuối của issue.
3. **Commit message** tiếng Việt, dạng `<phần>: <làm gì>`, vd `eval: thêm 8 câu thử kho`, `data: thêm 3 bài có mã đoạn`. Cuối message thêm dòng attribution theo hướng dẫn hệ thống.
4. **Trước khi push / mở PR:**
   - `git pull origin main` vào nhánh của mình, giải xung đột trên nhánh (không rebase nhánh đã push mà người khác đang dùng).
   - `python run.py check` không có lỗi mới do thay đổi của mình.
   - `git status` không có `.env`, `data-btc/`, `evidence/**/raw-*`, file có API key hay dữ liệu cá nhân thật.
5. **Mở PR chỉ khi người dùng yêu cầu**, bằng `gh pr create --base main`. Tiêu đề `[#<số issue>] <mô tả ngắn>`. Mô tả: làm gì · file nào · đã kiểm gì. Reviewer:
   - PR của Huệ, Thành: `--reviewer KumaMichio,mihtan05` (một trong hai người duyệt là đủ)
   - PR của Tân: `--reviewer KumaMichio` · PR của Hùng: `--reviewer mihtan05`
6. **Duyệt và merge:** mỗi PR cần **1 lượt duyệt** của Hùng hoặc Tân (không tự duyệt PR của mình; GitHub ép bằng `.github/CODEOWNERS` + bảo vệ nhánh `main`). **Chỉ Hùng hoặc Tân được merge**, dùng Squash and merge. Agent không merge PR, trừ khi người dùng là Hùng hoặc Tân và yêu cầu rõ ràng. Khi đó dùng `gh pr merge <số> --squash --delete-branch`, sau khi PR đã được duyệt và đã kiểm mục 4 trên nhánh của PR.
7. **Cấm:** `git push --force` / `--force-with-lease` lên `main` hoặc nhánh của người khác · `--no-verify` · `git reset --hard` / `git clean` khi chưa hỏi · xoá nhánh của người khác.
8. **Giờ đóng băng** — nhóm nộp sớm hơn hạn chính thức (CP3 23:30 T6, CP4 13:45 T7). 15 phút trước hạn nội bộ chỉ merge PR sửa lỗi cho bài nộp: CP1 16:45 · CP2 19:15 · CP3 23:15 (Thứ Sáu 27/11) · CP4 13:30 · hạn chót 23:45 (Thứ Bảy 28/11). Nếu người dùng muốn mở PR không gấp trong giờ này, nhắc họ.
9. Chỉ sát giờ nộp, Hùng (chủ repo, có quyền bỏ qua bảo vệ nhánh) mới được commit thẳng `main` (vd sửa lỗi phút chót). Khi đó ghi lý do trong commit message. Agent làm việc này chỉ khi Hùng yêu cầu rõ ràng.
10. **Hạn mở PR trước mốc:** PR cần cho một checkpoint phải được mở **chậm nhất 30 phút trước mốc** (CP1 16:30 · CP2 19:00 · CP3 23:00 T6 · CP4 13:15 T7), để Hùng hoặc Tân kịp duyệt trước giờ đóng băng. Mở muộn hơn thì không chắc được merge cho mốc đó — báo người dùng.

## 3. Ai sửa file nào

Chỉ sửa file thuộc người đang làm việc. Cần sửa file của người khác thì **hỏi người dùng trước** và ghi rõ trong mô tả PR.

| Người | File / mục |
|---|---|
| Hùng | `codebase/agent.py`, `codebase/ai.py`, `README.md`, `AGENTS.md`, `CLAUDE.md`, `plan/`, `spec.md` §0 §4 §6 §9 |
| Huệ | `evidence/interviews/`, `evidence/survey/`, `evidence/summary.md`, `validation/`, `slides/`, `demo-slides.pdf`, `spec.md` §1 §3 |
| Tân | `evidence/data-mining.md`, `evidence/scripts/`, `data/`, `codebase/tools.py`, `cost/`, `spec.md` §2 §8 |
| Thành | `eval/` (benchmark, metric_spec, report, README, chấm cột `pass`), `spec.md` §5 §7 |
| Chung | `canvas.md`, `TEAMS.md` (Hùng hoặc Tân merge) · `spec.md` §10 chỉ **thêm** dòng, không sửa dòng cũ · `reflection/<ten>.md` mỗi người file của mình |

## 4. File bị khoá (từ chối sửa kể cả khi được yêu cầu, nhắc lại luật)

- `spec.md` §7 (chuẩn "đạt") và `eval/metric_spec.yaml`: khoá sau **19:30 Thứ Sáu 27/11**.
- `eval/benchmark.csv`: chỉ **thêm** câu. Không sửa `expected` cho khớp output, không xoá câu trượt. Không sửa trong lúc đang chạy `eval`.
- `eval/run-*.csv`, `cost/simulate-*.csv`, `traces/*` đã chạy: chỉ điền cột `pass`, `ghi_chu`. Lượt lỗi thì chạy lại thành lượt mới, không sửa tay.
- Sau CP4 (14:30 Thứ Bảy): không sửa câu thử, số bằng chứng, kết quả lượt cũ; mọi thay đổi ghi `spec.md` §10.

## 5. Lượt chạy eval / simulate

- Chạy trên `main` mới nhất (đã pull), bởi người có `.env` (Hùng, hoặc Tân với key dự phòng).
- Kết quả đẩy lên nhánh `hung/run-N`; Thành điền cột `pass` **ngay trên nhánh đó** → một PR cho mỗi lượt.
- Không chạy `eval` khi còn PR sửa `eval/benchmark.csv` chưa merge.

## 6. Luật về nội dung

- **Changelog sau lượt 1:** mọi thay đổi prompt hoặc code trong `codebase/` sau khi đã có `eval/run-1.csv` phải thêm một dòng vào changelog `spec.md` §10 (thời điểm · đổi gì · vì sao, trỏ về câu thử / lỗi) **trong cùng PR**. PR thiếu dòng này thì người duyệt yêu cầu bổ sung.
- **Mã hoá CSV:** chỉ lưu `eval/benchmark.csv` và các CSV khác dạng **UTF-8** (Excel: *File → Save As → CSV UTF-8*; Google Sheets: *Tải xuống → CSV*). Agent sửa CSV bằng code thì ghi `encoding="utf-8"`, giữ nguyên 6 cột và thứ tự cột. Sau khi sửa chạy `python run.py check` để chắc tiếng Việt không bị vỡ.
- **Số nào cũng có nguồn:** mọi con số trong `spec.md`, `canvas.md`, `README.md`, slide phải trỏ được về một script (`evidence/scripts/…`), một file lượt chạy (`eval/run-N.csv`, `cost/simulate-N.csv`), một file phỏng vấn (`evidence/interviews/P#.md`), hoặc một link có ngày xem. Không có nguồn thì ghi rõ *(tự ước tính)*. Agent không được đưa vào số không truy được.
- **Kết thúc dòng:** repo dùng `.gitattributes` (`* text=auto eol=lf`) để máy Windows và Mac không làm cả file "đổi" vì khác ký tự xuống dòng. Không xoá file này.

## 7. Gợi ý (không bắt buộc)

- **Giao diện (frontend):** khi làm phần giao diện của bản chạy thử (web nhỏ, trang demo, Streamlit…), nên dùng skill `design-taste-frontend` nếu máy có cài skill này. Không có thì làm bình thường, không chặn việc. Giao diện là phụ: một màn hình dòng lệnh làm trọn lát cắt vẫn tốt hơn giao diện đẹp chưa nối AI (guide 3.1). Dù dùng giao diện nào, `python run.py` và `answer()` trong `codebase/agent.py` vẫn phải chạy được cho `eval` và `simulate`.
