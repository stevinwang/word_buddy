import nltk
from nltk.stem import SnowballStemmer
from gtts import gTTS
from playsound import playsound
import os

# 下载 nltk 必要数据
nltk.download('punkt')

# 初始化词干提取器
stemmer = SnowballStemmer('english')

# 自定义词根词缀字典（这里只是简单示例，实际应用可扩充）
prefixes = {
    'un': '相反、否定',
    're': '再次、重新',
    'pre': '在……之前'
}

suffixes = {
    'er': '人、物',
    'ing': '正在进行',
    'ed': '过去式、过去分词'
}


def analyze_word(word):
    # 简单的词干提取
    stem = stemmer.stem(word)
    prefix = ""
    suffix = ""
    for pre in prefixes.keys():
        if word.startswith(pre):
            prefix = pre
            break
    for suf in suffixes.keys():
        if word.endswith(suf):
            suffix = suf
            break
    return prefix, stem, suffix


def speak_word(word):
    tts = gTTS(text=word, lang='en')
    audio_file = 'temp_audio.mp3'
    tts.save(audio_file)
    playsound(audio_file)
    # 删除临时音频文件
    os.remove(audio_file)


words = ["unhappy", "rewrite", "worker"]
for word in words:
    prefix, stem, suffix = analyze_word(word)
    print(f"单词: {word}")
    if prefix:
        print(f"前缀: {prefix} - {prefixes[prefix]}")
    print(f"词根: {stem}")
    if suffix:
        print(f"后缀: {suffix} - {suffixes[suffix]}")
    print("-" * 20)
    speak_word(word)
