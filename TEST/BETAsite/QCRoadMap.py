from pyqum.instrument.analyzer import curve

x = [1,2,3,4,5]
y1 = [1,2,4,8,16]
y2 = [1,2,4,7,10]

curve([x,x], [y1,y2], 'QC Road Map', 'Year', 'KPI', yscal='log', basy=2, style=['b','r'])