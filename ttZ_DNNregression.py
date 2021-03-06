import os, sys
import numpy as np
import tensorflow as tf
from DNN_tensorflow_class_py2 import EarlyStopping, DNN
from ROOT import TFile, TTree, TCut, TH1F
from root_numpy import fill_hist
from root_numpy import root2array, tree2array, array2root, array2tree
from root_numpy import testdata
from sklearn.model_selection import train_test_split
from c0_READ_PATH_FILE_ROOT import read_file_name_root

model = DNN(n_in=29, n_hiddens=[150,150,150,150,150,150,150,150,150,150], n_out=1)
MEM = True #FIXME 'False' for KIN
epochs = 1000
earlyStop = 70
batch_size = 50
Date=20181005          #TODO FIXME
Layer_NUM= 10              #TODO FIXME
Node_on_Each_layer=150   #TODO FIXME
#model_name = "ttZ_tensor"
N_train = 2000000
Model_name = str(Date)+"_"+"TrainENum"+str(N_train)+"/"+"LayerNum_"+str(Layer_NUM)+"+"+"Node_"+str(Node_on_Each_layer)+"+"+"BatchSize_"+str(batch_size)
Make_dir = "mkdir -p "+ "tens_model_reg/"+Model_name
os.system(Make_dir)
model_name = Model_name +"/"+ "ttZ_Reg"

data = TFile.Open('ttZ_input/DNN_ttZ.root')
#data = TFile.Open('ttZ_input/out_ttz_250k.root')
tree = data.Get('Tree')

####################################### Input DATA Sets !!!!! 
reco_bj1_Energy_    = tree2array(tree, branches='multilepton_Bjet1_P4->Energy()')
reco_bj1_Theta_     = tree2array(tree, branches='multilepton_Bjet1_P4->Theta()')
reco_bj1_Phi_       = tree2array(tree, branches='multilepton_Bjet1_P4->Phi()')
reco_bj2_Energy_    = tree2array(tree, branches='multilepton_Bjet2_P4->Energy()')
reco_bj2_Theta_     = tree2array(tree, branches='multilepton_Bjet2_P4->Theta()')
reco_bj2_Phi_       = tree2array(tree, branches='multilepton_Bjet2_P4->Phi()')
reco_MW1_Energy_    = tree2array(tree, branches='multilepton_JetClosestMw1_P4->Energy()')
reco_MW1_Theta_     = tree2array(tree, branches='multilepton_JetClosestMw1_P4->Theta()')
reco_MW1_Phi_       = tree2array(tree, branches='multilepton_JetClosestMw1_P4->Phi()')
reco_MW2_Energy_    = tree2array(tree, branches='multilepton_JetClosestMw2_P4->Energy()')
reco_MW2_Theta_     = tree2array(tree, branches='multilepton_JetClosestMw2_P4->Theta()')
reco_MW2_Phi_       = tree2array(tree, branches='multilepton_JetClosestMw2_P4->Phi()')
reco_l1_Energy_     = tree2array(tree, branches='multilepton_Lepton1_P4->Energy()')
reco_l1_Theta_      = tree2array(tree, branches='multilepton_Lepton1_P4->Theta()')
reco_l1_Phi_        = tree2array(tree, branches='multilepton_Lepton1_P4->Phi()')
reco_l2_Energy_     = tree2array(tree, branches='multilepton_Lepton2_P4->Energy()')
reco_l2_Theta_      = tree2array(tree, branches='multilepton_Lepton2_P4->Theta()')
reco_l2_Phi_        = tree2array(tree, branches='multilepton_Lepton2_P4->Phi()')
reco_l3_Energy_     = tree2array(tree, branches='multilepton_Lepton3_P4->Energy()')
reco_l3_Theta_      = tree2array(tree, branches='multilepton_Lepton3_P4->Theta()')
reco_l3_Phi_        = tree2array(tree, branches='multilepton_Lepton3_P4->Phi()')
reco_mET_Pt_        = tree2array(tree, branches='multilepton_mET->Pt()')
reco_mET_Phi_       = tree2array(tree, branches='multilepton_mET->Phi()')
mHT_            = tree2array(tree, branches='multilepton_mHT')

