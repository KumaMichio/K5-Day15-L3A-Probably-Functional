"""Sinh giọng đọc tiếng Việt bằng OmniVoice cho từng câu thuyết minh.

Chạy:  ovenv/python voice.py lines.json outdir
lines.json = [{"id": "n1", "text": "...", "max": 3.8}, ...]  — max: khung giây tối đa của câu đó
"""
import json
import sys

import soundfile as sf
import torch
from omnivoice import OmniVoice

lines = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2]
torch.manual_seed(7)  # giữ cùng một giọng giữa các lần chạy
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cpu", dtype=torch.float32)
VOICE = "female, moderate pitch"
sr = model.sampling_rate
result = {}
for ln in lines:
    audio = model.generate(text=ln["text"], language="vi", instruct=VOICE)[0]
    dur = len(audio) / sr
    if dur > ln["max"]:  # dài hơn khung → ép đúng độ dài khung
        audio = model.generate(text=ln["text"], language="vi", instruct=VOICE, duration=ln["max"])[0]
        dur = len(audio) / sr
    sf.write(f"{out}/{ln['id']}.wav", audio, sr)
    result[ln["id"]] = round(dur, 2)
    print(ln["id"], round(dur, 2), "/", ln["max"], flush=True)
json.dump(result, open(f"{out}/durations.json", "w"), indent=1)
