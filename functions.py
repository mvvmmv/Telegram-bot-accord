import re


def get_chords_by_key_and_harmony(key: str, lad='натуральный мажор'):
    '''key - буквенное обозначение ноты,
    lad - название лада,
    возвращаемое значение - список аккордов в заданной тональности'''

    # получаем нужную гамму
    gamma = get_gamma_by_key_and_harmony(key, lad)

    # строим аккорды
    T53 = gamma[0]+gamma[2]+gamma[4]
    T6 = gamma[2]+gamma[4]+gamma[0]
    T64 = gamma[4]+gamma[0]+gamma[2]

    S53 = gamma[3]+gamma[5]+gamma[0]
    S6 = gamma[5]+gamma[0]+gamma[3]
    S64 = gamma[0]+gamma[5]+gamma[3]

    D53 = gamma[4]+gamma[6]+gamma[1]
    D6 = gamma[6]+gamma[1]+gamma[4]
    D64 = gamma[1]+gamma[4]+gamma[6]

    return ['T ', T53, T6, T64, '\nS ', S53, S6, S64, '\nD ', D53, D6, D64]


def get_gamma_by_key_and_harmony(key, lad='натуральный мажор'):
    '''Получить гамму по заданному ключу (тону) и ладу.
    key - ключ (тон), lad - название лада'''

    # проверка на корректность ключа
    gamma_copy = get_gamma().copy()
    gamma_copy.extend(get_sharp_flats().values())
    if key not in gamma_copy:
        return ['Ошибка: Некорректный ключ']

    # получить нужную гамму из всех построенных
    for gamma in GAMMAS[lad]:
        if gamma[0] == key:
            return (sharp_to_flat_check(gamma))


def get_gammas_by_harmony(lad='натуральный мажор'):
    '''lad - название лада,
    возвращаемое значение - список гамм от всех нот,
    соответствующий заданному lad'''

    # все ноты хроматической гаммы
    gamma = get_gamma()
    # все лады
    harmonies = get_harmonies()

    # проверка на корректность лада
    try:
        lad = harmonies[lad]
    except Exception:
        return ['Ошибка: Некорректный лад']

    gammas = []

    # строим гаммы для лада начиная с каждой ноты лада
    # гаммы представлены в виде 0 и 1
    for i in range(len(lad)):
        new_gamma = gamma[i:] + gamma[:i]
        gammas.append(new_gamma)

    nn_gammas = []

    # переводим каждую гамму в буквенную
    for gamma in gammas:
        nn_gammas.append([gamma[j] for j in range(len(lad)) if lad[j] == 1])

    return nn_gammas


def get_all_gammas():
    '''Получить все гаммы для всех ключей и ладов'''

    all_gammas = {}
    for lad in get_harmonies().keys():
        all_gammas[lad] = get_gammas_by_harmony(lad)
    return all_gammas


def sharp_to_flat_check(gamma):
    '''Проверить есть ли в гамме ноты с диезами, которые надо заменить
    на соответствующие ноты с бемолями'''

    new_gamma = gamma.copy()
    # если в гамме есть две одинаковые ноты (одна с диезом, одна - без)
    # то, заменяем их в соответствии с sharp_flat
    if re.search(r'(\w)\1', ''.join(gamma)):
        new_gamma = replace_sharps(gamma)
    # если в гамме все ноты с диезами
    # то, заменяем их в соответствии с sharp_flat
    elif ''.join(gamma).count('#') == 7:
        new_gamma = replace_sharps(gamma)
    return new_gamma


def get_sharp_flats():
    '''Словарь соответствия обозначени звуков,
    так как для одного звука может быть два обозначения'''

    sharp_flat = {
        'C#': 'Db',
        'D#': 'Eb',
        'E#': 'F',
        'F#': 'Gb',
        'G#': 'Ab',
        'A#': 'Hb',
        'H#': 'C'
    }
    return sharp_flat


def replace_sharps(gamma):
    '''Заменить ноты с диезами на соотв. ноты с бемолями'''

    sharp_flat = get_sharp_flats()
    new_gamma = []
    for key in gamma:
        if '#' in key:
            new_gamma.append(sharp_flat[key])
        else:
            new_gamma.append(key)
    return new_gamma


def get_gamma():
    '''Список всех нот хроматической гаммы от ноты До до ноты СИ'''

    return ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'H']


def get_harmonies():
    '''Словарь для построения ладов,
    ключи - названия ладов, 
    значения - схема по которой они строятся в музыке'''

    # 12 хроматических нот (1 - нота в гамме, 0 - нота отсутствует в гамме)
    harmonies = {
        'натуральный мажор': [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
        'натуральный минор': [1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1],
        'гармонический мажор': [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
        'гармонический минор': [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1],
        'локрийский лад (минор)': [1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
        'фригийский лад (минор)': [1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0]
    }
    return harmonies


GAMMAS = get_all_gammas()
