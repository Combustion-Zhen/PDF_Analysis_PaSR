"""
Zhen Lu 2017/11/09

plot scattering of c vs. Z, colored by FI
"""

import os
import copy
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from counterflow_file import *

models = np.array([['IEM','EMST'],
                   ['IEMHYB','EMSTHYB']])
modeln = np.array([['IEM','EMST'],
                   ['IEM-FI','EMST-FI']])

time_res = [1.e-2,]
mix_res_ratio = [0.2,]
equiv_ratio_f = [4.76,]
equiv_ratio = [1.0,]
Zf_variance = [0.1,]
dtmix = [0.01,]

params = {}
params['MIX'] = None
params['tres'] = None
params['tmix'] = None
params['eqv'] = None
params['Zfvar'] = None
params['dtmix'] = None
params['phif'] = None

dst = '.'
dat_name = 'particle_fi.dat'
full_name = 'fifull.op'

# plot
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 14.4
margin_left   = 1.2
margin_right  = 0.1
margin_bottom = 0.8
margin_top    = 0.8
space_width   = 1.0
space_height  = 1.5
ftsize        = 7

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

num_cols = 2
num_rows = 2

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.5

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

# loop over all parameters
for tres in time_res:
    params['tres'] = tres
    for tmix_ratio in mix_res_ratio:
        tmix = tmix_ratio*tres
        params['tmix'] = tmix_ratio
        for phi in equiv_ratio:
            params['eqv'] = phi
            for var in Zf_variance:
                params['Zfvar'] = var
                for dt in dtmix:
                    params['dtmix'] = dt
                    for phif in equiv_ratio_f:
                        params['phif'] = phif

                        fig, ax = plt.subplots(
                                num_rows,num_cols,
                                sharex=True,sharey=True,
                                figsize=cm2inch(plot_width,plot_height))

                        for i in range(num_rows):
                            for j in range(num_cols):
                                model = models[i,j]
                                params['MIX'] = model
                                case = params2name(params)
                                file_name = '/'.join([case,dat_name])
                                if os.path.exists(file_name):
                                    FI = np.genfromtxt(file_name)
                                else:
                                    print(file_name)
                                    FI = np.zeros((1000,3))

                                # npts limit
                                ntotal = FI.shape[0]
                                #if ntotal > 5000:
                                #    idx = np.random.randint(0,ntotal,5000)
                                #    FI = FI[idx,:]

                                if ntotal < 1000:
                                    file_name = '/'.join([model,
                                                          case,
                                                          full_name])
                                    FI = np.genfromtxt(file_name,
                                                       usecols=(1,2,3))
                                    idx = np.random.randint(0,FI.shape[0],1000)
                                    FI = FI[idx,:]

                                cplt = ax[i,j].scatter(
                                        FI[:,1],FI[:,2],c=FI[:,0],
                                        vmin=0,vmax=1,
                                        marker='.',
                                        cmap='coolwarm')

                                ax[i,j].text(0.25,0.25,modeln[i,j])
                                ax[i,j].set_ylim(0,0.31)
                            ax[i,0].set_ylabel('$c$')

                        ax[0,0].set_xlim(0,0.32)
                        ax[0,0].set_ylim(0,0.3)


                        for j in range(num_cols):
                            ax[-1,j].set_xlabel('$Z$')
                            ax[0,j].tick_params('x',length=0)
                        for j in range(num_rows):
                            ax[j,-1].tick_params('y',length=0)

                        fig.subplots_adjust(
                                left = margin_left/plot_width,
                                bottom = margin_bottom/plot_height,
                                right = 1.0-margin_right/plot_width,
                                top = 1.0-margin_top/plot_height,
                                wspace = space_width/plot_width,
                                hspace = space_height/plot_height
                                )

                        fig.text(6/plot_width,(plot_height-0.6)/plot_height,
                                 ''.join([
                                     r'$\tau_{\mathrm{res}}=$',
                                     '{:g}'.format(tres),
                                     r'$\;\mathrm{s}\quad$',
                                     r'$\tau_{\mathrm{mix}}=$',
                                     '{:g}'.format(tmix*1000.),
                                     r'$\;\mathrm{ms}\quad$',
                                     r'$\varphi=$',
                                     '{:g}'.format(phi),
                                     r'$\quad$',
                                     r'$\varphi_r=$',
                                     '{:g}'.format(phif),
                                     r'$\quad$',
                                     r'$\eta_{Z,r}=$',
                                     '{:g}'.format(var)
                                     ]))

                        cax = fig.add_axes([2.1/plot_width,
                                            (plot_height-0.7)/plot_height,
                                            3/plot_width,
                                            0.15/plot_height])

                        clb = fig.colorbar(cplt,cax=cax,orientation='horizontal')
                        clb.set_ticks([0, 0.25, 0.5, 0.75, 1.0])
                        clb.set_ticklabels(['-1','-0.5','0','0.5','1'])

                        cax.tick_params(axis='x',length=3)
                        cax.xaxis.set_ticks_position('top')
                        fig.text(1.4/plot_width,
                                 (plot_height-0.6)/plot_height,
                                 '$\mathrm{FI}$')

                        plot_params = copy.deepcopy(params)
                        del plot_params['MIX']
                        del plot_params['tres']
                        del plot_params['dtmix']
                        del plot_params['phif']
                        del plot_params['Zfvar']
                        plot_name = params2name(plot_params)

                        fig.savefig('{}/fig_zc_scatter_{}.pdf'.format(dst,plot_name))
                        plt.close('all')
