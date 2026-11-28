"""Ghép video demo: khung mở đầu + đoạn quay e2e (không cắt giữa) + khung kết + phụ đề + giọng đọc.

  python build.py plan  <take>               → <take>/timeline.json (mỗi câu thuyết minh: giây bắt đầu + khung tối đa)
  python build.py video <take> <vo|-> <out>  → video 30 giây (vo = thư mục wav của voice.py, "-" = không tiếng)
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
INTRO, TOTAL = 2.0, 30.0


def load(path):
    return json.load(open(path, encoding="utf-8"))


def plan(take):
    """Neo từng câu vào mốc thao tác trong marks.json (mỗi lần quay, model trả lời nhanh chậm khác nhau)."""
    marks = load(f"{take}/marks.json")
    at = lambda a: 0.0 if a == "intro" else INTRO + marks[a] - marks["start"]
    lines = [dict(ln, at=round(at(ln["anchor"]) + ln["delta"], 2)) for ln in load(os.path.join(HERE, "lines.json"))]
    for i, ln in enumerate(lines):
        nxt = lines[i + 1]["at"] - 0.2 if i + 1 < len(lines) else TOTAL - 0.1
        ln["max"] = round(nxt - ln["at"], 2)
        assert ln["max"] > 1.0, "câu %s chỉ còn %.1f s" % (ln["id"], ln["max"])
    json.dump(lines, open(f"{take}/timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for ln in lines:
        print(ln["id"], ln["at"], ln["max"], ln["text"])


def ts(t):
    return "%d:%02d:%05.2f" % (t // 3600, t % 3600 // 60, t % 60)


def video(take, vo, dst):
    marks = load(f"{take}/marks.json")
    lines = load(f"{take}/timeline.json")
    durs = load(f"{vo}/durations.json") if vo != "-" else {}
    dur_raw = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                             "-of", "csv=p=0", f"{take}/raw.webm"]).decode())
    off = marks["end"] - dur_raw          # mốc (tính từ lúc mở trình duyệt) → giây trong file video
    cut_in = marks["start"] - off          # chỉ bỏ đoạn tải trang ở đầu, không cắt giữa
    body = marks["end"] - marks["start"]
    outro = TOTAL - INTRO - body
    assert outro > 1.5, "đoạn quay dài %.1f s, không còn chỗ cho khung kết — quay lại" % body
    print("lệch %.2f · cắt từ %.2f · đoạn quay %.2f s · khung kết %.2f s" % (off, cut_in, body, outro))

    ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080", "",
           "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV",
           "Style: S,Segoe UI,42,&H00FFFFFF,&H70201A14,&H70201A14,1,3,12,0,2,80,80,26", "",
           "[Events]", "Format: Layer, Start, End, Style, Text"]
    for i, ln in enumerate(lines):
        end = lines[i + 1]["at"] - 0.1 if i + 1 < len(lines) else TOTAL
        ass.append("Dialogue: 0,%s,%s,S,%s" % (ts(ln["at"]), ts(end), ln["text"]))
    subs = f"{take}/subs.ass"
    open(subs, "w", encoding="utf-8").write("\n".join(ass) + "\n")

    cmd = ["ffmpeg", "-v", "error", "-y",
           "-loop", "1", "-t", str(INTRO), "-i", f"{take}/intro.png",
           "-ss", "%.3f" % cut_in, "-t", "%.3f" % body, "-i", f"{take}/raw.webm",
           "-loop", "1", "-t", "%.3f" % outro, "-i", f"{take}/outro.png"]
    voiced = [ln for ln in lines if ln["id"] in durs]
    for ln in voiced:
        cmd += ["-i", f"{vo}/{ln['id']}.wav"]
    sc = "scale=1920:1080:flags=lanczos,fps=30,setsar=1"
    # subtitles= cần đường dẫn không có ':' (Windows) → dùng đường dẫn tương đối, chạy ffmpeg trong thư mục hiện tại
    v = f"[0:v]{sc}[a];[1:v]{sc}[b];[2:v]{sc}[c];[a][b][c]concat=n=3:v=1:a=0,subtitles={os.path.relpath(subs).replace(os.sep, '/')}[v]"
    if voiced:
        a = "".join("[%d:a]aresample=48000,adelay=%d:all=1[s%d];" % (3 + i, ln["at"] * 1000, i) for i, ln in enumerate(voiced))
        a += "".join("[s%d]" % i for i in range(len(voiced)))
        a += "amix=inputs=%d:normalize=0,apad,atrim=0:%.2f,loudnorm=I=-16:TP=-1.5[au]" % (len(voiced), TOTAL)
        cmd += ["-filter_complex", v + ";" + a, "-map", "[v]", "-map", "[au]", "-c:a", "aac", "-b:a", "160k"]
    else:
        cmd += ["-filter_complex", v, "-map", "[v]"]
    cmd += ["-c:v", "libx264", "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            "-t", str(TOTAL), dst]
    subprocess.run(cmd, check=True)
    print("xong:", os.path.abspath(dst))


if __name__ == "__main__":
    if sys.argv[1] == "plan":
        plan(sys.argv[2])
    else:
        video(*sys.argv[2:5])
