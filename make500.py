import ROOT
fin = ROOT.TFile.Open('cartesian_upsilon_taus_GENSIM_withBP_12GeV_19.root')
tree = fin.Get('tree')
fout = ROOT.TFile('fout.root', 'recreate')
tree.CopyTree("Entry$ < %d" % (tree.GetEntries() * 0.506))
fout.Write()
