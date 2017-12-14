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
                      'ase'],
    entry_points={
        'console_scripts': [
            'thermof-read=thermof.cli.thermof_read:main',
            'thermof-write=thermof.cli.thermof_write:main',
        ]
    }
)
