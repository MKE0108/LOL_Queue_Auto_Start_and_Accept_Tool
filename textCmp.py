import Levenshtein

def levenshtein_similarity(str1, str2):
    distance = Levenshtein.distance(str1, str2)
    max_len = max(len(str1), len(str2))
    if max_len == 0:  # 防止除以零
        return 1
    return 1 - distance / max_len

def find_similar_name_from_list(name, name_list):
    # 从名单中找到与给定名字最相似的名字(levenshtein_similarity最高的)
    # return 在名单中找到的名字
    max_similarity = 0
    similar_name = None
    for n in name_list:
        similarity = levenshtein_similarity(name, n)
        if similarity > max_similarity:
            max_similarity = similarity
            similar_name = n
    return similar_name