Gen_BjetTopHad_E_       = tree2array(tree, branches='Gen_BjetTopHad_E')
Gen_WTopHad_mW_     = tree2array(tree, branches='Gen_WTopHad_mW')
Gen_BjetTopLep_E_       = tree2array(tree, branches='Gen_BjetTopLep_E')
Gen_NeutTopLep_Phi_     = tree2array(tree, branches='Gen_NeutTopLep_Phi')
Gen_WTopLep_mW_     = tree2array(tree, branches='Gen_WTopLep_mW')
Kin_BjetTopHad_E_       = tree2array(tree, branches='Kin_BjetTopHad_E')
Kin_WTopHad_mW_     = tree2array(tree, branches='Kin_WTopHad_mW')
Kin_BjetTopLep_E_       = tree2array(tree, branches='Kin_BjetTopLep_E')
Kin_NeutTopLep_Phi_     = tree2array(tree, branches='Kin_NeutTopLep_Phi')
Kin_WTopLep_mW_     = tree2array(tree, branches='Kin_WTopLep_mW')
###############################################################################################################

##################################### Target DATA !!!!!
mc_mem_ttz_weight_evalgenmax_log = tree2array(tree, branches='mc_mem_ttz_weight_evalgenmax_log')
mc_kin_ttz_weight_logmax = tree2array(tree, branches='mc_kin_ttz_weight_logmax')
###############################################################################################################

##################################### MEM/KIN's Valid events !!!!!
if(MEM == True):
    I1 = 0
    for i1 in range(mc_mem_ttz_weight_evalgenmax_log.size):
        if(mc_mem_ttz_weight_evalgenmax_log[i1] > -600):
            I1 = I1 + 1
    print("MEM's Total event number is : ", mc_mem_ttz_weight_evalgenmax_log.size)
    print("MEM's Valid event number is : ",  I1)
    num_Valid = np.zeros(I1)
    I2 = 0
    for i2 in range(mc_mem_ttz_weight_evalgenmax_log.size):
        if(mc_mem_ttz_weight_evalgenmax_log[i2] > -600):
            num_Valid[I2] = i2
            I2 = I2 + 1
elif(MEM == False):
    I1 = 0
    for i1 in range(mc_kin_ttz_weight_logmax.size):
            if(mc_kin_ttz_weight_logmax[i1] > -600):
                    I1 = I1 + 1
    print("KIN's Total event number is : ", mc_kin_ttz_weight_logmax.size)
    print("KIN's Valid event number is : ",  I1)
    num_Valid = np.zeros(I1)
    I2 = 0
    for i2 in range(mc_kin_ttz_weight_logmax.size):
            if(mc_kin_ttz_weight_logmax[i2] > -600):
                    num_Valid[I2] = i2
                    I2 = I2 + 1
else:
    raise SystemExit
###############################################################################################################

