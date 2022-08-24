#<----------final update:0820---------------->

import pandas as pd
import numpy as np
from numpy import hstack,array
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import silhouette_score
from kneed import KneeLocator
from colorama import init, Fore, Back, Style

# kmeans input and fitting ,輸出預測資料及標籤
def k_fitter(x,y,k,ini_center ='k-means++'):
  
    #請KMeans分成k類
    clf = KMeans(n_clusters=k,init=ini_center)
    #開始訓練！
    clf.fit(y,x)
    #這樣就可以取得預測結果了！
    labels = clf.labels_

    return labels

# Trying
def dbscan(inp,eps,min_samples):
    labels = DBSCAN(eps=eps,min_samples=min_samples).fit(inp).labels_

    return labels


# 選出主群、最遠群及過度群之idx
def colect_cluster(labels,mode):
    peak_susp_idx = []
    nope_idx = []

    rec = simple_sort(labels,mode) #由少排到多

    target_k = rec[0] #最遠群
    env = rec[-1] #主群


    for i in range(len(labels)):
        if labels[i] == target_k[0]: #最遠群保留
            peak_susp_idx.append(i)
        if labels[i] == env[0]:  #主群計算中心
            nope_idx.append(i)

    return peak_susp_idx, nope_idx

#群集內數量排序（2群）
def simple_sort(labels,mode):  #input
    zero = 0
    _one = 0
    def Key(elem):
        return elem[1]

    if mode == 'db':
        for i in range(len(labels)):
            if labels[i]==-1 :
                _one += 1 
            else:
                zero += 1
        rec = [[0,zero],[-1,_one]] 
    else:
        for i in range(len(labels)):
            if labels[i]==1 :
                _one += 1 
            else:
                zero += 1
        rec = [[0,zero],[1,_one]]
    rec.sort(key = Key) #以數量由小到大排序

    return rec

#以下計算偵測到的點之振幅平均值，輸出平均值、幾倍標準差
def work_func(idx_list,sub_array,threshold):
    amp_detected = []
    for i in idx_list:
        for j in range(sub_array.shape[0]):
            if j == i:
                amp_detected.append(sub_array[i])
    detected_avg = sum(amp_detected)/len(amp_detected)
    deviation = 0
    for i in amp_detected:
        deviation+=(i-detected_avg)**2
    std = (deviation/len(amp_detected))**(1/2)

    return detected_avg, detected_avg+threshold*std,detected_avg-threshold*std


#以下開始判斷是否為尖端，左右斜率乘積為負。
def find_tip(idx_list,sub_array):
    true_up = []
    true_down = []
    for i in idx_list:
        left_slope = sub_array[i]-sub_array[i-1]
        right_slope = sub_array[i+1]-sub_array[i]
        if left_slope*right_slope < 0 :
            if left_slope > right_slope:
                true_up.append(i)
            else:
                true_down.append(i)
  #尖有可能朝上或下，將少的剔除
    if len(true_up) > len(true_down):
        tp = 'up'
        return true_up, tp 
    elif len(true_up) < len(true_down):
        tp = 'down'
        return true_down, tp
    else:
        up_dist = []
        down_dist = []
        env_avg = np.average(sub_array)
        for i in range(len(true_up)):
            up_dist.append(abs(sub_array[true_up[i]] - env_avg))
            down_dist.append(abs(sub_array[true_down[i]] - env_avg))

        if max(up_dist)>= max(down_dist):
            tp = 'up'
            return true_up, tp
        else:
            tp = 'down'
            return true_down, tp


