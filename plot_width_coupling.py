from ROOT import TFile, TGraph, TMarker, TLine, TLegend, TCanvas

f_hmssm = TFile('data/hMSSM_13TeV.root')

h_width_A = f_hmssm.Get('width_A')
h_br_A_tt = f_hmssm.Get('br_A_tt') # to calculate partial width

mass = 750.

bin_mass = h_width_A.FindBin(mass)

h_width = h_width_A.ProjectionY('h_width', bin_mass, bin_mass)
h_br = h_br_A_tt.ProjectionY('h_br', bin_mass, bin_mass)

h_coupling = h_width.Clone('h_coupling')

for i in xrange(1, h_coupling.GetNbinsX() + 1):
    h_coupling.SetBinContent(i, 1./h_coupling.GetXaxis().GetBinCenter(i)**2)

n_points = h_width.GetNbinsX()
g_width = TGraph(n_points)
g_partial_width = TGraph(n_points)

for i in xrange(n_points):
    g_width.SetPoint(i, h_coupling.GetBinContent(i + 1), h_width.GetBinContent(i + 1))
    g_partial_width.SetPoint(i, h_coupling.GetBinContent(i + 1), h_width.GetBinContent(i + 1)*h_br.GetBinContent(i + 1))


# Points/lines for simulated samples
p_5percent = TMarker(1., 0.05*mass, 1)
p_10percent = TMarker(1., 0.1*mass, 2)
p_25percent = TMarker(1., 0.25*mass, 3)

def findX(graph, y):
    '''Find x value, assume monotonously decreasing y'''
    xvals = graph.GetX()
    yvals = graph.GetY()
    for i in xrange(graph.GetN()):
        yval = yvals[i]
        xval = xvals[i]
        print xval, yval, y
        if yval < y:
            if i == 0:
                return xval
            deltay = yval - yvals[i-1]

            weight_down = (yval - y)/deltay
            weight_up = (y - yvals[i-1])/deltay
            print 'For y =', y, 'return', weight_down*xvals[i-1] + weight_up*xval
            return weight_down*xvals[i-1] + weight_up*xval
    else:
        print 'Graph find x: No value found; assigning max val found'
    
    return xvals[graph.GetN()-1]


l_5percent = TLine(0., 0.05*mass, findX(g_partial_width, 0.05*mass), 0.05*mass)
l_10percent = TLine(0., 0.1*mass, findX(g_partial_width, 0.1*mass), 0.1*mass)
l_25percent = TLine(0., 0.25*mass, findX(g_partial_width, 0.25*mass), 0.25*mass)

# The drawing and cosmetics part
c = TCanvas()

g_width.Draw('AC')
g_width.SetLineWidth(2)
g_width.SetTitle('hMSSM, m_{{A}} = {mass} GeV'.format(mass=int(mass)))

l_5percent.SetLineColor(2)
l_5percent.SetLineWidth(3)
l_10percent.SetLineColor(2)
l_10percent.SetLineWidth(3)
l_10percent.SetLineStyle(2)
l_25percent.SetLineColor(2)
l_25percent.SetLineStyle(3)
l_25percent.SetLineWidth(3)

p_5percent.SetMarkerStyle(20)
p_5percent.SetMarkerColor(2)
p_10percent.SetMarkerStyle(21)
p_10percent.SetMarkerColor(2)
p_25percent.SetMarkerStyle(22)
p_25percent.SetMarkerColor(2)

p_5percent.Draw()
l_5percent.Draw()
p_10percent.Draw()
l_10percent.Draw()
p_25percent.Draw()
l_25percent.Draw()

g_width.GetXaxis().SetTitle('1/tan(#beta)^{2}') #  #prop coupling^{2}
g_width.GetYaxis().SetTitle('Width (GeV)')
g_width.GetYaxis().SetRangeUser(0., mass*0.12)

g_partial_width.SetLineColor(4)
g_partial_width.SetLineWidth(3003)
g_partial_width.SetFillStyle(3002)
g_partial_width.Draw('C')

legend = TLegend(0.15, 0.6, 0.4, 0.85)
legend.AddEntry(g_width, 'Total width', 'l')
legend.AddEntry(g_partial_width, 'Partial width (t#bar{t})', 'l')

g_partial_width_excl = g_partial_width.Clone('g_partial_width_excl')
g_partial_width_excl.SetLineWidth(0)
g_partial_width_excl.SetLineColor(0)

legend.AddEntry(g_partial_width_excl, 'Forbidden', 'f')
legend.AddEntry(p_5percent, 'Sample (5% width)', 'p')
legend.AddEntry(p_10percent, 'Sample (10% width)', 'p')
legend.SetBorderSize(0)
legend.Draw()

c.Print('width_vs_tanb_mA{mass}.pdf'.format(mass=int(mass)))
