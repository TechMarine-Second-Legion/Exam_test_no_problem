from gtts import gTTS

def make_ans_voice(textux='Првиет, мир', path_to_save='./', voice_file='voiesd.mp3', lan='ru'):
    tts = gTTS(text= textux, lang=lan)
    tts.save(path_to_save+voice_file)
    return voice_file