# 過濾30MHz以內的點
def filter_in30(tip_susp,sub_array,tp,p2p_freq):
    dis = int(0.03/p2p_freq)

    sorted_tip = sorted(tip_susp)

    tip = []
    if len(sorted_tip) > 2:
        for i in range(len(sorted_tip)-1):


            if abs(sorted_tip[i]-sorted_tip[i+1])<=dis:
                if tp == 'up' :
                    if sub_array[sorted_tip[i]] > sub_array[sorted_tip[i+1]]:
                        tip.append(sorted_tip[i])
                    else:
                        tip.append(sorted_tip[i+1])
                elif tp == 'down' :
                    if sub_array[sorted_tip[i]] > sub_array[sorted_tip[i+1]]:
                        tip.append(sorted_tip[i+1])
                    else:
                        tip.append(sorted_tip[i])
                else:
                    tip.append(sorted_tip[i])
            else:
                tip.append(sorted_tip[i])
                if i == len(sorted_tip)-2:
                    tip.append(sorted_tip[i+1])
    else:
        tip = sorted_tip
  
    return sorted(tip)


def denoise(susp_list,freq,sub_array):
    #取出尖點，判斷尖點方向
    tip_susp,tp = find_tip(susp_list,sub_array)

    p2p_freq = (freq[-1]-freq[0])/freq.shape[0]
    #先刪除距離含30MHz內
    #依尖點方向判斷留大或小
    tip = filter_in30(tip_susp,sub_array,tp,p2p_freq)
    ori_len = len(tip)
    after_len = 0
    while (ori_len - after_len) !=0:
        after_tip = filter_in30(tip,sub_array,tp,p2p_freq)
        after_len = len(after_tip)
        if (ori_len - after_len) !=0 :
            ori_len = len(after_tip)
            after_len =0
        else:
            tip = after_tip
 
    return tip

  
# 求兩點間距離
def cal_distance(iq_1,iq_2):
    distance = ( (iq_1[0]-iq_2[0])**2 + (iq_1[1]-iq_2[1])**2 )**0.5
    return distance

def idx_exchanger(idx_list,target_array):
    retu_list = []
    for i in idx_list:
        retu_list.append(target_array[i])
    return retu_list
    

#以主群中心，找出最遠，並過濾出1.25倍背景標準差內的點
def find_farest(tip,nope_center,sub_array,IArray,QArray,FreqArray):
    def Key(elem):
        return elem[1]

    dist = []
    for i in tip:
        I = IArray[i]
        Q = QArray[i]
        dist.append([i,cal_distance([I,Q],nope_center)])

    dist.sort(key = Key)

    target_idx = []
    for i in dist :
        idx = i[0]
        target_idx.append(idx)

    target_idx = list(set(target_idx)) # delete repeat idx
    _, bg_ulimit, bg_dlimit = check_overpower(tip,sub_array,1.25)

  
    tip_avg, tip_ulimit, tip_dlimit = work_func(tip,sub_array,0.5)


  
    filtered = target_idx.copy()
    for i in target_idx:
        if bg_dlimit<=sub_array[i]<=bg_ulimit :
            filtered.remove(i)

  # idx to freq      
    target_freq = idx_exchanger(filtered,FreqArray)
    
    return target_freq


# kmeans 檢查答案正確度，用於計算Ec時
def final_check(terget_freq,sub,freq):
    freq = freq.reshape(-1,1)
    sub = sub.reshape(-1,1)
    label_k = k_fitter(freq,sub,k=2)
    true,_ = colect_cluster(label_k,'k')
    final_ans = []
    for i in true:
        for j in terget_freq:
            if freq[i] == j:
                final_ans.append(j)
  
    return sorted(final_ans,reverse=True)


# 給出Ec及狀態,
def cal_Ec_GHz(target_freq,sub,freq):
    sort_freq = sorted(target_freq,reverse = True)
    target_freq = final_check(sort_freq,sub,freq)

    if len(target_freq)>1 :
        if len(target_freq)>1:
            fq = target_freq[0]
            Ec = 2*(target_freq[0] - target_freq[1])
            status = 2

    
    else:
        if len(target_freq)==1 :
            fq = target_freq[0]
            Ec = 0
            status = 1

        else:
            fq = 0
            Ec = 0
            status = 0
    return fq, Ec, status, target_freq




