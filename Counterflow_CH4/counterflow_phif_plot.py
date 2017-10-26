
import numpy as np
import glob
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def cm2inch(*tupl):
    inch = 2.54
    return tuple(i/inch for i in tupl)

var_names = ['T','C_o','C_4spe','C_2spe','Q']

# plot
# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',family='serif')
# figure and axes parameters
# total width is fixed, for one column plot
plot_width      =9.0
margin_left     =1.8
margin_right    =0.5
margin_bottom   =1.2
margin_top      =1.0
space_width     =0.3
space_height    =1.0
ftsize          =12

subplot_width = plot_width-margin_left-margin_right
subplot_height = subplot_width * 0.9

plot_height = subplot_height+margin_bottom+margin_top

figs = [None] * len(var_names)
axes = [None] * len(var_names)

# generate figure and axes
for i, var in enumerate(var_names):
    figs[i], axes[i] = plt.subplots(figsize=cm2inch(plot_width,plot_height))

for case in glob.glob('*.xml'):

    flame = case[:-4]
    flame_params = flame.split('_')
    phi_str = flame_params[3][4:]

    file_name = '{}.dat'.format(flame)
    data = np.genfromtxt(file_name,skip_header=3,names=True)

    for i, var in enumerate(var_names):
        axes[i].plot(data['Z1'],data[var],label=phi_str,linewidth=1)

for i, var in enumerate(var_names):
    if i ==0 :
        axes[i].set_xlim(0.0,1.0)
    else:
        axes[i].set_xlim(0.03,0.08)
    axes[i].set_xlabel('$Z$',fontsize=ftsize)
    axes[i].set_ylabel('${}$'.format(var),fontsize=ftsize)
    axes[i].legend(fontsize=ftsize,frameon=False)
    
    figs[i].subplots_adjust(left = margin_left/plot_width,
            bottom = margin_bottom/plot_height,
            right = 1.0-margin_right/plot_width,
            top = 1.0-margin_top/plot_height,
            wspace = space_width/plot_width,
            hspace = space_height/plot_height)

    figs[i].savefig('phif_a100_{}.pdf'.format(var))
