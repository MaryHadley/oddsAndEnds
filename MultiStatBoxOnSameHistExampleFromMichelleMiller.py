import ROOT as r
import sys
from ROOT import gROOT,gStyle,TCanvas, TF1
import FWCore.ParameterSet.Config as cms
from histogrammar import *

## Read in the files that contain the branches and the information you want using f.TFile; recognize this as the original ROOT command of calling a file
ljmet_f = r.TFile('/eos/uscms/store/user/mcmiller/ljmet/131kMiniParents.root')
##The input file below is the output file of the step1 that Jess edited
nano_f = r.TFile('/eos/uscms/store/user/mcmiller/NanoAOD/131kNanoEvents.root')

# This get object command puts the branches from the root files into the histograms we named (first entry is the branch and the second entry is the histogram you defined)
lj = ljmet_f.Get('ljmetTpTp_MiniAod')
nano = nano_f.Get('ljmet')


MyNanoHists = {}
MyLJHists = {}
branches = []
 
for branch in nano.GetListOfBranches():
	## creating string names for the branches which will be used as labels
	string = ('%s' %branch).split(' ')[2]
        string = string.split('("')[1].split('")')[0]
	#sys.stderr.write("Sample: %s\n" % branch)
	branches.append(branch.GetName())

for branch in branches:
	c1 = r.TCanvas()
##Needing to fill a histogram to use the TPaveStats argument
	sys.stderr.write("branch: %s \n" %branch)
	histNanoLabel = "%s" % (branch)
	histLJLabel = "%s" %(branch)
	
	print branch
	print ("branch %s" %histLJLabel)	
	x_min= min(nano.GetMinimum(branch), lj.GetMinimum(branch))
	x_max = max(nano.GetMaximum(branch), lj.GetMaximum(branch))
	nbin=max(int((x_max-x_min)/10), 100)	
####NanoAOD plots
	MyNanoHists[histNanoLabel]=r.TH1D(histNanoLabel,histNanoLabel,100 , x_min, x_max)
	nano.Draw("%s >> %s" %(branch,histNanoLabel))
	#StatBox = MyNanoHists[histNanoLabel].GetListOfFunctions().FindObject("stats")
	#StatBox.SetY1NDC(.5)
	#StatBox.SetY2NDC(.30)
	MyNanoHists[histNanoLabel].SetFillStyle(3001)
        MyNanoHists[histNanoLabel].SetFillColor(2)
        MyNanoHists[histNanoLabel].SetLineColor(2) 
	print MyNanoHists[histNanoLabel].GetXaxis().GetXmax()
	c1.Update()
	gStyle.SetOptStat(1111111)
	StatBox = MyNanoHists[histNanoLabel].GetListOfFunctions().FindObject("stats")
	StatBox.SetY1NDC(.5)
        StatBox.SetY2NDC(.20)

	###LJMet Plot
	gStyle.SetOptStat(1111111)
	MyLJHists[histLJLabel]=r.TH1D(histLJLabel,histLJLabel,100, x_min, x_min)
	print MyLJHists[histLJLabel]
	lj.Draw("%s >> %s" %(branch,histLJLabel), "", "SAMES")
	MyLJHists[histLJLabel].SetLineColor(4)
        MyLJHists[histLJLabel].SetFillColor(4)
	MyLJHists[histLJLabel].SetFillStyle(3001)
	#legend = r.TLegend(0.1,0.3,0.4,0.5)
	#legend.AddEntry( histLJLabel,"LJmet with MiniAOD","F")
	#legend.AddEntry( histNanoLabel,"step1 with NanoAOD","F")
	#legend.AddEntry( MyNanoHists[histNanoLabel].GetRMS(),"nano RMS", "")
	#legend.AddEntry( MyNanoHists[histNanoLabel].GetRMSError(),"nano RMS Error","")
	#legend.Draw()
	c1.Update()
	#MyLJHists[histLJLabel].Draw("same")
	#StatBox1 = MyLJHists[histLJLabel].GetListOfFunctions().FindObject("stats")
	#print StatBox1
	#StatBox1.SetY1NDC(.5)
        #StatBox1.SetY2NDC(.2)
#
## IsA --> give me the class that an object is
## Canvas.GetListOfPrimitives  
##dir(hist)
	
#c1.SaveAs('plots.root')	
	c1.SaveAs('%s_plot.pdf' %branch)