reco_bj1_Energy = np.zeros(I2)
reco_bj1_Theta  = np.zeros(I2)
reco_bj1_Phi    = np.zeros(I2)
reco_bj2_Energy = np.zeros(I2)
reco_bj2_Theta  = np.zeros(I2)
reco_bj2_Phi    = np.zeros(I2)
reco_MW1_Energy = np.zeros(I2)
reco_MW1_Theta  = np.zeros(I2)
reco_MW1_Phi    = np.zeros(I2)
reco_MW2_Energy = np.zeros(I2)
reco_MW2_Theta  = np.zeros(I2)
reco_MW2_Phi    = np.zeros(I2)
reco_l1_Energy  = np.zeros(I2)
reco_l1_Theta   = np.zeros(I2)
reco_l1_Phi = np.zeros(I2)
reco_l2_Energy  = np.zeros(I2)
reco_l2_Theta   = np.zeros(I2)
reco_l2_Phi = np.zeros(I2)
reco_l3_Energy  = np.zeros(I2)
reco_l3_Theta   = np.zeros(I2)
reco_l3_Phi = np.zeros(I2)
reco_mET_Pt = np.zeros(I2)
reco_mET_Phi    = np.zeros(I2)
mHT     = np.zeros(I2)
Gen_BjetTopHad_E    = np.zeros(I2)
Gen_WTopHad_mW      = np.zeros(I2)
Gen_BjetTopLep_E    = np.zeros(I2)
Gen_NeutTopLep_Phi  = np.zeros(I2)
Gen_WTopLep_mW  = np.zeros(I2)
Kin_BjetTopHad_E    = np.zeros(I2)
Kin_WTopHad_mW      = np.zeros(I2)
Kin_BjetTopLep_E    = np.zeros(I2)
Kin_NeutTopLep_Phi  = np.zeros(I2)
Kin_WTopLep_mW  = np.zeros(I2)
TARGET  = np.zeros(I2)
for j1 in range(reco_bj1_Energy.size):
    jj1 = int(num_Valid[j1])
    reco_bj1_Energy[j1] = reco_bj1_Energy_[jj1]
    reco_bj1_Theta[j1]  = reco_bj1_Theta_[jj1]
    reco_bj1_Phi[j1]    = reco_bj1_Phi_[jj1]
    reco_bj2_Energy[j1] = reco_bj2_Energy_[jj1]
    reco_bj2_Theta[j1]  = reco_bj2_Theta_[jj1]
    reco_bj2_Phi[j1]    = reco_bj2_Phi_[jj1]
    reco_MW1_Energy[j1] = reco_MW1_Energy_[jj1]
    reco_MW1_Theta[j1]  = reco_MW1_Theta_[jj1]
    reco_MW1_Phi[j1]    = reco_MW1_Phi_[jj1]
    reco_MW2_Energy[j1] = reco_MW2_Energy_[jj1]
    reco_MW2_Theta[j1]  = reco_MW2_Theta_[jj1]
    reco_MW2_Phi[j1]    = reco_MW2_Phi_[jj1]
    reco_l1_Energy[j1]  = reco_l1_Energy_[jj1]
    reco_l1_Theta[j1]   = reco_l1_Theta_[jj1]
    reco_l1_Phi[j1]     = reco_l1_Phi_[jj1]
    reco_l2_Energy[j1]  = reco_l2_Energy_[jj1]
    reco_l2_Theta[j1]   = reco_l2_Theta_[jj1]
    reco_l2_Phi[j1]     = reco_l2_Phi_[jj1]
    reco_l3_Energy[j1]  = reco_l3_Energy_[jj1]
    reco_l3_Theta[j1]   = reco_l3_Theta_[jj1]
    reco_l3_Phi[j1]     = reco_l3_Phi_[jj1]
    reco_mET_Pt[j1]     = reco_mET_Pt_[jj1]
    reco_mET_Phi[j1]    = reco_mET_Phi_[jj1]
    mHT[j1]         = mHT_[jj1]
    Gen_BjetTopHad_E[j1]        = Gen_BjetTopHad_E_[jj1]
    Gen_WTopHad_mW[j1]          = Gen_WTopHad_mW_[jj1]
    Gen_BjetTopLep_E[j1]        = Gen_BjetTopLep_E_[jj1]
    Gen_NeutTopLep_Phi[j1]      = Gen_NeutTopLep_Phi_[jj1]
    Gen_WTopLep_mW[j1]          = Gen_WTopLep_mW_[jj1]
    Kin_BjetTopHad_E[j1]        = Kin_BjetTopHad_E_[jj1]
    Kin_WTopHad_mW[j1]          = Kin_WTopHad_mW_[jj1]
    Kin_BjetTopLep_E[j1]        = Kin_BjetTopLep_E_[jj1]
    Kin_NeutTopLep_Phi[j1]      = Kin_NeutTopLep_Phi_[jj1]
    Kin_WTopLep_mW[j1]          = Kin_WTopLep_mW_[jj1]
    if(MEM==True):
        TARGET[j1]      = mc_mem_ttz_weight_evalgenmax_log[jj1]
    else:
        TARGET[j1]      = mc_kin_ttz_weight_logmax[jj1]

