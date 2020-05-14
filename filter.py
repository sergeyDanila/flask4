def minmaxstring(lst, s):
    min_v = max_v = lst[0]
    for i in lst:
        if i < min_v:
            min_v = i
        if i > max_v:
            max_v = i
    return (s.replace('#min#', str(min_v))).replace('#max#', str(max_v))