def freq2idx(target_freq,freq):
    ret_out =[]
    for i in target_freq:
        ret_out.append(np.where(freq==i))

    return sorted(list(np.array(ret_out).reshape(len(ret_out))),reverse = True)


def Find_eps(inp_db):
    data = np.array(inp_db)
    neighbors = int(data.shape[0]*0.5)
    nbrs = NearestNeighbors(n_neighbors=neighbors ).fit(data)
    distances, indices = nbrs.kneighbors(data)
    distance_desc = sorted(distances[:,neighbors-1], reverse=True)
    

    kneedle = KneeLocator(range(1,len(distance_desc)+1),  #x values
                      distance_desc, # y values
                      S=1, #parameter suggested from paper
                      curve="convex", #parameter from figure
                      direction="decreasing") #parameter from figure
    eps = distance_desc[kneedle.elbow]*0.7
    return eps,neighbors

# find the nope center
def cal_nopecenter(nope_idx,I,Q):
    nope_center_i = []
    nope_center_q = []

    for i in nope_idx:
        nope_center_i.append(I[i])
        nope_center_q.append(Q[i])

    nope_center = [sum(nope_center_i)/len(nope_center_i),sum(nope_center_q)/len(nope_center_q)]
    return nope_center

# filter out rhe overpower case
def check_overpower(tip_denoised,sub_array,threshold):
    bg_idx = []
    for i in range(sub_array.shape[0]):
        bg_idx.append(i)
    for i in list(set(tip_denoised)): 
        bg_idx.remove(i)

    bg_avg, bg_ulimit, bg_dlimit = work_func(bg_idx,sub_array,threshold)
    max_min_avg = 0.5*(np.max(sub_array)+np.min(sub_array))

    if bg_dlimit <= max_min_avg <= bg_ulimit :
        mode = 'overpower'
    else:
        mode = 'safe'
    
    return mode, bg_ulimit, bg_dlimit


# 0820 update

def freq_sorter(y,group):
    
    groupTOsort = [] 
    avg = []
    for g in list(set(group)):
        indices = [i for i, x in enumerate(group) if x == g]
        group_temp = []
        for idx in indices:
            group_temp.append(y[idx])
        if group != [0,0]:
            avg.extend([np.mean(group_temp)])
            groupTOsort.extend([group_temp])
        else:
            groupTOsort.extend([group_temp])
    if len(avg) != 0:
        freq_group = {}    
        sorted_avg = sorted(avg,reverse=True)
        for i in range(len(sorted_avg)):
            if i == 0:
                freq_group['high'] = np.array(groupTOsort[avg.index(sorted_avg[i])])
            elif i == 1:
                freq_group['mid'] = np.array(groupTOsort[avg.index(sorted_avg[i])])
            else:
                freq_group['low'] = np.array(groupTOsort[avg.index(sorted_avg[i])])

        return freq_group
    
    else:
        return {'high':np.array(groupTOsort),'mid':np.array([]),'low':np.array([])}

def rm_empty(ary):
    ret = []
    for i in ary:
        if np.array(i).size != 0:
            ret.append(i)
    return np.array(list(set(ret)))
