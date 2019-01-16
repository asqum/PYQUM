from pyqum.instrument.logger import get_data, search_param

userdata = get_data("LTH")

result = search_param(userdata, 'NCHUQ_S21')
print("Search result for 'S21': %s" %[x for x in result])

for key in result[:len(result)-1]:
    print(result.value(key))