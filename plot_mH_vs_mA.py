import ROOT
from ROOT import TFile, TGraph, TMarker, TLine, TLegend, TCanvas

f_hmssm = TFile('data/hMSSM_13TeV.root')

# h_m_A = f_hmssm.Get('m_A')
m_H = f_hmssm.Get('m_H') 

graphs = []

min_mA = 300.
max_mA = 800.

for tanb in [0.8, 2.0, 10.0]:
    bin_tb = m_H.GetYaxis().FindBin(tanb)
    proj_mH = m_H.ProjectionX('h_mH', bin_tb, bin_tb)
    
    graph = TGraph(int((max_mA - min_mA)/proj_mH.GetBinWidth(10)))
    graph.SetLineWidth(3)
    graph.SetTitle('tan(#beta) = {:.1f}'.format(tanb))

    i_g = 0

    print int((max_mA - min_mA)/proj_mH.GetBinWidth(10))

    for i_x in xrange(proj_mH.GetNbinsX()):
        mA = proj_mH.GetXaxis().GetBinCenter(i_x)
        if mA >= min_mA and mA <= max_mA:
            mH = proj_mH.GetBinContent(i_x)
            graph.SetPoint(i_g, mA, mH)
            print i_g, mA, mH
            i_g += 1
            
    
    graphs.append(graph)



# The drawing and cosmetics part
c = TCanvas()

colours = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue-4]

legend = TLegend(0.15, 0.6, 0.4, 0.85)

for i_g, graph in enumerate(graphs):
    graph.SetLineColor(colours[i_g])
    graph.SetLineStyle(i_g + 1)
    if i_g == 0:
        graph.Draw('AC')
        graph.GetXaxis().SetTitle('m_{A} (GeV)') #  #prop coupling^{2}
        graph.GetYaxis().SetTitle('m_{H} (GeV)')
        graph.GetYaxis().SetTitleSize(0.05)
        graph.GetYaxis().SetLabelSize(0.05)
        graph.GetYaxis().SetTitleOffset(0.85)
        graph.GetXaxis().SetTitleSize(0.05)
        graph.GetXaxis().SetLabelSize(0.05)
        graph.GetXaxis().SetTitleOffset(0.89)
        graph.GetYaxis().SetRangeUser(graph.GetXaxis().GetXmin(), graph.GetXaxis().GetXmax())
    else:
        graph.Draw('C')
    legend.AddEntry(graph, graph.GetTitle(), 'l')
    graph.SetTitle('hMSSM mass relations')


legend.SetBorderSize(0)
legend.Draw()

c.Print('mh_vs_ma.pdf')
