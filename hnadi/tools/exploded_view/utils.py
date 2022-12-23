def get_name_from_path(path:str):
    reverse_str = list(reversed(path))
    num = len(reverse_str)-((reverse_str.index("/"))+1)
    name = path[num+1:]
    return name

def get_pure_list(list:list):
    new_list = []
    for i in list:
        full_path0 = i.GetPrimPath()
        full_path = str(full_path0)
        if get_name_from_path(full_path) != "Explosion_Centre":
            new_list.append(i)
        # print(new_list)
    return new_list