"""Công cụ của bài toán — NHÓM VIẾT. Điền ở guide bước 2.2 (thiết kế) và 3.2 (code).

Mỗi công cụ là một hàm Python có @tool. Docstring ghi đúng 4 ý như sơ đồ ở spec.md §4:
    tên · input · output · có tác động ra ngoài không (gửi tin, sửa dữ liệu, chấm điểm…)
Khung tự ghi mỗi lần gọi công cụ vào trace (tên, input, output rút gọn, thời gian, lỗi).

Số công cụ, kiểu công cụ do thiết kế của nhóm quyết định — có bài chỉ cần một công cụ tra cứu.
Công cụ có tác động ra ngoài: KHÔNG tự làm. Trả về bản nháp chờ người duyệt (guide bước 2.2, "chỗ người duyệt").
Dữ liệu công cụ đọc (bài mẫu, thông báo mẫu, lịch…): để trong data/ và mô tả ở data/DATA_CARD.md.
"""
import json
import math
import re
from pathlib import Path

from tracing import tool, TOOLS  # noqa: F401  (TOOLS: danh sách công cụ đã đăng ký, dùng khi viết vòng lặp agent)

LESSONS_DIR = Path(__file__).resolve().parent.parent / "data" / "lessons"
MIN_SCORE = 0.3  # đoạn tốt nhất dưới ngưỡng này → coi như bài không có (guide: nói "không có trong bài")
RELATIVE = 1 / 3  # đoạn thứ 2, 3 chỉ cần đạt 1/3 điểm đoạn tốt nhất (câu hỏi hai ý)
UNKNOWN_WEIGHT = 1.5  # trọng số của từ không có trong bài nào (từ hiếm trong bài có idf ~2,8)
# Từ chức năng và từ đệm tiếng Việt hay gặp trong câu hỏi ("thầy nói ở phút 10, em chưa hiểu lắm…"), không mang nội dung bài
STOPWORDS = set("""
là gì của và có không được cho với trong khi thì mà này đó các những một để từ theo
như nào sao vì tại thế bao nhiêu ạ ơi nhé vậy hả em anh chị mình tôi bạn thầy cô ai
hỏi giải thích cho biết về làm hơn rất nên bị đã đang sẽ cũng còn ra vào lên đâu
chưa hiểu lắm phần lại giúp với thầy nói phút giây hôm qua nay xem tới đến video bài học
ở được nữa luôn thôi rồi dạ vâng ok khi sao
""".split())


def _words(text):
    words = [w for w in re.findall(r"\w+", text.lower()) if w not in STOPWORDS]
    # thêm cặp âm tiết liền nhau: tiếng Việt nhiều từ ghép ("ngữ cảnh", "cửa sổ")
    return set(words) | {a + " " + b for a, b in zip(words, words[1:])}


def _load():
    passages = []
    for f in sorted(LESSONS_DIR.glob("*.json")):
        lesson = json.loads(f.read_text(encoding="utf-8"))
        passages += [{"code": p["code"], "text": p["text"]} for p in lesson["passages"]]
    return passages


PASSAGES = _load()
_INDEX = [_words(p["text"]) for p in PASSAGES]
_DF = {}
for _ws in _INDEX:
    for _w in _ws:
        _DF[_w] = _DF.get(_w, 0) + 1


def _idf(word):
    # từ không có trong bài nào: trọng số thấp cố định, để câu hỏi dài, tự nhiên ("thầy nói ở phút 10…")
    # không bị kéo điểm xuống dưới ngưỡng chỉ vì nhiều chữ đệm
    if word not in _DF:
        return UNKNOWN_WEIGHT
    return math.log((len(PASSAGES) + 1) / (_DF[word] + 0.5))


