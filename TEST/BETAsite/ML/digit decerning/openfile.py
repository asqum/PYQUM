import csv
import matplotlib.pyplot as plt
import numpy as np

def smooth(y, box_pts): # used to smooth the curve 
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

with open('1Dsqepulse (1).csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    t_row = list()
    I_row = list()
    Q_row = list()
    A_row = list()
    I_dist = list()
    Q_dist = list()
    A_dist = list()
    i = 0
    for row in rows:
        if (len(row) != 0) & (i != 0):
            t_row.append(float(row[0]))
            I_row.append(float(row[1]))
            Q_row.append(float(row[2]))
            A_row.append(float(row[3]))
            #if (len(I_dist) == 0) & (len(Q_dist) == 0) & (len(A_dist) == 0):
                ##I_dist.append(float(row[1]))
               #Q_dist.append(float(row[2]))
                #A_dist.append(float(row[3]))
            #else: 
                #I_dist.append((float(row[1]) - I_row[-2])/(t_row[-1] - t_row[-2]))
                #Q_dist.append(float(row[2]) - Q_row[-2])
                #A_dist.append(float(row[3]) - A_row[-2])
        i = i + 1
    #plt.plot(t_row, I_row, 'ro')
    #plt.plot(t_row, Q_row, 'ro')
    plt.plot(t_row, A_row, 'ro')
    I_row_smooth = smooth(I_row, 10)
    Q_row_smooth = smooth(Q_row, 10)
    A_row_smooth = smooth(A_row, 10)
    A_point = list()
    B_point = list()
    A_value = list()
    B_value = list()
    for i in range(3):
        A_point.append(0)
        B_point.append(0)
        A_value.append(0)
        B_value.append(0)
    for i in range(len(t_row)):
        if i != 0:
            I_dist.append((I_row_smooth[i] - I_row_smooth[i - 1])/(t_row[i] - t_row[i - 1]))
            Q_dist.append((Q_row_smooth[i] - Q_row_smooth[i - 1])/(t_row[i] - t_row[i - 1]))
            A_dist.append((A_row_smooth[i] - A_row_smooth[i - 1])/(t_row[i] - t_row[i - 1]))
        else:
            I_dist.append(0)
            Q_dist.append(0)
            A_dist.append(0)
    for i in range(int(len(t_row) / 2)):
        if i == 0:
            A_point[0] = i
            A_value[0] = abs(I_dist[i])
            B_point[0] = len(t_row) - i - 1
            B_value[0] = abs(I_dist[-i - 1])
            A_point[1] = i
            A_value[1] = abs(Q_dist[i])
            B_point[1] = len(t_row) - i - 1
            B_value[1] = abs(Q_dist[-i - 1])
            A_point[2] = i
            A_value[2] = abs(A_dist[i])
            B_point[2] = len(t_row) - i - i
            B_value[2] = abs(A_dist[-i - 1])
        if abs(I_dist[i]) > abs(A_value[0]):
            A_point[0] = i
            A_value[0] = abs(I_dist[i])
        if abs(Q_dist[i]) > abs(A_value[1]):
            A_point[1] = i
            A_value[1] = abs(Q_dist[i])
        if abs(A_dist[i]) > abs(A_value[2]):
            A_point[2] = i
            A_value[2] = abs(A_dist[i])
        if abs(I_dist[-i - 1]) > abs(B_value[0]):
            B_point[0] = len(t_row) - i - 1
            B_value[0] = abs(I_dist[-i - 1])
        if abs(Q_dist[-i - 1]) > abs(B_value[1]):
            B_point[1] = len(t_row) - i - 1
            B_value[1] = abs(Q_dist[-i - 1])
        if abs(A_dist[-i - 1]) > abs(B_value[2]):
            B_point[2] = len(t_row) - i - 1
            B_value[2] = abs(A_dist[-i - 1])
    plt.plot(t_row, smooth(A_row, 20))
    #plt.plot(t_row, smooth(Q_row, 20))
    #plt.plot(t_row, I_row_smooth)
    plt. axvline(x = t_row[A_point[2] + 4])
    plt. axvline(x = t_row[B_point[2] - 5])
    plt.show()
