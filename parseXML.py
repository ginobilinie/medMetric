import os
import numpy as np
import SimpleITK as sitk
import scipy.io as scio
import surface_distance
import shlex, subprocess
import time
from xml.etree import ElementTree

def parseAXml(filename):
    dsc = 0
    hd = 0
    asd = 0
    with open(filename, 'rt') as f:
        tree = ElementTree.parse(f)  
        for node in tree.iter('DICE'):  
            value = node.attrib.get('value')
            dsc = float(value)
        for node in tree.iter('HDRFDST'):  
            value = node.attrib.get('value')
            hd = float(value)
        for node in tree.iter('AVGDIST'):  
            value = node.attrib.get('value')
            asd = float(value)
    res = [dsc, hd, asd]
    return res

def main():
    basePath = '/netscr/liwa/iSeg/'
    basePath = '/home/dongnie/warehouse/iSeg/evaluationTestSet/'
    basePath = '/shenlab/lab_stor5/dongnie/iSeg/evaluationTestSet/data/'
    gtPath = basePath + 'Ground_truth'
    prePath = basePath + 'Top8'

    usingPythonLib = 0
    basexmlName = "res_sub11_Bern_IPMI_csf.xml"

    #ids=[1,2,3,4,5,6,7,8,9,10,11] 
    N = 13 # # of subjects
    M = 8 # # of teams
    R = 84 # # of ROIs, 83 ROI + one bg
    
    dscMat = np.zeros([N,M,3])
    hdMat = np.zeros([N,M,3])
    asdMat = np.zeros([N,M,3])
    ids=[11,12,13,14,15,16,17,18,19,20,21,22,23]
    #files=os.listdir([datapath,'*.hdr']) 
    subDirs = ['MSL_SKKU','LIVIA','Bern_IPMI','Tu_Image','UPF_simbiosys','NeuroMTL','UPC_DLMI', 'LRDE']
    tissues = ['wm', 'gm', 'csf']
    for i in range(0, len(ids)):
        ind=ids[i]    
        print 'now come to subject: ', ind
        teamInd = 0
        for subDir in subDirs: # for each team
            tissueInd = 0
            for tissue in tissues:
                xmlName = basexmlName.replace('11', str(ind))
                xmlName = xmlName.replace('Bern_IPMI', subDir)
                xmlName = xmlName.replace('csf', tissue)
                res = parseAXml(xmlName)
                print res
                dscMat[i, teamInd, tissueInd] = res[0]
                hdMat[i, teamInd, tissueInd] = res[1]
                asdMat[i, teamInd, tissueInd] = res[2]  
                tissueInd = tissueInd + 1
            teamInd = teamInd + 1

    np.save('dsc4ISeg.npy', dscMat)
    np.save('hd4ISeg.npy', hdMat)
    np.save('asd4ISeg.npy', asdMat)
if __name__ == '__main__':     
    main()