@tool
def search_lesson(query: str, k: int = 3) -> list:
    """search_lesson · Input: câu hỏi của học viên (str), k = số đoạn tối đa (int, mặc định 3).
    Output: danh sách {"code", "text", "score"} xếp điểm giảm dần; [] nếu đoạn tốt nhất chưa đạt MIN_SCORE.
    Các đoạn sau đoạn đầu được giữ nếu điểm >= RELATIVE × điểm đoạn đầu.
    score = tỉ lệ trọng số (idf) các từ của câu hỏi có mặt trong đoạn, 0–1.
    Chỉ đọc file data/lessons/*.json, không tác động ra ngoài."""
    q = _words(query)
    total = sum(_idf(w) for w in q)
    if not total:
        return []
    hits = []
    for p, ws in zip(PASSAGES, _INDEX):
        common = q & ws
        if common:
            score = sum(_idf(w) for w in common) / total
            # phân hạng khi bằng điểm: từ khoá xuất hiện sớm hơn (đoạn định nghĩa "X là…") đứng trước
            text = p["text"].lower()
            # find() = -1 khi cặp âm tiết bị dấu câu chen giữa → bỏ, không thì đoạn đó luôn lên đầu
            first = min([i for i in (text.find(w) for w in common) if i >= 0] or [len(text)])
            hits.append((-score, first, {"code": p["code"], "text": p["text"], "score": round(score, 3)}))
    hits.sort(key=lambda t: t[:2])
    if not hits or -hits[0][0] < MIN_SCORE:
        return []
    # câu hỏi nhiều ý: đoạn đầu đạt MIN_SCORE thì giữ thêm đoạn có điểm >= RELATIVE × điểm đoạn đầu
    floor = -hits[0][0] * RELATIVE
    return [h for s, _, h in hits if -s >= floor][:k]


@tool
def get_passage(code: str) -> dict:
    """get_passage · Input: mã đoạn (str), vd "D07-L1-P03".
    Output: {"code", "text"}, hoặc None nếu mã không có thật (dùng để code kiểm mã model trích).
    Chỉ đọc file data/lessons/*.json, không tác động ra ngoài."""
    code = code.strip().upper()
    return next(({"code": p["code"], "text": p["text"]} for p in PASSAGES if p["code"] == code), None)


if __name__ == "__main__":
    # Tự kiểm hợp đồng chung: python codebase/tools.py
    import sys
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252, vỡ khi in tiếng Việt
    assert search_lesson("Token là gì?")[0]["code"] == "D01-L1-P02"
    assert search_lesson("prompt injection phòng thế nào")[0]["code"] == "D04-L1-P08"
    assert search_lesson("RAG là gì", k=1)[0]["code"] == "D07-L1-P01"
    assert search_lesson("cách nấu phở bò") == [] and search_lesson("?") == []
    assert len(search_lesson("token", k=2)) <= 2
    # câu hai ý: đoạn của ý thứ hai (0.27 < MIN_SCORE) vẫn được giữ nhờ RELATIVE
    assert {h["code"] for h in search_lesson("few-shot và chain-of-thought dùng khi nào")} == {"D04-L1-P03", "D04-L1-P04"}
    # câu hỏi dài, tự nhiên (nhiều chữ đệm, từ ngoài bài) vẫn ra đúng đoạn
    assert "D01-L1-P05" in [h["code"] for h in search_lesson("Thầy nói về hallucination ở phút 10, sao model lại bịa được?")]
    assert search_lesson("Hôm qua em xem video tới đoạn context window thì không hiểu lắm, nó là gì vậy ạ?")[0]["code"] == "D01-L1-P03"
    assert search_lesson("Em chưa hiểu lắm phần reranking trong video, giải thích lại giúp em với")[0]["code"] == "D07-L1-P05"
    assert search_lesson("Hôm nay trời Hà Nội mưa không, tối nay em có nên đi học không?") == []
    assert get_passage("d07-l1-p03")["code"] == "D07-L1-P03" and get_passage("D99-L1-P01") is None
    print("tools.py: OK ·", len(PASSAGES), "đoạn")
