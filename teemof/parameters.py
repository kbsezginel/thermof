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
              dpi=300,
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
    'hist': dict()
}
