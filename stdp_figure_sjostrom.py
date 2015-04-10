from util import get_all_save_keys, get_periodic_current, get_inst_backprop, get_fixed_spiker, get_dendr_spike_det_dyn_ref
from helper import do, PeriodicAccumulator, BooleanAccumulator, dump, get_default
import numpy as np
from IPython import embed
import cPickle
from collections import OrderedDict
from simulation import run
import matplotlib.pyplot as plt
import time


def task((repetition_i,p)):

    learn = {}
    learn['eta'] = 1e-7
    learn['eps'] = 1e-3
    learn['tau_delta'] = 2.0
    
    n_spikes = 40.0
        

    neuron = get_default("neuron")
    neuron["phi"]['r_max'] = p["r_max"]
    neuron["phi"]['alpha'] = p["alpha"]
    neuron["phi"]['beta'] = p["beta"]
    neuron["g_L"] = p["g_L"]
    
    freq = p["freq"]
    delta = p["delta"]

    first_spike = 1000.0/(2*freq)
    isi = 1000.0/freq
    t_end = 1000.0*n_spikes/freq
    
    spikes = np.arange(first_spike, t_end, isi)
    pre_spikes = spikes + delta
    
    my_s = {
        'start': 0.0,
        'end': t_end,
        'dt': 0.05,
        'pre_spikes': pre_spikes,
        'I_ext': lambda t: 0.0
        }
        
    seed = int(int(time.time()*1e8)%1e9)
    accs = [PeriodicAccumulator(['weight'], interval=10)]
    accums = run(my_s, get_fixed_spiker(spikes), get_dendr_spike_det_dyn_ref(-50.0,10.0,100.0), accs, seed=seed, learn=learn, neuron=neuron)
                
    dump(accums[0].res['weight'][-1]/accums[0].res['weight'][0],p['ident'])

params = OrderedDict()
params['alpha'] = [-54.0]
params["beta"] = [0.1]
params["g_L"] = [0.03]
params["r_max"] = [0.071]
params["freq"] = np.array([1.0,10.0,20.0,40.0,50.0])
params["delta"] = np.array([-10.0,10.0])

file_prefix = 'stdp_figure_sjostrom'

do(task, params, file_prefix, prompt=False, withmp=True)
