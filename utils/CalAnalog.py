import numpy as np

def find_nearest_ens_index(hist_array):
    try:
        return np.nanargmin(hist_array, axis = 1)
    except:
        return np.argmin(hist_array, axis = 1)


def find_n_ens_index(hist_array, n_ensemble):
    search_array = np.copy(hist_array)
    Anal_index = np.empty([len(hist_array),n_ensemble],dtype = np.int)
    
    col = 0
    while n_ensemble > col:
        index = find_nearest_ens_index(search_array)
        for i in np.arange(len(hist_array)):
            Anal_index[i,col] = index[i]
            search_array[i,index[i]] = np.nan # replace value
        col +=1
    return Anal_index

def find_n_ens(hist_array,n_ensemble, estimate_ens):
    if hist_array.shape[1] > n_ensemble:
        Anal_index = find_n_ens_index(hist_array,n_ensemble)
        rows = len(Anal_index)
        Anal_ens = np.empty([rows,n_ensemble],dtype = np.float)
        for i in range(rows):
            for k in range(n_ensemble):
                index = Anal_index[i,k]
                Anal_ens[i,k] = estimate_ens[i,index]
        return Anal_ens
    else:
        return estimate_ens
        
def GetAnalog(ens_no,model_now,model_past,obs_past):

    diff = np.absolute(model_past - model_now)
    est = model_past - obs_past

    Anal_ens = find_n_ens(diff,ens_no,est)


    return Anal_ens

if __name__ == '__main__':
    array = np.array([[1,2,3],[5,4,6],[7,8,9]],dtype = np.float)
    y_axis = np.arange(len(array)).reshape(len(array),1)
    #print(find_n_ens_index(array,2))
    print(find_n_ens_index(array,2))
    print(np.mean(array,axis = 1))