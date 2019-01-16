from pyqum.instrument.logger import get_data, search_param

userdata = get_data("LTH")

result = search_param(userdata, 'NCHUQ_S21')
print("Search result for 'S21': %s" %[x for x in result])

USR = userdata[result[0]]
for key in result[1:len(result)-1]:
    USR = userdata[key]
    print(USR)
