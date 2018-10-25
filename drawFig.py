'''
    Target: draw box-plot for each metric (each tissue type) based on different subjects' performance
    Dong Nie Sep, 2018
'''
import matplotlib.pyplot as plt
import numpy as np

## reference: https://matplotlib.org/examples/pylab_examples/boxplot_demo.html

def main():
    diceFN = 'dsc4ISeg.npy'
    hdFN = 'hd4ISeg.npy'
    asdFN = 'asd4ISeg.npy'
    
    # NxMx3
    dscMat = np.load(diceFN)
    hdMat = np.load(hdFN)
    asdMat = np.load(asdFN)
    # for dsc
    # for white matter
    plt.figure()
    plt.boxplot(np.transpose(dscMat[:,:,0],(1,0)))
    plt.show()
    # for grey matter
    plt.figure()
    plt.boxplot(np.transpose(dscMat[:,:,1],(1,0)))
    plt.show()
    # for grey matter
    plt.figure()
    plt.boxplot(np.transpose(dscMat[:,:,2],(1,0)))
    plt.show()
    
    # for hd
    # for white matter
    plt.figure()
    plt.boxplot(np.transpose(hdMat[:,:,0],(1,0)))
    plt.show()
    # for grey matter
    plt.figure()
    plt.boxplot(np.transpose(hdMat[:,:,1],(1,0)))
    plt.show()
    # for grey matter
    plt.figure()
    plt.boxplot(np.transpose(hdMat[:,:,2],(1,0)))
    plt.show()
    
    
    # for asd
    # for white matter
    plt.figure()
    plt.boxplot(np.transpose(asdMat[:,:,0],(1,0)))
    plt.show()
    # for grey matter
    plt.figure()
    plt.boxplot(np.transpose(asdMat[:,:,1],(1,0)))
    plt.show()
    # for grey matter
    plt.figure()
    plt.boxplot(np.transpose(asdMat[:,:,2],(1,0)))
    plt.show()


if __name__ == '__main__':     
    main()
