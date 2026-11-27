# CLAUDE.md — luật cho Claude Code (và mọi coding agent) trong repo này

@AGENTS.md

Repo nộp bài hackathon AI20K K5 · L3A · Track A (hướng A1) của nhóm Probably-Functional. Luật chung của repo (lệnh, cấu trúc code, những gì không được sửa) nằm ở `AGENTS.md`, đã được import ở trên. File này thêm **quy trình git** và **phân quyền file**. Kế hoạch và phân công: `plan/index.html`.

## 1. Ai là ai

Đọc `git config user.name` để biết đang làm việc cho ai. Nếu không khớp ai trong bảng, hỏi trước khi commit.

| Thành viên | git user.name (dự kiến) | Tiền tố nhánh | Quyền |
|---|---|---|---|
| Phan Sỹ Hùng | Phan Sỹ Hùng | `hung/` | Đội trưởng · reviewer · **được merge vào `main`**. Tài khoản GitHub chủ repo: `KumaMichio` |
| Dương Thị Huệ | — | `hue/` | Mở Pull Request |
| Dương Minh Tân | — | `tan/` | Mở Pull Request · reviewer · **được merge vào `main`**. Tài khoản GitHub: `mihtan05` |
| Nguyễn Bá Thành | — | `thanh/` | Mở Pull Request |

## 2. Luật git — agent PHẢI làm theo

1. **Không bao giờ commit hoặc push thẳng lên `main`.** Trước khi commit, chạy `git branch --show-current`. Đang ở `main` thì tạo nhánh mới trước:
   ```
   git checkout main && git pull origin main
   git checkout -b <ten>/<Txx-viec-ngan>      # vd tan/T12-lessons-tools
   ```
   `<ten>` là `hung`, `hue`, `tan` hoặc `thanh`; `Txx` là mã task trong `plan/index.html`.
2. **Một nhánh, một PR cho một task.** Không gom việc của nhiều task vào một PR.
3. **Commit message** tiếng Việt, dạng `<phần>: <làm gì>`, vd `eval: thêm 8 câu thử kho`, `data: thêm 3 bài có mã đoạn`. Cuối message thêm dòng attribution theo hướng dẫn hệ thống.
4. **Trước khi push / mở PR:**
   - `git pull origin main` vào nhánh của mình, giải xung đột trên nhánh (không rebase nhánh đã push mà người khác đang dùng).
   - `python run.py check` không có lỗi mới do thay đổi của mình.
   - `git status` không có `.env`, `data-btc/`, `evidence/**/raw-*`, file có API key hay dữ liệu cá nhân thật.
5. **Mở PR chỉ khi người dùng yêu cầu**, bằng `gh pr create --base main`. Tiêu đề `[Txx] <mô tả ngắn>`. Mô tả: làm gì · file nào · đã kiểm gì. Reviewer:
   - PR của Huệ, Thành: `--reviewer KumaMichio,mihtan05` (một trong hai người duyệt là đủ)
   - PR của Tân: `--reviewer KumaMichio` · PR của Hùng: `--reviewer mihtan05`
6. **Duyệt và merge:** mỗi PR cần **1 lượt duyệt** của Hùng hoặc Tân (không tự duyệt PR của mình; GitHub ép bằng `.github/CODEOWNERS` + bảo vệ nhánh `main`). **Chỉ Hùng hoặc Tân được merge**, dùng Squash and merge. Agent không merge PR, trừ khi người dùng là Hùng hoặc Tân và yêu cầu rõ ràng. Khi đó dùng `gh pr merge <số> --squash --delete-branch`, sau khi PR đã được duyệt và đã kiểm mục 4 trên nhánh của PR.
7. **Cấm:** `git push --force` / `--force-with-lease` lên `main` hoặc nhánh của người khác · `--no-verify` · `git reset --hard` / `git clean` khi chưa hỏi · xoá nhánh của người khác.
8. **Giờ đóng băng** — 15 phút trước mỗi mốc chỉ merge PR sửa lỗi cho bài nộp: CP1 16:45 · CP2 19:15 (Thứ Sáu 27/11) · CP3 09:45 · CP4 14:15 · hạn chót 23:45 (Thứ Bảy 28/11). Nếu người dùng muốn mở PR không gấp trong giờ này, nhắc họ.
9. Chỉ sát giờ nộp, Hùng (chủ repo, có quyền bỏ qua bảo vệ nhánh) mới được commit thẳng `main` (vd sửa lỗi phút chót). Khi đó ghi lý do trong commit message. Agent làm việc này chỉ khi Hùng yêu cầu rõ ràng.

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

- Chạy trên `main` mới nhất (đã pull), bởi người có `.env` (thường là Hùng).
- Kết quả đẩy ngay qua nhánh `hung/run-N` + PR. Chấm cột `pass` trên nhánh `thanh/cham-run-N`.
- Không chạy `eval` khi còn PR sửa `eval/benchmark.csv` chưa merge.

## 6. Gợi ý (không bắt buộc)

- **Giao diện (frontend):** khi làm phần giao diện của bản chạy thử (web nhỏ, trang demo, Streamlit…), nên dùng skill `design-taste-frontend` nếu máy có cài skill này. Không có thì làm bình thường, không chặn việc. Giao diện là phụ: một màn hình dòng lệnh làm trọn lát cắt vẫn tốt hơn giao diện đẹp chưa nối AI (guide 3.1). Dù dùng giao diện nào, `python run.py` và `answer()` trong `codebase/agent.py` vẫn phải chạy được cho `eval` và `simulate`.
