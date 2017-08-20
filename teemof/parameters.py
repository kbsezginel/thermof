"""
Parameters for reading and plotting thermal flux
"""

k_parameters = dict(kb=0.001987,
                    conv=69443.84,
                    dt=5,
                    volume=80 * 80 * 80,
                    temp=300,
                    prefix='J0Jt_t',
                    isotropic=False,
                    average=True,
                    read_info=False,
                    read_thermo=False)

plot_parameters = {
    'k': dict(limit=(0, 2000),
              size=(20, 10),
              fontsize=14,
              dpi=200,
              avg=True,
              cmap='Spectral_r',
              save=None,
              legendloc=(1.02, 0),
              ncol=1,
              title=None,
              xlabel='Time',
              ylabel='k (W/mK)'),
    'thermo': dict(),
    'runs': dict(),
    'hist': dict(subplot=(2, 5),
                 size=(14, 6),
                 dpi=200,
                 space=(0.2, 0.1),
                 grid_size=10,
                 bin_size=1,
                 vmax=25,
                 vmin=0.01,
                 cmap='YlOrRd',
                 grid_limit=10,
                 ticks=False,
                 cbar=[0.92, 0.135, 0.02, 0.755],
                 save=None,
                 selections=None)
}
