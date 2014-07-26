import numpy as np
import os
import matplotlib.pyplot as plt


def sigmaz(results, sigma=2):
    return (results[abs(results-results.mean())/results.std() < sigma])


def do(folder):
    all = os.listdir(folder)
    files = [i for i in all if 'csv' in i]
    print files
    tmp = []
    for file in files:
        try:
            array = np.loadtxt(str(folder)+'/'+str(file))
            tmp.append(array)
        except:
            continue
    res = np.hstack(tmp)
    res = sigmaz(res, 2)
    print res.mean()
    print res.std()
    return res.mean(), res.std()/np.sqrt(len(res))


def get_folders():
    folders = []
    for i, j, k in os.walk('./'):
        if './.' not in i and len(i) > 2:
            folders.append(i)
    return folders


def plot_results(folders):
    fig, ax = plt.subplots()
    for folder in folders:
        ax.errorbar(int(folder[2:]), do(folder)[0],
                    yerr=do(folder)[1], fmt='o-')
    ax.set_title(os.getcwd().split('/')[-1])
    ax.set_xlabel('dose')
    ax.set_ylabel('radius (nm)')
    fig.show()
    raw_input('close..')


if __name__ == "__main__":
    folders = get_folders()
    plot_results(folders)
