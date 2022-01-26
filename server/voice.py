from gtts import gTTS
import conf_server as params

def make_ans_voice():
    file_text = params.voice_ans.file_for_voice
    voice_file = params.voice_ans.voice_file
    lan = params.voice_ans.lan
    path_to_save = params.voice_ans.path_to_save

    with open(path_to_save+file_text,'r') as f:
        lan, ans_len = map(str, f.readline().replace('\n','').split())
        ans_len = int(ans_len)
        text1=''

        for i in range(min(ans_len,2)):
            vr = f.readline().replace('\n','.')
            text1+=vr

        # Здесь создаётся и сохраняется текст в речь
        tts = gTTS(text= text1, lang=lan)
        tts.save(path_to_save+voice_file)

        return path_to_save+voice_file
