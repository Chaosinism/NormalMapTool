import numpy as np
from scipy.optimize import minimize
import imageio
import sys

ULength = 0
VLength = 0
Scale = 1
MAXITER = 100

NormalArray = np.array([])
MaskArray = np.array([])

# read inputs
if len(sys.argv)>1:
    MAXITER = int(sys.argv[1])

if len(sys.argv)>2:
    NormalArray = imageio.imread(sys.argv[2])
    NormalArray = np.array(NormalArray,dtype=np.float32)
    NormalArray = NormalArray-127

if len(sys.argv)>3:
    MaskArray = imageio.imread(sys.argv[3])
    MaskArray = MaskArray[:,:,0]>127
elif NormalArray.shape[2]>3:
    MaskArray = NormalArray[:,:,3]>0
else:
    MaskArray = NormalArray[:,:,0]>-65535

VLength=NormalArray.shape[0]
ULength=NormalArray.shape[1]


def EnergyCost(x):
    global ULength, VLength, Scale
    HeightArray = np.reshape(x,[VLength,ULength]) / 255.0
    # calculate tangents
    VDiff = HeightArray.copy()
    VDiff[1:,:] = np.diff(HeightArray,axis=0)*Scale
    UDiff = HeightArray.copy()
    UDiff[:,1:] = np.diff(HeightArray,axis=1)*Scale

    E0 = (NormalArray[:,:,0] + UDiff*NormalArray[:,:,2]) / 255.0
    E1 = (NormalArray[:,:,1] - VDiff*NormalArray[:,:,2]) / 255.0
    E = (E0*E0+E1*E1)*MaskArray
    print('Energy: '+str(E.sum()))
    return E.sum()

def EnergyGradient(x):
    global ULength, VLength, Scale
    HeightArray = np.reshape(x,[VLength,ULength]) / 255.0
    # calculate tangents
    VDiff = HeightArray.copy()
    VDiff[1:,:] = np.diff(HeightArray,axis=0)*Scale
    UDiff = HeightArray.copy()
    UDiff[:,1:] = np.diff(HeightArray,axis=1)*Scale
    # terms of the gradient
    g0 = 2* (NormalArray[:,:,0] + UDiff*NormalArray[:,:,2]) * NormalArray[:,:,2]
    g0[:,:-1] = g0[:,:-1] - g0[:,1:]
    g1 = -2* (NormalArray[:,:,1] - VDiff*NormalArray[:,:,2]) * NormalArray[:,:,2]
    g1[:-1,:] = g1[:-1,:] - g1[1:,:]
    g = (g0+g1) / 65025.0 * MaskArray

    return np.reshape(g,ULength*VLength)

x0 = np.random.rand(ULength*VLength)*255
opt = minimize(EnergyCost, x0, jac=EnergyGradient, method='L-BFGS-B', options={'maxiter': MAXITER})

HeightArray = np.reshape(opt.x,[VLength,ULength])
LB=HeightArray.min()
UB=HeightArray.max()
HeightArray = (HeightArray-LB)/(UB-LB)*255*MaskArray

imageio.imwrite('HeightMap.png',HeightArray)