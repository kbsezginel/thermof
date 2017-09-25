from setuptools import setup, find_packages


setup(
    name="thermof",
    version="0.1.2",
    description="Thermoelectrically entangled MOFs",
    author="Kutay B. Sezginel",
    author_email="kbs37@pitt.edu",
    install_requires=['pytest',
                      'pyyaml',
                      'matplotlib',
                      'periodictable',
                      'ase'],
    dependency_links=['git+ssh://git@github.com/kbsezginel/lammps_interface.git']
    include_package_data=True,
    packages=find_packages()
)
