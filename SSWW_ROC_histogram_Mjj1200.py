from ROOT import *
import sys, os, math
import numpy as np
from array import array

def ROC_List_Maker(dirname='./',dirnameNN='./', verbose=0):
    LL_filename = dirname+"/SS_4p0M_cut_LL_Mjj1200_tree_hist.root"
    TTTL_filename = dirname +"/SS_4p0M_cut_TTTL_Mjj1200_tree_hist.root" 
    LL_TFile = TFile(LL_filename,"READ") 
    TTTL_TFile = TFile(TTTL_filename,"READ")   
    LL_LL_Hist = LL_TFile.Get("LL")
    TTTL_LL_Hist = TTTL_TFile.Get("LL")

    if verbose==1:
        #LL_var_filename = dirname+"/TEST_ROOT_LL_hist.root"
        #TTTL_var_filename = dirname+"/TEST_ROOT_TTTL_hist.root"
        LL_var_filename = "/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_fitting/ROC_PureMC_input/SS_2p5M_cut_LL_hist.root"
        TTTL_var_filename = "/Users/leejunho/Desktop/git/PKUHEP/DNN/SSWW_fitting/ROC_PureMC_input/SS_2p5M_cut_TTTL_hist.root"
        LL_var_TFile = TFile(LL_var_filename,"READ")
        TTTL_var_TFile = TFile(TTTL_var_filename,"READ")
        LL_lep1pt_Hist = LL_var_TFile.Get("lep1pt")
        TTTL_lep1pt_Hist = TTTL_var_TFile.Get("lep1pt")
        LL_dphijj_Hist = LL_var_TFile.Get("dphijj")
        TTTL_dphijj_Hist = TTTL_var_TFile.Get("dphijj")
        LL_detajj_Hist = LL_var_TFile.Get("detajj")
        TTTL_detajj_Hist = TTTL_var_TFile.Get("detajj")
        LL_Mjj_Hist = LL_var_TFile.Get("Mjj")
        TTTL_Mjj_Hist = TTTL_var_TFile.Get("Mjj")
        LL_jet1pt_Hist = LL_var_TFile.Get("jet1pt")
        TTTL_jet1pt_Hist = TTTL_var_TFile.Get("jet1pt")
        '''
        LL_NN_filename = dirnameNN+"/TEST_ROOT_LL_tree_hist.root"
        TTTL_NN_filename = dirnameNN +"/TEST_ROOT_TTTL_tree_hist.root"
        LL_NN_TFile = TFile(LL_NN_filename,"READ")
        TTTL_NN_TFile = TFile(TTTL_NN_filename,"READ")
        LL_LL_NN_Hist = LL_NN_TFile.Get("LL")
        TTTL_LL_NN_Hist = TTTL_NN_TFile.Get("LL")
        '''

    DNN_list = list()
    ROC_list = list()
    TotalBinNum = LL_LL_Hist.GetSize()-2
    if(TotalBinNum!= TTTL_LL_Hist.GetSize()-2):
        print("LL and TTTL histo bin number is not identical, ERROR!")
        return

    LL_ETotal=0; TTTL_ETotal=0;
    for i in range(TotalBinNum):
        LL_ETotal += LL_LL_Hist.GetBinContent(i+1)
        TTTL_ETotal += TTTL_LL_Hist.GetBinContent(i+1)
    print("Total Entry for True LL :",LL_ETotal)
    print("Total Entry for True TTTL :",TTTL_ETotal)
   
    LL_temp=0; TTTL_temp=0 
    for i in range(TotalBinNum):    
        temp_list = []
        LL_temp += LL_LL_Hist.GetBinContent(i+1)
        TTTL_temp += TTTL_LL_Hist.GetBinContent(i+1)
        TPR = (LL_ETotal-LL_temp)/LL_ETotal
        FPR = (TTTL_ETotal-TTTL_temp)/TTTL_ETotal
        temp_list.append(TPR);
        temp_list.append(FPR);
        DNN_list.append(temp_list)
        del temp_list
    ROC_list.append(DNN_list)
    del DNN_list


    if verbose==1:
        lep1pt_list = []; dphijj_list = []; detajj_list = []; Mjj_list = []; jet1pt_list = [];
        TotalBinNum_var = TTTL_dphijj_Hist.GetSize()-2
        LL_var_ETotal=0; TTTL_var_ETotal=0;
        for i in range(TotalBinNum_var):
            LL_var_ETotal += LL_dphijj_Hist.GetBinContent(i+1)
            TTTL_var_ETotal += TTTL_dphijj_Hist.GetBinContent(i+1)

        LL_lep1pt_temp=0; TTTL_lep1pt_temp=0
        LL_dphijj_temp=0; TTTL_dphijj_temp=0
        LL_detajj_temp=0; TTTL_detajj_temp=0
        LL_Mjj_temp=0; TTTL_Mjj_temp=0
        LL_jet1pt_temp=0; TTTL_jet1pt_temp=0
        for i in range(TotalBinNum_var):
            temp_lep1pt_list = []; temp_dphijj_list = []; temp_detajj_list = []; temp_Mjj_list = []; temp_jet1pt_list=[];
            LL_lep1pt_temp += LL_lep1pt_Hist.GetBinContent(i+1)
            TTTL_lep1pt_temp += TTTL_lep1pt_Hist.GetBinContent(i+1)
            LL_dphijj_temp += LL_dphijj_Hist.GetBinContent(i+1)
            TTTL_dphijj_temp += TTTL_dphijj_Hist.GetBinContent(i+1)
            LL_detajj_temp += LL_detajj_Hist.GetBinContent(i+1)
            TTTL_detajj_temp += TTTL_detajj_Hist.GetBinContent(i+1)
            LL_Mjj_temp += LL_Mjj_Hist.GetBinContent(i+1)
            TTTL_Mjj_temp += TTTL_Mjj_Hist.GetBinContent(i+1)
            LL_jet1pt_temp += LL_jet1pt_Hist.GetBinContent(i+1)
            TTTL_jet1pt_temp += TTTL_jet1pt_Hist.GetBinContent(i+1)
            TPR_lep1pt = (LL_var_ETotal-LL_lep1pt_temp)/LL_var_ETotal 
            FPR_lep1pt = (TTTL_var_ETotal-TTTL_lep1pt_temp)/TTTL_var_ETotal
            TPR_dphijj = (LL_var_ETotal-LL_dphijj_temp)/LL_var_ETotal
            FPR_dphijj = (TTTL_var_ETotal-TTTL_dphijj_temp)/TTTL_var_ETotal
            TPR_detajj = (LL_var_ETotal-LL_detajj_temp)/LL_var_ETotal
            FPR_detajj = (TTTL_var_ETotal-TTTL_detajj_temp)/TTTL_var_ETotal
            TPR_Mjj = (LL_var_ETotal-LL_Mjj_temp)/LL_var_ETotal
            FPR_Mjj = (TTTL_var_ETotal-TTTL_Mjj_temp)/TTTL_var_ETotal
            TPR_jet1pt = (LL_var_ETotal-LL_jet1pt_temp)/LL_var_ETotal
            FPR_jet1pt = (TTTL_var_ETotal-TTTL_jet1pt_temp)/TTTL_var_ETotal
            temp_lep1pt_list.append(TPR_lep1pt); temp_lep1pt_list.append(FPR_lep1pt);
            temp_dphijj_list.append(TPR_dphijj); temp_dphijj_list.append(FPR_dphijj);
            temp_detajj_list.append(TPR_detajj); temp_detajj_list.append(FPR_detajj);
            temp_Mjj_list.append(TPR_Mjj); temp_Mjj_list.append(FPR_Mjj);
            temp_jet1pt_list.append(TPR_jet1pt); temp_jet1pt_list.append(FPR_jet1pt);
            lep1pt_list.append(temp_lep1pt_list)
            dphijj_list.append(temp_dphijj_list)
            detajj_list.append(temp_detajj_list)
            Mjj_list.append(temp_Mjj_list)
            jet1pt_list.append(temp_jet1pt_list)
            del temp_lep1pt_list; del temp_dphijj_list; del temp_detajj_list; del temp_Mjj_list; del temp_jet1pt_list;
        ROC_list.append(lep1pt_list);
        ROC_list.append(dphijj_list);
        ROC_list.append(detajj_list);
        ROC_list.append(Mjj_list);
        ROC_list.append(jet1pt_list); 

        '''
        NN_list = []
        TotalBinNum_NN = LL_LL_NN_Hist.GetSize()-2
        LL_NN_ETotal=0; TTTL_NN_ETotal=0;
        for i in range(TotalBinNum_NN):
            LL_NN_ETotal += LL_LL_NN_Hist.GetBinContent(i+1)
            TTTL_NN_ETotal += TTTL_LL_NN_Hist.GetBinContent(i+1)
        print("Total Entry for True NN LL :",LL_NN_ETotal)
        print("Total Entry for True NN TTTL :",TTTL_NN_ETotal)
        LL_NN_temp=0; TTTL_NN_temp=0
        for i in range(TotalBinNum_NN):
            temp_list = []
            LL_NN_temp += LL_LL_NN_Hist.GetBinContent(i+1)
            TTTL_NN_temp += TTTL_LL_NN_Hist.GetBinContent(i+1)
            TPR_NN = (LL_NN_ETotal-LL_NN_temp)/LL_NN_ETotal
            FPR_NN = (TTTL_NN_ETotal-TTTL_NN_temp)/TTTL_NN_ETotal
            temp_list.append(TPR_NN);
            temp_list.append(FPR_NN);
            NN_list.append(temp_list)
            del temp_list
        ROC_list.append(NN_list)
        '''
    #print(ROC_list)
        '''
        #MY_BDT
        BDT_list = []
        BDT_filename = "/Users/leejunho/Downloads/root6_cmake/tutorials/tmva/SSWW_TMVA.root"
        BDT_TFile = TFile(BDT_filename,"READ")
        LL_BDT_Hist = BDT_TFile.Get("dataset/Method_BDT/BDT/MVA_BDT_S")
        TTTL_BDT_Hist = BDT_TFile.Get("dataset/Method_BDT/BDT/MVA_BDT_B")
        TotalBinNum_BDT = LL_BDT_Hist.GetSize()-2
        LL_BDT_ETotal = 0; TTTL_BDT_ETotal = 0
        for i in range(TotalBinNum_BDT):
            LL_BDT_ETotal += LL_BDT_Hist.GetBinContent(i+1)
            TTTL_BDT_ETotal += TTTL_BDT_Hist.GetBinContent(i+1)
        print("Total Entry for True BDT LL :",LL_BDT_ETotal)
        print("Total Entry for True BDT TTTL :",TTTL_BDT_ETotal)
        LL_BDT_temp=0; TTTL_BDT_temp=0
        for i in range(TotalBinNum_BDT):
            temp_list = []
            LL_BDT_temp += LL_BDT_Hist.GetBinContent(i+1)
            TTTL_BDT_temp += TTTL_BDT_Hist.GetBinContent(i+1)
            TPR_BDT = (LL_BDT_ETotal-LL_BDT_temp)/LL_BDT_ETotal
            FPR_BDT = (TTTL_BDT_ETotal-TTTL_BDT_temp)/TTTL_BDT_ETotal
            temp_list.append(TPR_BDT);
            temp_list.append(FPR_BDT);
            BDT_list.append(temp_list)
            del temp_list
        ROC_list.append(BDT_list)
        '''

        ''' #TMVA BDT 
        BDT_list = []
        BDT_filename = "/Users/leejunho/Downloads/root6_cmake/tutorials/tmva/SSWW_TMVA.root"
        BDT_TFile = TFile(BDT_filename,"READ")
        BDT_Hist = BDT_TFile.Get("dataset/Method_BDT/BDT/MVA_BDT_rejBvsS")
        TotalBinNum_BDT = BDT_Hist.GetSize()-2
        for i in range(TotalBinNum_BDT):
            one_fill = BDT_Hist.GetBinCenter(i+1)
            two_fill = BDT_Hist.GetBinContent(i+1)
            temp_list = [one_fill,two_fill]
            #print(temp_list)
            BDT_list.append(temp_list)
            del temp_list
        BDT_list.append([1,0])
        ROC_list.append(BDT_list)
        '''

    return ROC_list


