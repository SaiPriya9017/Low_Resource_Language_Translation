
import pandas as pd
from gtts import gTTS
import os, re
from pydub import AudioSegment

excel_file = r"C:\Users\Asus\Desktop\Major\english_banjara_words.xlsx"
df = pd.read_excel(excel_file)

output_dir = "banjari_audio"
os.makedirs(output_dir, exist_ok=True)

def apply_emotion(audio_path, emotion):
    sound = AudioSegment.from_mp3(audio_path)

    if emotion == "happy":
        sound = sound.speedup(playback_speed=1.2).apply_gain(+4)
    elif emotion == "sad":
        sound = sound.speedup(playback_speed=0.9).apply_gain(-3)
    elif emotion == "angry":
        sound = sound.speedup(playback_speed=1.3).apply_gain(+6)
    elif emotion == "calm":
        sound = sound.speedup(playback_speed=0.95).apply_gain(-1)

    # Save with emotion suffix
    new_path = audio_path.replace(".mp3", f"_{emotion}.mp3")
    sound.export(new_path, format="mp3")
    print(f"🎭 Added {emotion} emotion: {new_path}")

for index, row in df.iterrows():
    eng = str(row[0]).strip()
    banjari = str(row[1]).strip()
    
    if pd.isna(eng) or pd.isna(banjari):
        continue  

    safe_eng = re.sub(r'[\\/*?:"<>|]', "_", eng)
    safe_banjari = re.sub(r'[\\/*?:"<>|]', "_", banjari)

    # Generate base mp3
    tts = gTTS(text=banjari, lang="en")
    filename = f"{output_dir}/{safe_eng}_{safe_banjari}.mp3"
    tts.save(filename)
    print(f"✅ Saved: {filename}")

    # Generate emotional variations
    for emotion in ["happy", "sad", "angry", "calm"]:
        apply_emotion(filename, emotion)
