def locate(element, array):
    loc = []
    j = 0
    try:
        while True:
            loc.append(array.index(element) + j)
            array.remove(element)
            j += 1
    except: [array.insert(i, element) for i in loc]
    return loc

# loca = locate(5, [0,1,2,5,3,6,7])
# print(loca)