'''
    Target: evaluate the Dice for white matter, grey matter and CSF for N subjects with M methods
    Dong Nie @ Sep, 2017; Sep, 2018
'''
import os
import numpy as np
import SimpleITK as sitk
import scipy.io as scio
import surface_distance
import shlex, subprocess
import time
#this function is used to compute the dice ratio
def dice(im1, im2,tid):
    eps = 1e-7
    im1=im1==tid #make it boolean
    im2=im2==tid #make it boolean
    im1=np.asarray(im1).astype(np.bool)
    im2=np.asarray(im2).astype(np.bool)

    if im1.shape != im2.shape:
        raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")
    # Compute Dice coefficient
    intersection = np.logical_and(im1, im2)
    dsc=2. * intersection.sum() / (im1.sum() + im2.sum()+eps)
    return dsc

# compute hausdorff distance (hd), using python library
def computeHD(gtMat, preMat, ind, percent=95, spacing = (1,1,1)):
    if ind != -1:
        indices = np.where(gtMat==ind) #here, inds is a tuple which contains i,j,k
        gtMask = np.zeros(gtMat.shape, np.uint8)
        gtMask[indices] = 1 #successfully convert some specififc value
        
        indices = np.where(preMat==ind) #here, inds is a tuple which contains i,j,k
        preMask = np.zeros(preMat.shape, np.uint8)
        preMask[indices] = 1 #successfully convert some specififc value
    else:
        gtMask = gtMat
        preMask = gtMat
    surface_distances = surface_distance.compute_surface_distances(gtMask, preMask, spacing_mm=spacing)
    res = surface_distance.compute_robust_hausdorff(surface_distances, percent)
    return res

# compute average surface distance (asd), using python library
def computeASD(gtMat, preMat, ind, spacing = (1,1,1)):
    if ind != -1:
        indices = np.where(gtMat==ind) #here, inds is a tuple which contains i,j,k
        gtMask = np.zeros(gtMat.shape, np.uint8)
        gtMask[indices] = 1 #successfully convert some specififc value
        
        indices = np.where(preMat==ind) #here, inds is a tuple which contains i,j,k
        preMask = np.zeros(preMat.shape, np.uint8)
        preMask[indices] = 1 #successfully convert some specififc value
    else:
        gtMask = gtMat
        preMask = gtMat
    surface_distances = surface_distance.compute_surface_distances(gtMask, preMask, spacing_mm=spacing)
    res = surface_distance.compute_average_surface_distance(surface_distances)
    return res

# compute hausdorff distance (hd), using c++ library
def computeMetrics(gtMat, preMat, ind, cmdline, gtFN, preFN):
    if ind != -1:
        indices = np.where(gtMat==ind) #here, inds is a tuple which contains i,j,k
        gtMask = np.zeros(gtMat.shape, np.uint8)
        gtMask[indices] = 1 #successfully convert some specififc value
        
        indices = np.where(preMat==ind) #here, inds is a tuple which contains i,j,k
        preMask = np.zeros(preMat.shape, np.uint8)
        preMask[indices] = 1 #successfully convert some specififc value
    else:
        gtMask = gtMat
        preMask = gtMat
    volOut=sitk.GetImageFromArray(gtMask)
    sitk.WriteImage(volOut,gtFN)
    time.sleep(5)
    volSeg=sitk.GetImageFromArray(preMask)
    sitk.WriteImage(volSeg,preFN)
    time.sleep(5)
    args = shlex.split(cmdline)
    #print args
    p = subprocess.Popen(args)
    time.sleep(10)
    return p


