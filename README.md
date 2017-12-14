[![Build Status](https://travis-ci.org/kbsezginel/thermof.svg?branch=master)](https://travis-ci.org/kbsezginel/thermof)
[![codecov](https://codecov.io/gh/kbsezginel/thermof/branch/master/graph/badge.svg)](https://codecov.io/gh/kbsezginel/thermof)

Thermal transport in MOFs (thermof)
===================================
Investigating thermal transport in metal-organic frameworks.

Installation
------------
First, install [lammps_interface](https://github.com/kbsezginel/lammps_interface) Python package:

```bash
git clone https://github.com/kbsezginel/lammps_interface
cd lammps_interface
python setup.py install
```

Then, clone and install the TherMOF repository:

```bash
git clone https://github.com/kbsezginel/thermof.git
cd thermof
pip install -e .
```

Usage
-----
TherMOF library can be used to initialize, run, and analyze simulation results to investigate thermal transport in porous crytals. Here sample files for an idealized cubic MOF along with an interpenetrated version are provided (see Figure 1). Using these files Molecular Dynamics simulations can be run with [Lammps].

### Command-line interface

TherMOF can be used with the command-line interface (CLI) provided in this repository. The CLIs are installed as console scripts by default. Alternatively, you can find the scripts in `thermof/cli`.

#### Initializing LAMMPS simulations

A thermal conductivity calculation input files for LAMMPS can be generated for a `cif` file with the `thermof_write` CLI as follows:
```
thermof_write myMOF.cif
```
This would create a directory (`myMOF`) in the same directory as the cif file containing LAMMPS input files. Currently only `P1` symmetry is accepted. An example cif file can be found in `thermof/sample/MOF5.cif`.


Using the `--help` flag more information about the CLI (such as selecting force field, cell size) can be obtained:
```
thermof_write --help
```

#### Analyzing LAMMPS simulations

After running LAMMPS simulations the resuts can be analyzed and plotted with the `thermof_read` CLI as follows:
```
thermof_read /path/to/simulation
```
Here `/path/to/simulation` is the name of the directory that contains simulation results.

Using the `--help` flag more information about the CLI (such as selecting plots, parameters) can be obtained:
```
thermof_read --help
```

### Sample
Sample [Lammps] input files for thermal conductivity calculations can be found in `thermof/sample`

-   in3_ipmof.cond.sample: Interpenetrated MOF simulation parameters with 3D thermal flux
-   in3_single.cond.sample: Single MOF simulation parameters with 3D thermal flux
-   in_ipmof.cond.sample: Interpenetrated MOF simulation parameters with 1D thermal flux
-   lammps_ipmof.data.sample: Interpenetrated MOF structure file
-   lammps_ipmof_metal.data.sample: Interpenetrated MOF with differemt corner atoms structure file
-   lammps_single.data.sample: Single MOF structure file
-   lammps_single_metal.data.sample: Single MOF with differemt corner atoms structure file
-   lammps_qsub.sh.sample: Job submission script for lammps simulations on [Frank]

### Notebooks
Example jupyter notebooks can be found in `/notebooks`

-   change_trajectory: Change xyz trajectory atoms names
-   initialize: Initialize Lammps simulation files according to selected simulation parameters
-   interpenetrate: Create interpenetrated structure
-   read_simulation: Read and plot thermal conductivity Lammps simulation results

### Publications

1. [Babaei, Hasan, and Christopher E. Wilmer. **"Mechanisms of heat transfer in porous crystals containing adsorbed gases: Applications to metal-organic frameworks."** *Physical review letters* 116.2 (2016): 025902.](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.116.025902)
2. [Babaei, Hasan, Alan JH McGaughey, and Christopher E. Wilmer. **"Effect of pore size and shape on the thermal conductivity of metal-organic frameworks."** *Chemical Science* 8.1 (2017): 583-589.](http://pubs.rsc.org/-/content/articlehtml/2016/sc/c6sc03704f)
3. Sezginel, Kutay B., Patrick Asinger, Hasan Babaei, and Christopher E. Wilmer. **"Effect of interpenetration on the thermal conductivity of metal-organic frameworks."** *submitted*

-------------------------------------------------------------------------
[Lammps]: http://lammps.sandia.gov/ "Lammps home page"
[Frank]: http://core.sam.pitt.edu/frank "Frank home page"