# !!!Warning!!! Important~
def freq_clustering(x,y):
    if y.shape[0] == 3:
        swit = 0
        for i in range(y.shape[0]):
            if i != y.shape[0]:
                for j in range(i+1,y.shape[0],1):
                    if abs(y[i]-y[j])<=0.05:
                        swit +=1
    
        if  swit != 0:                         
            group = list(k_fitter(x.reshape(-1,1),y.reshape(-1,1),2,ini_center ='k-means++'))

        else:
            init()
            print(Style.BRIGHT+Fore.RED+'Warning! DB-scan somewhere maybe goes wrong check it plz!'+Style.RESET_ALL)
            group = list(k_fitter(x.reshape(-1,1),y.reshape(-1,1),3,ini_center ='k-means++'))

    elif 2 == y.shape[0]:
        if abs(y[1] - y[0]) < 0.05:     # two frequency distance < 50MHz treat as same group
            group = [0,0]
        else:
            init()
            print(Style.BRIGHT+Fore.RED+'Warning! DB-scan somewhere maybe goes wrong check it plz!'+Style.RESET_ALL)
            group = list(k_fitter(x.reshape(-1,1),y.reshape(-1,1),2,ini_center ='k-means++'))

    else:
        group = list(k_fitter(x.reshape(-1,1),y.reshape(-1,1),3,ini_center ='k-means++')) 
        
    return group

def check_acStark_power(powa_status,fqS,high_freq_group):  #inputs dict, dict, array
    only_one_powa = []
    for status_key in powa_status.keys():
        if powa_status[status_key] == 1:
            only_one_powa.append(status_key)
    acStark_power = []
    for powa in only_one_powa:
        if fqS[powa][0] in high_freq_group:
            acStark_power.append(int(powa))
    return np.array(acStark_power)
 



class Db_Scan:

    def __init__(self,dataframe):#,Ec,status,area_Maxratio,density
        self.dataframe = dataframe

        self.fq = 0.0
        self.Ec = 0.0
        self.freq = 0.0
        self.status = 0
        self.target_freq = []
        self.sub = []
        self.title = ''
        self.answer = {} # <- 0630 update
        self.plot_items = {}



    def do_analysis(self):
        self.freq = self.dataframe['Frequency'].to_numpy()  #for qubit  <b>XY-Frequency(GHz)</b>
        I = self.dataframe['I'].to_numpy()
        Q = self.dataframe['Q'].to_numpy()

        inp_db = []
        for i in range(I.shape[0]):
            inp_db.append(list(hstack(([I[i]],[Q[i]]))))

        # start DBSCAN
        eps,min_samples = Find_eps(inp_db)
        labels_db = dbscan(array(inp_db),eps,min_samples)

        # output process
        peak_susp_idx, nope_idx = colect_cluster(labels_db,mode='db')
        nope_center = cal_nopecenter(nope_idx,I,Q)

        # redefine the background
        redef_sub = []
        for i in range(self.freq.shape[0]):
            redef_sub.append(cal_distance([I[i],Q[i]],nope_center))

        self.sub = array(redef_sub)
        self.title = 'Amplitude_Redefined'


        if len(peak_susp_idx) != 0:

            tip = denoise(peak_susp_idx,self.freq,self.sub)
            #filter out the overpower case within +-0.5 std
            overpower,_,_ = check_overpower(tip,self.sub,0.5)

            if overpower == 'safe':
                #farest 3 point in IQ
                denoised_freq = find_farest(tip,nope_center,self.sub,I,Q,self.freq)

                #calculate Ec based on farest
                self.fq, self.Ec, self.status, self.target_freq = cal_Ec_GHz(denoised_freq,self.sub,self.freq)
            else:
                self.fq, self.Ec, self.status, self.target_freq = 0, 0, 0, []
        else:
            self.fq, self.Ec, self.status, self.target_freq = 0, 0, 0, []

        self.answer = {'Fq':self.fq,'Ec':self.Ec,'Status':self.status,'Freqs':self.target_freq} 
        '''status = 0 for 0 peak detected -> overpower with high probability
           status = 1 for 1 peak detected -> so far, a stronger xy-power again
           status = 2 for 2 peak detected'''
        return self.answer
                                                                                         
    def give_result(self):
        farest = freq2idx(self.target_freq,self.freq)[:3]
        self.plot_items = {
            'Targets':self.sub[farest],
            'Targets_Freq':self.freq[farest],
            'Sub_Frequency':self.freq,
            'Substrate':self.sub
        }