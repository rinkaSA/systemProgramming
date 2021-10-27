from collections import defaultdict

def alphabet(transition_func):
    alpha = set()
    for m in transition_func:
        alpha.add(m[2])
    return alpha


def distance(pos_1, pos_2, visited, dict_neigh):
    if pos_1 == pos_2:
        return True
    visited.add(int(pos_1))
    for e in dict_neigh[pos_1]:
        if e not in visited:
            if distance(int(e), int(pos_2), visited, dict_neigh):
                return True
    return False


def detect_path(w, curr_pos, transition_func, list_final_states, dict_with_letter_to_pos):
    path = [curr_pos]
    for e in range(len(w)):
        for m in transition_func:
            if curr_pos not in dict_with_letter_to_pos[w[e]]:
                print("Слово ne розпізналось автоматом")
                return []
            if int(m[0]) == curr_pos and w[e] == m[2]:
                curr_pos = int(m[4])
                path.append(curr_pos)
                break
        if e == len(w)-1 and str(curr_pos) in list_final_states:
            print("Слово розпізнається автоматом")
            return path
        if e == len(w)-1:
            print("Слово ne розпізналось автоматом")
            exit()


def w1_existence(pathes, dict_neigh):
    for p in pathes:
        if len(p) != 0 or "0" in dict_neigh[0]:  # існує слово з якоюсь буквою алфавіту спереду або є петля в нульвому стані
            return "Слово w1 iснує"
    return 'Слова w1 не існує'


def w2_existence(end_states, list_final_states_no_w0_end, visited, dict_neigh):
    for j in list(end_states):
        for g in list_final_states_no_w0_end:
            if distance(int(j), int(g), visited, dict_neigh) or j in dict_neigh[j]:  # з кінця в0 існує шлях до іншого кінц стану або петля
                return 'Слов w2 існує'
    return 'Слова w2 не існує'

def main():
    with open('input3.txt') as f:
        my_lines = list(f)

    set_final_states = set(my_lines[3].split())

    curr_pos = int(my_lines[2])
    transition_func = my_lines[4:]
    #w0 = 'acd'
    #w0 = 'cdb'
    w0 = 'cbd'
    alfav = alphabet(transition_func)

    list_f_neigh = []
    for i in transition_func:
        list_f_neigh.append((int(i[0]), int(i[4])))
    dict_neigh = defaultdict(list)

    for key, val in list_f_neigh:
        if val not in dict_neigh[key]:
            dict_neigh[key].append(val)

    l_with_letter_to_pos = []
    for i in transition_func:
        l_with_letter_to_pos.append((i[2], int(i[0])))
    dict_with_letter_to_pos = defaultdict(list)

    for key, val in l_with_letter_to_pos:
        if val not in dict_with_letter_to_pos[key]:
            dict_with_letter_to_pos[key].append(val)
    w_diff = [i + w0 for i in list(alfav)]
    pathes = []
    for k in w_diff:
        print(k)
        pathes.append(detect_path(k, curr_pos, transition_func, set_final_states, dict_with_letter_to_pos))
    print(pathes)

    end_states = set()
    for p in pathes:
        if len(p) != 0:
            end_states.add(str(p[-1]))
    difference = set_final_states.difference(end_states)
    list_final_states_no_w0_end = list(difference)
    visited = set()
    result = [w1_existence(pathes, dict_neigh), w2_existence(end_states, list_final_states_no_w0_end, visited, dict_neigh) ]
    return result


print(main())