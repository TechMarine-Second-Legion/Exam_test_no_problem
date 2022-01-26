#coding:utf-8
# Серверная часть настроек часть настроек

class for_search:
    server_port = 65432
    search_depth = 20 # Максимальная разница ответа и базы (для распознаных изображений)
    search_cnt = 3    # Количество выводимых ответов
    filters = [';', '.', ',', '?', ':', '№', '@',' ', '«', '»','-','_']
    to_lower = True

    separ = '?'
    path_to_base = '../../bases/openedu_pravo/' # Путь до базы, пока относительно


class voice_ans:
    path_to_save = './voice/req/'
    file_for_voice = 'text1.txt'
    voice_file='voiesd.mp3'
    lan = 'ru'

class messages:
    len_of_type = 3 # 3 символа для типа сообщения. req, inf, cmd
    inf_separ = ':' # лучше не трогать


if __name__ == "__main__":
    import take_and_continue
