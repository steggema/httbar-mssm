import ROOT
from ROOT import TFile, TGraph, TMarker, TLine, TLegend, TCanvas

f_hmssm = TFile('data/hMSSM_13TeV.root')

# h_m_A = f_hmssm.Get('m_A')
width_H = f_hmssm.Get('width_H') 
width_A = f_hmssm.Get('width_A') 
m_H = f_hmssm.Get('m_H') 

graphs = []

min_mA = 300.
max_mA = 800.

for tanb in [0.8, 2.0, 10.0]:
    bin_tb = width_H.GetYaxis().FindBin(tanb)
    proj_wH = width_H.ProjectionX('h_wH', bin_tb, bin_tb)
    proj_wA = width_A.ProjectionX('h_wA', bin_tb, bin_tb)
    proj_mH = m_H.ProjectionX('h_mH', bin_tb, bin_tb)
    
    graphH = TGraph(int((max_mA - min_mA)/proj_wH.GetBinWidth(10)))
    graphH.SetLineWidth(3)
    graphH.SetTitle('tan(#beta) = {:.1f}'.format(tanb))

    
    graphA = TGraph(int((max_mA - min_mA)/proj_wA.GetBinWidth(10)))
    graphA.SetLineWidth(3)
    graphA.SetTitle('tan(#beta) = {:.1f}'.format(tanb))

    i_g = 0

    for i_x in xrange(proj_wH.GetNbinsX()):
        mA = proj_wH.GetXaxis().GetBinCenter(i_x)
        mH = proj_mH.GetBinContent(i_x)
        if mA >= min_mA and mA <= max_mA:
            wH = proj_wH.GetBinContent(i_x)
            wA = proj_wA.GetBinContent(i_x)
            
            graphH.SetPoint(i_g, mH, wH)
            graphA.SetPoint(i_g, mA, wA)
            print i_g, wA, wH, mH
            i_g += 1
            
    graphs.append((graphA, graphH))



# The drawing and cosmetics part
c = TCanvas()

legendA = TLegend(0.15, 0.6, 0.4, 0.85)
legendA.AddEntry(None, 'A width', '')

legendH = TLegend(0.45, 0.6, 0.7, 0.85)
legendH.SetTextColor(2)
legendH.AddEntry(None, 'H width', '')

for i_g, (graphA, graphH) in enumerate(graphs):
    graphA.SetLineColor(ROOT.kBlack)
    graphH.SetLineColor(ROOT.kRed)
    graphA.SetLineStyle(i_g + 1)
    graphH.SetLineStyle(i_g + 1)
    if i_g == 0:
        graphA.Draw('AC')
        graphA.GetXaxis().SetTitle('m_{#Phi} (GeV)') #  #prop coupling^{2}
        graphA.GetYaxis().SetTitle('Width (GeV)')
        graphA.GetYaxis().SetTitleSize(0.05)
        graphA.GetYaxis().SetLabelSize(0.05)
        graphA.GetYaxis().SetTitleOffset(0.85)
        graphA.GetXaxis().SetTitleSize(0.05)
        graphA.GetXaxis().SetLabelSize(0.05)
        graphA.GetXaxis().SetTitleOffset(0.89)
        # graph.GetYaxis().SetRangeUser(graph.GetXaxis().GetXmin(), graph.GetXaxis().GetXmax())
    else:
        graphA.Draw('C')
    graphH.Draw('C')
    legendA.AddEntry(graphA, graphA.GetTitle(), 'l')
    legendH.AddEntry(graphH, graphH.GetTitle(), 'l')

    graphA.SetTitle('hMSSM width relations')

    


legendA.SetBorderSize(0)
legendA.Draw()
legendH.SetBorderSize(0)
legendH.Draw()
c.Print('widths_vs_ma.pdf')
