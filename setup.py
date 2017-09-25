from setuptools import setup, find_packages


setup(
    name="thermof",
    version="0.1.2",
    description="Investigating thermal conductivity of MOFs using Lammps",
    author="Kutay B. Sezginel",
    author_email="kbs37@pitt.edu",
    url='https://github.com/kbsezginel/thermof',
    include_package_data=True,
    packages=find_packages(),
    install_requires=['pytest',
                      'pyyaml',
                      'matplotlib',
                      'periodictable',
                      'ase',
                      'lammps_interface'],
    dependency_links=['https://github.com/kbsezginel/lammps_interface/tarball/master#egg=package-1.0'],
    zip_safe=False
)