if(MEM==True):
    ARRAY = np.stack((reco_bj1_Energy, reco_bj1_Theta, reco_bj1_Phi, reco_bj2_Energy, reco_bj2_Theta, reco_bj2_Phi, reco_MW1_Energy, reco_MW1_Theta, reco_MW1_Phi, reco_MW2_Energy, reco_MW2_Theta, reco_MW2_Phi, reco_l1_Energy, reco_l1_Theta, reco_l1_Phi, reco_l2_Energy, reco_l2_Theta, reco_l2_Phi, reco_l3_Energy, reco_l3_Theta, reco_l3_Phi, reco_mET_Pt, reco_mET_Phi, mHT, Gen_BjetTopHad_E, Gen_WTopHad_mW, Gen_BjetTopLep_E, Gen_NeutTopLep_Phi, Gen_WTopLep_mW))
else:
    ARRAY = np.stack((reco_bj1_Energy, reco_bj1_Theta, reco_bj1_Phi, reco_bj2_Energy, reco_bj2_Theta, reco_bj2_Phi, reco_MW1_Energy, reco_MW1_Theta, reco_MW1_Phi, reco_MW2_Energy, reco_MW2_Theta, reco_MW2_Phi, reco_l1_Energy, reco_l1_Theta, reco_l1_Phi, reco_l2_Energy, reco_l2_Theta, reco_l2_Phi, reco_l3_Energy, reco_l3_Theta, reco_l3_Phi, reco_mET_Pt, reco_mET_Phi, mHT, Kin_BjetTopHad_E, Kin_WTopHad_mW, Kin_BjetTopLep_E, Kin_NeutTopLep_Phi, Kin_WTopLep_mW))

TARGET = np.stack([TARGET])
#TARGET = np.stack((TARGET))

ARRAY = ARRAY.T
TARGET = TARGET.T
#print(ARRAY.shape); print(TARGET.shape)

#X_train = ARRAY[0:N_train]
#Y_train = TARGET[0:N_train]
X_train = ARRAY[:]
Y_train = TARGET[:]
N_validation = ARRAY.shape[0]-(N_train)
#X_validation = ARRAY[(N_train):]
#Y_validation = TARGET[(N_train):]
#N_validation = ARRAY.shape[0]-(N_train)
#print(X_train.shape);print(X_validation.shape);print(Y_train.shape);print(Y_validation.shape)
#print(N_train); print(N_validation)

#X_train, X_test, Y_train, Y_test = train_test_split(X_train, Y_train, train_size=N_train)
#X_train, X_validation, Y_train, Y_validation = train_test_split(X_train, Y_train, test_size=N_validation)
#print(X_train.shape);print(X_validation.shape);print(Y_train.shape);print(Y_validation.shape)

X_train, X_test, Y_train, Y_test = train_test_split(X_train, Y_train, train_size=N_train)
X_train, X_validation, Y_train, Y_validation = train_test_split(X_train, Y_train, test_size=N_validation)
print(X_train.shape,"x_train");print(X_validation.shape,"x_validation");print(Y_train.shape);print(Y_validation.shape)

make_ROOT_DIR = "mkdir -p tens_model_reg/"+Model_name+"/TEST_TRAIN_ROOT/"
os.system(make_ROOT_DIR)
## <SAVE TEST_ROOT>
Test_List = []
for i in range(len(X_test)):
#    if i>1: break
    TEST = np.append(X_test[i],Y_test[i])
    TEST = tuple(TEST)
    Test_List.append(TEST)
