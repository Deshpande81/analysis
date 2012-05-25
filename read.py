#!/usr/bin/env python
import numpy as np
import sys
import matplotlib.pyplot as plt
import scipy.signal as sig
from rootpy.tree import Tree, TreeModel
from rootpy.io import open
from rootpy.types import *
import ROOT
import datetime
import KDataPy.util as util

plt.ion()
ROOT.gSystem.Load("libkpta")

f = open(sys.argv[1])

tree = f.t

results  = ROOT.TFile("results.root", "recreate")
amp = ROOT.TH1I("amp", "amplitudes", 1000, 0, -1000)

# define objects by prefix:
#tree.define_object(name='date')

bas = ROOT.KBaselineRemoval()
bas.SetBaselineStop(.2)

# define a mixin class to add functionality to a tree object
class Pulse(object):
  def whatever(self): 
    print "hi"
    
# define collections of objects by prefix
tree.define_collection(name='pulsesy',
                       prefix='c1y_',
                       size='c1y_n',
                       mix=Pulse)

tree.define_collection(name='pulsesx',
                       prefix='c1x_',
                       size='c1x_n',
                       mix=Pulse)

# loop over "events" in tree
for event in tree:
  print "%d" % event.date
  
  bas.SetInputPulse( event.c1y_val )
  bas.RunProcess()
  pulsey = util.get_out(bas)
  #plt.plot( np.array(event.c1x_val), util.get_out(bas) )
  amp.Fill( np.argmin(pulsey) ) 
     
  #raw_input()
  #plt.cla()

f.close()
amp.Draw()
results.cd()
amp.Write()
raw_input()