#for branch in branches:
	f = open("%s_stats.txt" %branch, 'w')
	f.write("nano mean %f" %MyNanoHists[histNanoLabel].GetMean())
	f.write("LJmet  mean %f \n" %MyLJHists[histLJLabel].GetMean())

	f.write("nano StdDev %f " %MyNanoHists[histNanoLabel].GetStdDev())
	f.write("LJmet  StdDev  %f \n" %MyLJHists[histLJLabel].GetStdDev())

	#Not for binned data ; don't use the KS test
	##f.write("KS Stat %f " %MyNanoHists[histNanoLabel].KolmogorovTest(MyLJHists[histLJLabel]))
	##f.write("KS Stat %f \n" %MyLJHists[histLJLabel].KolmogorovTest(MyNanoHists[histNanoLabel]))
	
	f.write("nano mean %f " %MyNanoHists[histNanoLabel].GetEntries())
	f.write("LJmet  Entries  %f \n" %MyLJHists[histLJLabel].GetEntries())
	
	f.write("nano RMS %f " %MyNanoHists[histNanoLabel].GetRMS())
        f.write("LJmet RMS  %f \n" %MyLJHists[histLJLabel].GetRMS())
	
	f.write("nano RMS Error %f " %MyNanoHists[histNanoLabel].GetRMSError())
        f.write("LJmet  RMS Error  %f \n" %MyLJHists[histLJLabel].GetRMSError())
	
	f.write("nano Chi Squared %f " %MyNanoHists[histNanoLabel].Chi2Test(MyLJHists[histLJLabel]))
        f.write("LJmet  Chi Squared  %f \n" %MyLJHists[histLJLabel].Chi2Test(MyNanoHists[histNanoLabel]))	

	f.close()	

BranchesBinned = ['elDR03TkSumPt_singleLepCalc', 'isBWBW_TpTpCalc', 'isTau_singleLepCalc', 'isTHBW_TpTpCalc', 'isTHTH_TpTpCalc', 'isTT_TTbarMassCalc', 'isTTbb_TTbarMassCalc', 'isTTbj_TTbarMassCalc', 'isTTcc_TTbarMassCalc', 'isTTcj_TTbarMassCalc', 'isTTlf_TTbarMassCalc', 'isTTll_TTbarMassCalc', 'isTZBW_TpTpCalc', 'isTZTH_TpTpCalc', 'isTZTZ_TpTpCalc', 'NExtraBs_TTbarMassCalc', 'NExtraCs_TTbarMassCalc', 'NExtraLs_TTbarMassCalc', 'NLeptonDecays_TpTpCalc','theJetAK8SDSubjetIndex_JetSubCalc']

bin_size =[100,2,2,2,2,2,2,2,2,2,2,2,2,2,2,6,9,15,6,15]


for i in range(20):
	c1 = r.TCanvas()
##Needing to fill a histogram to use the TPaveStats argument
        sys.stderr.write("branch: %s \n" %BranchesBinned[i])
        histNanoLabel = "%s" % (BranchesBinned[i])
        histLJLabel = "%s" %(BranchesBinned[i])

        print ("branch %s" %histLJLabel)
        x_min= min(nano.GetMinimum(BranchesBinned[i]), lj.GetMinimum(BranchesBinned[i]))
        x_max = max(nano.GetMaximum(BranchesBinned[i]), lj.GetMaximum(BranchesBinned[i]))
	print x_min
	print x_max
####NanoAOD plots
        MyNanoHists[histNanoLabel]=r.TH1D(histNanoLabel,histNanoLabel,bin_size[i] , x_min, x_max)
        nano.Draw("%s >> %s" %(BranchesBinned[i],histNanoLabel))
        MyNanoHists[histNanoLabel].SetFillStyle(3001)
        MyNanoHists[histNanoLabel].SetFillColor(2)
        MyNanoHists[histNanoLabel].SetLineColor(2)
        print MyNanoHists[histNanoLabel].GetXaxis().GetXmax()
        c1.Update()
        gStyle.SetOptStat(1111111)
        StatBox = MyNanoHists[histNanoLabel].GetListOfFunctions().FindObject("stats")
        StatBox.SetY1NDC(.5)
        StatBox.SetY2NDC(.20)

        ###LJMet Plot
        gStyle.SetOptStat(1111111)
        MyLJHists[histLJLabel]=r.TH1D(histLJLabel,histLJLabel,bin_size[i], x_min, x_min)
        print MyLJHists[histLJLabel]
        lj.Draw("%s >> %s" %(BranchesBinned[i],histLJLabel), "", "SAMES")
        MyLJHists[histLJLabel].SetLineColor(4)
        MyLJHists[histLJLabel].SetFillColor(4)
        MyLJHists[histLJLabel].SetFillStyle(3001)
        c1.Update()
        c1.SaveAs('%s_plot.pdf' %BranchesBinned[i])