def ROC_plotter(Roc_list,dirname,verbose=0):
    xarray_TPR = array( 'd' ); yarray_FPR=array( 'd' ); 
    for i,content in enumerate(Roc_list[0]):
        xarray_TPR.append(1-content[1])
        yarray_FPR.append(content[0])
    #print(xarray_TPR); print(yarray_FPR)

    c1 = TCanvas('c1', 'A Simple Graph Example', 200, 10, 700, 500);
    c1.SetGrid()
    gr = TGraph( len(Roc_list[0]), xarray_TPR, yarray_FPR )
    gr.SetLineColor(kRed)
    gr.SetLineWidth( 4 )
    gr.SetMarkerColor(kRed)
    gr.SetMarkerStyle( 21 )
    gr.SetTitle('ROC')
    gr.GetXaxis().SetTitle( '1-FPR' )
    gr.GetYaxis().SetTitle( 'TPR' )
    #gr.Draw( 'ACP' )
    #gr.Draw('AL')
    gr.Draw( 'AC' )


    if verbose==1:
        xarray_lep1pt_TPR = array( 'd' ); yarray_lep1pt_FPR=array( 'd' );
        for i,content in enumerate(Roc_list[1]):
            xarray_lep1pt_TPR.append(1-content[0])
            yarray_lep1pt_FPR.append(content[1])
        xarray_dphijj_TPR = array( 'd' ); yarray_dphijj_FPR=array( 'd' );
        for i,content in enumerate(Roc_list[2]):
            xarray_dphijj_TPR.append(1-content[1])
            yarray_dphijj_FPR.append(content[0])
        xarray_detajj_TPR = array( 'd' ); yarray_detajj_FPR=array( 'd' );
        for i,content in enumerate(Roc_list[3]):
            xarray_detajj_TPR.append(1-content[1])
            yarray_detajj_FPR.append(content[0])
        xarray_Mjj_TPR = array( 'd' ); yarray_Mjj_FPR=array( 'd' );
        for i,content in enumerate(Roc_list[4]):
            xarray_Mjj_TPR.append(1-content[1])
            yarray_Mjj_FPR.append(content[0])
        xarray_jet1pt_TPR = array( 'd' ); yarray_jet1pt_FPR=array( 'd' );
        for i,content in enumerate(Roc_list[5]):
            xarray_jet1pt_TPR.append(1-content[0])
            yarray_jet1pt_FPR.append(content[1])
        '''
        xarray_NN_TPR = array( 'd' ); yarray_NN_FPR=array( 'd' );
        for i,content in enumerate(Roc_list[6]):
            xarray_NN_TPR.append(1-content[1])
            yarray_NN_FPR.append(content[0])
        '''
        '''
        xarray_BDT_TPR = array( 'd' ); yarray_BDT_FPR=array( 'd' );
        for i,content in enumerate(Roc_list[6]):
            xarray_BDT_TPR.append(1-content[1])
            yarray_BDT_FPR.append(content[0])
        '''

        gr_lep1pt = TGraph( len(Roc_list[1]), xarray_lep1pt_TPR, yarray_lep1pt_FPR)
        gr_lep1pt.SetLineColor(kBlue); gr_lep1pt.SetLineWidth(4); gr_lep1pt.SetMarkerColor(kBlue); gr_lep1pt.SetMarkerStyle(21); gr_lep1pt.Draw("C SAME")
        gr_dphijj = TGraph( len(Roc_list[2]), xarray_dphijj_TPR, yarray_dphijj_FPR)
        gr_dphijj.SetLineColor(kGreen); gr_dphijj.SetLineWidth(4); gr_dphijj.SetMarkerColor(kGreen); gr_dphijj.SetMarkerStyle(21); gr_dphijj.Draw("L SAME")
        gr_detajj = TGraph( len(Roc_list[3]), xarray_detajj_TPR, yarray_detajj_FPR)
        gr_detajj.SetLineColor(kMagenta); gr_detajj.SetLineWidth(4); gr_detajj.SetMarkerColor(kMagenta); gr_detajj.SetMarkerStyle(21); gr_detajj.Draw("C SAME")
        gr_Mjj = TGraph( len(Roc_list[4]), xarray_Mjj_TPR, yarray_Mjj_FPR)
        gr_Mjj.SetLineColor(41); gr_Mjj.SetLineWidth(4); gr_Mjj.SetMarkerColor(41); gr_Mjj.SetMarkerStyle(21); gr_Mjj.Draw("C SAME")
        gr_jet1pt = TGraph( len(Roc_list[5]), xarray_jet1pt_TPR, yarray_jet1pt_FPR)
        gr_jet1pt.SetLineColor(kBlack); gr_jet1pt.SetLineWidth(4); gr_jet1pt.SetMarkerColor(kBlack); gr_jet1pt.SetMarkerStyle(21); gr_jet1pt.Draw("C SAME")
        '''
        gr_NN = TGraph( len(Roc_list[6]), xarray_NN_TPR, yarray_NN_FPR)
        gr_NN.SetLineColor(46); gr_NN.SetLineWidth(4); gr_NN.SetMarkerColor(46); gr_NN.SetMarkerStyle(21); gr_NN.Draw("C SAME")
        gr_BDT = TGraph( len(Roc_list[7]), xarray_BDT_TPR, yarray_BDT_FPR)
        gr_BDT.SetLineColor(17); gr_BDT.SetLineWidth(4); gr_BDT.SetMarkerColor(17); gr_BDT.SetMarkerStyle(21); gr_BDT.Draw("C SAME")
        '''

    gr_cross = TGraph(2, array('d',[0,1]),array('d',[1,0]))   
    #gr_hori = TGraph(2, array('d',[0,1]),array('d',[1,1]))
    #gr_verti = TGraph(2, array('d',[1,0]),array('d',[1,1]))
    gr_cross.Draw("same"); #gr_hori.Draw("same"); gr_verti.Draw("same")



    legend = TLegend(0.7,0.7,1.0,1.0)
    legend.AddEntry(gr,"DNN","l")
    if verbose==1:
        legend.AddEntry(gr_lep1pt,"lep1pt","l")
        legend.AddEntry(gr_dphijj,"dphijj","l")
        legend.AddEntry(gr_detajj,"detajj","l")
        legend.AddEntry(gr_Mjj,"Mjj","l")
        legend.AddEntry(gr_jet1pt,"jet1pt","l")
        #legend.AddEntry(gr_NN,"NN","l")
        #legend.AddEntry(gr_BDT,"BDT","l")
    legend.Draw()

    c1.SaveAs("ROC_test.pdf")
    mv_cmd = "mv ROC_test.pdf " + dirname
    os.system(mv_cmd)


def main():
    dirname = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/From_ipnl/Raw_20181115_TrainENum2600000/LayerNum_10+Node_150+BatchSize_10/TEST_TRAIN_ROOT_Mjj1200" #FIXME
    dirnameNN = "/Users/leejunho/Desktop/git/PKUHEP/DNN/tens_model_class/From_ipnl/High_20181010_TrainENum700000/LayerNum_1+Node_150+BatchSize_10/TEST_TRAIN_ROOT" #FIXME
    verbose = 1  #FIXME


    Roc_list = ROC_List_Maker(dirname=dirname,dirnameNN=dirnameNN,verbose=verbose)
    ROC_plotter(Roc_list=Roc_list,dirname=dirname,verbose=verbose)



if __name__=="__main__":
    main()
