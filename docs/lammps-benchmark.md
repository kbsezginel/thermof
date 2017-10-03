---
layout: default
title:  "Lammps Benchmarking"
date:   2017-09-20
---
[Running Lammps](http://lammps.sandia.gov/doc/Section_start.html#running-lammps)

[How to make your Lammps run faster](https://hpc.nrel.gov/users/software/applications/lammps/how-to-make-your-lammps-run-faster)

I did some benchmarking to see how I can improve Lammps simulation speed. The sources above were quite helpful.
I tried using `srun` as well as `mpirun` and I also tried using the `export OMP_NUM_THREADS` command.
For all trials I used `mpi` cluster in `H2P` with 2 nodes and 8 processors per node.
For me the fastest was just using `mpirun` with total number of tasks:
```
mpirun -np ${SLURM_NTASKS} lmp_mpi -in in.MOF5 > lammps_out.txt

>>> Total wall time: 0:08:08
```

Close second was assigning the `OMP_NUM_THREADS` variable:
```
export OMP_NUM_THREADS=2
mpirun -np 8 lmp_mpi -in in.MOF5 > lammps_out.txt

>>> Total wall time: 0:09:49
```

The tests were done for calculating thermal conductivity of MOF5. For other types of simulations results may differ.
