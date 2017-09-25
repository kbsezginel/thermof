from setuptools import setup, find_packages


setup(
    name="thermof",
    version="0.1.2",
    description="Investigating thermal conductivity of MOFs using Lammps",
    author="Kutay B. Sezginel",
    author_email="kbs37@pitt.edu",
    install_requires=['pytest',
                      'pyyaml',
                      'matplotlib',
                      'periodictable',
                      'ase'],
    dependency_links=['http://github.com/kbsezginel/lammps_interface/tarball/master'],
    include_package_data=True,
    packages=find_packages()
)
