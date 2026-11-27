/**
 * Tạo Google Form khảo sát "xem video pre-class" (#8 / #25) — phụ trách: Dương Thị Huệ.
 *
 * Cách chạy (2 phút):
 *   1. Mở https://script.google.com → Dự án mới.
 *   2. Xoá code mẫu, dán toàn bộ file này vào, bấm Lưu.
 *   3. Chọn hàm createPreclassForm → Chạy → cho phép quyền (Google Forms) khi được hỏi.
 *   4. Mở "Nhật ký thực thi": có link sửa form và link gửi học viên.
 *
 * Luật (evidence/survey/TEMPLATE.md):
 *   - Hỏi hành vi đã xảy ra, không hỏi "có thích không"; không nhắc giải pháp của nhóm.
 *   - Không thu tên, email, mã học viên (chỉ câu cuối, nếu người trả lời tự để lại).
 *   - Ngưỡng khảo sát: ≥20 người ngoài nhóm, đúng người dùng. Form KHÔNG thay phỏng vấn P1–P4.
 *   - Xuất kết quả → evidence/survey/results.csv đã XOÁ cột liên hệ; bản gốc không commit.
 */
function createPreclassForm() {
  var form = FormApp.create('Khảo sát: xem video pre-class và chỗ chưa hiểu (L3 · AI20K K5)');
  form.setDescription(
    'Nhóm Probably-Functional (L3A) đang tìm hiểu cách học viên xử lý chỗ chưa hiểu khi xem video pre-class. ' +
    'Khoảng 3 phút. Không thu tên, email hay mã học viên. Hãy trả lời theo LẦN GẦN NHẤT bạn xem video, không theo "thường thì".'
  );
  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false); // để không bắt đăng nhập
  form.setAllowResponseEdits(false);
  form.setShowLinkToRespondAgain(false);
  form.setProgressBar(true);

  // 1. Lọc đúng người dùng
  form.addMultipleChoiceItem()
    .setTitle('Bạn là:')
    .setChoiceValues(['Học viên L3A', 'Học viên L3B', 'Lab coach / TA', 'Giảng viên', 'Khác'])
    .setRequired(true);

  // 2. Lần gần nhất xem video
  form.addMultipleChoiceItem()
    .setTitle('Lần gần nhất bạn xem video pre-class là khi nào?')
    .setChoiceValues(['Hôm nay', 'Trong tuần này', 'Tuần trước', 'Lâu hơn', 'Chưa xem bao giờ'])
    .setRequired(true);

  // 3. Có gặp chỗ chưa hiểu không
  form.addMultipleChoiceItem()
    .setTitle('Trong lần xem gần nhất đó, có chỗ nào bạn chưa hiểu không?')
    .setChoiceValues(['Có', 'Không', 'Không nhớ'])
    .setRequired(true);

  // 4. Đã làm gì (nhiều lựa chọn)
  form.addCheckboxItem()
    .setTitle('Lần gần nhất gặp chỗ chưa hiểu trong video, bạn đã làm gì? (chọn mọi việc đã làm)')
    .setChoiceValues([
      'Tua lại video',
      'Hỏi trợ giảng AI ngay dưới video',
      'Hỏi bạn học / nhóm',
      'Hỏi trên Discord',
      'Hỏi ChatGPT / AI khác bên ngoài',
      'Tự tìm trên Google / tài liệu',
      'Bỏ qua, xem tiếp'
    ])
    .showOtherOption(true);

  // 5. Mất bao lâu
  form.addMultipleChoiceItem()
    .setTitle('Lần đó mất khoảng bao lâu đến khi bạn hiểu (hoặc bỏ qua)?')
    .setChoiceValues(['Dưới 5 phút', '5–15 phút', '15–30 phút', 'Trên 30 phút', 'Không nhớ']);

  // 6. Kết quả
  form.addMultipleChoiceItem()
    .setTitle('Cuối cùng lần đó bạn có hiểu ra không?')
    .setChoiceValues(['Hiểu', 'Hiểu một phần', 'Không, bỏ qua', 'Vào lớp mới thấy mình hiểu sai']);

  // 7. Tần suất (số)
  form.addTextItem()
    .setTitle('Trong 1 tuần qua, bạn gặp chỗ chưa hiểu khi xem video pre-class khoảng mấy lần?')
    .setHelpText('Ghi một con số. Không nhớ thì ghi "không nhớ".');

  // 8. Trợ giảng: làm gì sau khi đọc câu trả lời (kiểm số E/F trong evidence/data-mining.md)
  form.addCheckboxItem()
    .setTitle('Nếu bạn từng hỏi trợ giảng AI dưới video: lần gần nhất, ngay sau khi đọc câu trả lời bạn đã làm gì?')
    .setChoiceValues([
      'Chưa từng hỏi trợ giảng',
      'Hiểu luôn, xem tiếp',
      'Hỏi lại / hỏi tiếp trợ giảng',
      'Tua lại video để kiểm',
      'Hỏi chỗ khác để kiểm',
      'Không chắc đúng nhưng vẫn xem tiếp'
    ])
    .showOtherOption(true);

  // 9. Kiểm đúng sai bằng cách nào (kiểm số D)
  form.addParagraphTextItem()
    .setTitle('Bạn kiểm câu trả lời của trợ giảng đúng hay sai bằng cách nào? Kể lần gần nhất.');

  // 10. Khó chịu nhất
  form.addParagraphTextItem()
    .setTitle('Điều gì khó chịu nhất ở lần gần nhất bạn gặp chỗ chưa hiểu trong video?');

  // 11. Tuyển người phỏng vấn (tuỳ chọn)
  form.addMultipleChoiceItem()
    .setTitle('Bạn có sẵn lòng cho nhóm hỏi thêm 10–15 phút (gọi online) không?')
    .setChoiceValues(['Có', 'Không']);
  form.addTextItem()
    .setTitle('Nếu có: cách liên hệ (Discord / Zalo…) — không bắt buộc')
    .setHelpText('Chỉ dùng để hẹn phỏng vấn, không đưa vào báo cáo.');

  form.setConfirmationMessage('Cảm ơn bạn! Nhóm Probably-Functional chỉ dùng số tổng hợp, không ghi tên ai.');

  Logger.log('Link sửa form: ' + form.getEditUrl());
  Logger.log('Link gửi học viên: ' + form.getPublishedUrl());
}