def main():
    basePath = '/netscr/liwa/iSeg/'
    basePath = '/home/dongnie/warehouse/iSeg/evaluationTestSet/'
    basePath = '/shenlab/lab_stor5/dongnie/iSeg/evaluationTestSet/data/'
    gtPath = basePath + 'Ground_truth'
    prePath = basePath + 'Top8'

    usingPythonLib = 0
    basecmdline = "./EvaluateSegmentation  data/Ground_truth/subject-11-label.hdr data/Top8/method1/subject-11-label.hdr -use DICE,HDRFDST@0.95@,AVGDIST -xml res_sub11_method1_csf.xml"

    #ids=[1,2,3,4,5,6,7,8,9,10,11] 
    N = 13 # # of subjects
    M = 8 # # of teams
    R = 84 # # of ROIs, 83 ROI + one bg
    
    dscMat = np.zeros([N,M,4])
    hdMat = np.zeros([N,M,3])
    asdMat = np.zeros([N,M,3])
    ids=[11,12,13,14,15,16,17,18,19,20,21,22,23]
    #files=os.listdir([datapath,'*.hdr']) 
    subDirs = ['method1','method2','method3','method4','method5','method6','method7', 'method8']
    for i in range(0, len(ids)):
        ind=ids[i]    
        gtLabelfilename = 'subject-%d-label.hdr'%ind #provide a sample name of your filename of data here
        gtROIfilename = 'subject-%d-ROI.hdr'%ind #provide a sample name of your filename of data here
        gtLabelfn = os.path.join(gtPath,gtLabelfilename)
        gtROIfn = os.path.join(gtPath,gtROIfilename)
        imgT1Org = sitk.ReadImage(gtLabelfn)
        gtLabel = sitk.GetArrayFromImage(imgT1Org)
        imgT2Org = sitk.ReadImage(gtROIfn)
        gtROI = sitk.GetArrayFromImage(imgT2Org)
        gtLabel[gtLabel>200]=3 #white matter
        gtLabel[gtLabel>100]=2 #gray matter
        gtLabel[gtLabel>4]=1 #csf
        print 'now come to subject: ', ind
        teamInd = 0

        for subDir in subDirs: # for each team
            preLabelfilename = 'subject-%d-label.hdr'%ind  # provide a sample name of your filename of ground truth here
            preLabelfn = os.path.join(prePath, subDir, preLabelfilename)
            labelOrg = sitk.ReadImage(preLabelfn)
            preLabel = sitk.GetArrayFromImage(labelOrg)
            preLabel[preLabel>200]=3 #white matter
            preLabel[preLabel>100]=2 #gray matter
            preLabel[preLabel>4]=1 #csf
            
            if usingPythonLib: #using python library
                bgDice = dice(gtLabel,preLabel,0)   
                wmDice = dice(gtLabel,preLabel,1)
                gmDice = dice(gtLabel,preLabel,2)
                csfDice = dice(gtLabel,preLabel,3)  
                dscMat[i,teamInd,:] = [bgDice, wmDice, gmDice, csfDice]
                print 'now come to team: ', subDir, ' Dice: ',bgDice, ' ',wmDice,' ',gmDice,' ',csfDice
                
                wmHD = computeHD(gtLabel, preLabel, 1)
                gmHD = computeHD(gtLabel, preLabel, 2)
                csfHD = computeHD(gtLabel, preLabel, 3)
                wholeHD = computeHD(gtLabel, preLabel, -1)
                hdMat[i,teamInd,:] = [wmHD, gmHD, csfHD]
                print 'now come to team: ', subDir, ' 95HD: ',wmHD,' ',gmHD,' ',csfHD,' wholeHD: ', wholeHD
                
                wmASD = computeASD(gtLabel, preLabel, 1)
                gmASD = computeASD(gtLabel, preLabel, 2)
                csfASD = computeASD(gtLabel, preLabel, 3)
                wholeASD = computeASD(gtLabel, preLabel, -1)
                asdMat[i,teamInd,:] = [np.mean(wmASD), np.mean(gmASD), np.mean(csfASD)]
                print 'now come to team: ', subDir, ' ASD: ',wmASD,' ',gmASD,' ',csfASD,' wholeASD: ',wholeASD
                np.save('dsc4ISeg.npy', dscMat)
                np.save('hd4ISeg.npy', hdMat)
                np.save('asd4ISeg.npy', asdMat)
            else: #using C++ library
                cmdline = basecmdline.replace('11', str(ind))
                cmdline = cmdline.replace('Bern_IPMI', subDir)
                cmdline = cmdline.replace('csf', 'wm')
                gtFN = 'sub'+str(ind)+'_wm.nii.gz'
                preFN = 'sub'+str(ind)+'_'+subDir+'_wm.nii.gz'
                p = computeMetrics(gtLabel, preLabel, 1, cmdline, gtFN, preFN)
                
                cmdline = basecmdline.replace('11', str(ind))
                cmdline = cmdline.replace('Bern_IPMI', subDir)
                cmdline = cmdline.replace('csf', 'gm')
                gtFN = 'sub'+str(ind)+'_gm.nii.gz'
                preFN = 'sub'+str(ind)+'_'+subDir+'_gm.nii.gz'
                p = computeMetrics(gtLabel, preLabel, 2, cmdline, gtFN, preFN)
                
                cmdline = basecmdline.replace('11', str(ind))
                cmdline = cmdline.replace('Bern_IPMI', subDir)
                cmdline = cmdline.replace('csf', 'csf')
                gtFN = 'sub'+str(ind)+'_csf.nii.gz'
                preFN = 'sub'+str(ind)+'_'+subDir+'_csf.nii.gz'
                p = computeMetrics(gtLabel, preLabel, 3, cmdline, gtFN, preFN)
#             allROIs = np.unique(gtROI)
#             print 'ROIs is: ',allROIs
#             for uniROI in allROIs: # for each ROI
#                 indices = np.where(gtROI==uniROI) #here, inds is a tuple which contains i,j,k
#                 gtMat = np.zeros(gtROI.shape)
#                 gtMat[indices] = gtLabel[indices] #successfully convert some specififc value
#                 preMat = np.zeros(gtROI.shape)
#                 preMat[indices] = preLabel[indices] #successfully convert some specififc value
#                 bgDice = dice(gtMat,preMat,0)   
#                 wmDice = dice(gtMat,preMat,1)
#                 gmDice = dice(gtMat,preMat,2)
#                 csfDice = dice(gtMat,preMat,3)   
#                 print 'ROI ', uniROI,' : ',bgDice, ' ',wmDice,' ',gmDice,' ',csfDice   
#                 scoreMat[i,teamInd, uniROI, :] = [bgDice, wmDice, gmDice, csfDice]  
#             teamInd = teamInd + 1    
#     np.savetxt('scoreMat.out', scoreMat, fmt='%1.4f')

if __name__ == '__main__':     
    main()
