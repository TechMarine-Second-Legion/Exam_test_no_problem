import os#, vlc
import voice
import time
import conf_server

def clear_the_string(strin):

    filters = conf_server.for_search.filters
    toLower = conf_server.for_search.to_lower

    for i in filters:
        strin = strin.replace(i,'')
    if toLower:
        strin = strin.lower()

    return strin

# Расстояние Левейнштена
def distance(a : str, b : str):
    n, m = len(a), len(b)
    if n > m:
        # n <= m, чтобы использовать минимум памяти O(min(n, m))
        a, b = b, a
        n, m = m, n
    current_row = range(n + 1)  # 0 ряд - просто восходящая последовательность (одни вставки)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]

# Для верного порядка вывода ответов
def minest_q(mi, new):
    for i in range(len(mi)):
        if mi[i][0] > new:
            return mi[:i]+[[new, '']]+mi[i:-1], i


def load_answ_base(d):
    separ = conf_server.for_search.separ
    path_to_base = conf_server.for_search.path_to_base

    import text_voice

    with open(path_to_base+'all_inf.txt', 'r') as f:
        sh_name = f.readline().split(': ')[-1]
        os.system(f'cvlc {path_to_base}{text_voice.make_ans_voice("Загружена база: "+sh_name, path_to_base)} --play-and-exit')

    with open(path_to_base+'ans.txt', 'r') as f:
        for line in f:
            index = line.rfind('?')
            if index != -1:
                first_key = line[:index+1]
                key = clear_the_string(first_key)

                if len(first_key)>150:
                    a = [i for i in first_key.split()]
                    first_key = ' '.join(a[:4])+' ... '+' '.join(a[-4:])

                d[key] = (first_key, line.replace('\n','').replace('\t','')[index+1:])
    return d

# Поиск соответствий по загруженной базе
def find_in_d(phrase, d):

    len_of_ans = conf_server.for_search.search_cnt
    start_q = conf_server.for_search.search_depth

    phrase = clear_the_string(phrase)
    phrase_len = len(phrase)

    # Обход проблем с короткими вопросами
    start_q = min(int(phrase_len/2), start_q)

    succes=[] # Массив (около)успешных совпадений

    # Поиск точного вхождения
    for key, value in d.items():
        if key.find(phrase) != -1:
            succes.append([value[0], value[1]])
    if len(succes) > 0:
        return succes


    with open('./voice/req/vr.txt','w') as f:
        f.write(phrase)

    m = [[start_q, ''] for i in range(len_of_ans)]

    # Иначе поиск по расстоянию Левейнштена
    for key, value in d.items():
        dis = distance(key, phrase)
        if dis < m[-1][0]:

            # Наврех - самое близкое совпадение
            m, k = minest_q(m, dis)
            m[k][1] = key
        if m[0][0] <= 2:
            break
    print(*m, sep='\n')

    ind = len(m)
    for i in range(len(m)-1, -1, -1):
        if m[i][1] == '':
            ind-=1
        else:
            break

    for i in m[:ind]:
        first_key = d[i[1]][0]
        answ = d[i[1]][1]
        succes.append([first_key, answ])
    return succes


def print_ans(search_for, ans):
    n = len(ans)
    print(f"Запрос: {search_for}")
    print(f"Количество найденных ответов: {n}")
    for i in range(n):
        print(str(i+1).rjust(len(str(n)), ' '), end=' ')
        print(f"Вопрос: {ans[i][0]}")
        print(f"{' '*(len(str(n))+1)}Ответ: {ans[i][1]}", end ='\n\n')


# Обработка сообщений типа 'inf'
def inf_center(mess):

        sepr = conf_server.messages.inf_separ
        posible_status = {'active':'st_active.mp3', 'deactive':'st_deactive.mp3'}
        all_inf_func = {'watch':'W_ready.mp3', 'status': posible_status}

        i = mess.find(sepr)
        if i != -1:
            file_to_say = all_inf_func[mess[:i]][mess[i+1:]]
        else:
            file_to_say = all_inf_func[mess]

        os.system(f'cvlc ./voice/inf/{file_to_say} --play-and-exit')

# Приём всех сообщений
def message_center(d, mess):
    if len(mess)==0:
        return None
    print(mess)

    len_of_type = conf_server.messages.len_of_type

    qw_type = mess[:len_of_type]
    mess = mess[len_of_type:]
    if qw_type == 'inf':
        inf_center(mess)
    elif qw_type == 'cmd':
        print(mess)
    else:
        search_center(d, mess)

# Поиск, вывод и озучивание результатов
def search_center(d,search_for):
    if len(search_for)==0:
        return None
    print(search_for)

    path_to_save = conf_server.voice_ans.path_to_save
    file_for_voice = conf_server.voice_ans.file_for_voice
    voice_file = conf_server.voice_ans.voice_file

    d_ans = find_in_d(search_for, d)

    print_ans(search_for, d_ans)
    ans_len = len(d_ans)

    if ans_len>=1:
        with open(path_to_save+file_for_voice,'w') as f:
            f.write(f'ru {str(ans_len)}\n')
            for i in range(ans_len):
                if ans_len != 1:
                    f.write(f'Вариант №{i+1}. ')
                f.write(f"Вопрос. {d_ans[i][0]}. Ответ. {d_ans[i][1].replace('?.', '?').replace(' .', '.')}.\n")
        voice.make_ans_voice()
    else:
        voice_file ='no_match.mp3'
    time.sleep(0.2)

    os.system(f'cvlc {path_to_save}{voice_file} --play-and-exit')