#print(Test_List)
TEST_nplist = np.array(Test_List, dtype=[('reco_bj1_Energy',np.float32), ('reco_bj1_Theta',np.float32), ('reco_bj1_Phi',np.float32), ('reco_bj2_Energy',np.float32), ('reco_bj2_Theta',np.float32), ('reco_bj2_Phi',np.float32), ('reco_MW1_Energy',np.float32), ('reco_MW1_Theta',np.float32), ('reco_MW1_Phi',np.float32), ('reco_MW2_Energy',np.float32), ('reco_MW2_Theta',np.float32), ('reco_MW2_Phi',np.float32), ('reco_l1_Energy',np.float32), ('reco_l1_Theta',np.float32), ('reco_l1_Phi',np.float32), ('reco_l2_Energy',np.float32), ('reco_l2_Theta',np.float32), ('reco_l2_Phi',np.float32), ('reco_l3_Energy',np.float32), ('reco_l3_Theta',np.float32), ('reco_l3_Phi',np.float32), ('reco_mET_Pt',np.float32), ('reco_mET_Phi',np.float32), ('mHT',np.float32), ('Gen_BjetTopHad_E',np.float32), ('Gen_WTopHad_mW',np.float32), ('Gen_BjetTopLep_E',np.float32), ('Gen_NeutTopLep_Phi',np.float32), ('Gen_WTopLep_mW',np.float32), ('mc_mem_ttz_weight_evalgenmax_log',np.float32)] )
ROOT_filename = "tens_model_reg/"+Model_name+"/TEST_TRAIN_ROOT/"+"TEST_ROOT.root"
Test_ROOT = TFile(ROOT_filename,"RECREATE")
tree_test = array2tree(TEST_nplist)
tree_test.Write()
Test_ROOT.Close()
del Test_List
del TEST_nplist
## </SAVE TEST_ROOT>

## <SAVE TRAIN ROOT>
Train_List = []
for i in range(len(X_train)):
    TRAIN = np.append(X_train[i],Y_train[i])
    TRAIN = tuple(TRAIN)
    Train_List.append(TRAIN)
TRAIN_nplist = np.array(Train_List,dtype=[('reco_bj1_Energy',np.float32), ('reco_bj1_Theta',np.float32), ('reco_bj1_Phi',np.float32), ('reco_bj2_Energy',np.float32), ('reco_bj2_Theta',np.float32), ('reco_bj2_Phi',np.float32), ('reco_MW1_Energy',np.float32), ('reco_MW1_Theta',np.float32), ('reco_MW1_Phi',np.float32), ('reco_MW2_Energy',np.float32), ('reco_MW2_Theta',np.float32), ('reco_MW2_Phi',np.float32), ('reco_l1_Energy',np.float32), ('reco_l1_Theta',np.float32), ('reco_l1_Phi',np.float32), ('reco_l2_Energy',np.float32), ('reco_l2_Theta',np.float32), ('reco_l2_Phi',np.float32), ('reco_l3_Energy',np.float32), ('reco_l3_Theta',np.float32), ('reco_l3_Phi',np.float32), ('reco_mET_Pt',np.float32), ('reco_mET_Phi',np.float32), ('mHT',np.float32), ('Gen_BjetTopHad_E',np.float32), ('Gen_WTopHad_mW',np.float32), ('Gen_BjetTopLep_E',np.float32), ('Gen_NeutTopLep_Phi',np.float32), ('Gen_WTopLep_mW',np.float32), ('mc_mem_ttz_weight_evalgenmax_log',np.float32)])
ROOT_filename = "tens_model_reg/"+Model_name+"/TEST_TRAIN_ROOT/"+"TRAIN_ROOT.root"
Train_ROOT = TFile(ROOT_filename,"RECREATE")
tree_train = array2tree(TRAIN_nplist)
tree_train.Write()
Train_ROOT.Close()
del Train_List
del TRAIN_nplist
## </SAVE TRAIN ROOT>

epoch_txt_loca="tens_model_reg/"+Model_name
model.fit_regression(X_train, Y_train, X_validation, Y_validation, epochs=epochs, batch_size=batch_size, p_keep=0.5, earlyStop=earlyStop, model_name = model_name, epoch_txt_loca=epoch_txt_loca)
plot_name = "tens_model_reg/"+Model_name+"/"+"ttZ_DNN_reg.pdf"
model.Plot_acc_loss(plot_name = plot_name)

