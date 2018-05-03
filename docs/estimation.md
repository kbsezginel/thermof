---
layout: default
date:   2018-05-03
---
Automated Estimation of Thermal Conductivity
============================================

I have tried 3 following methods to estimate *k* automatically:
- k<sub>0</sub>: Linear fit between 15 - 30 ps (6000 - 12000 timesteps)
- k<sub>1</sub>: Exponential fit between 0 - 5 ps (0 - 2000 timesteps)
- k<sub>2</sub>: Exponential fit between 0 - 10 ps (0 - 2000 timesteps)
- k<sub>3</sub>: Exponential fit between 0 - 50 ps (0 - 2000 timesteps)

You can see in the plot below how these fits are done:

<p align="center"> <img src="assets/img/estimation/ZASJAG_clean.png"> </p>

<p align="center"> <img src="assets/img/estimation/ZASWOF_clean.png"> </p>


Comparison with Manual Estimation
---------------------------------

<p>
  <details>
    <summary>Click here for more</summary>
    <b>Manually read k values vs automatically calculated k values for each direction (x, y, z) and for the whole range (0 - 12 W/mK).</b>
    <p align="center"> <img src="assets/img/estimation/kcomparison-012.png"> </p>
    <b>Manually read k values vs automatically calculated k values for each direction (x, y, z) zoomed in (0 - 1.5 W/mK).</b>
    <p align="center"> <img src="assets/img/estimation/kcomparison-01.png"> </p>
  </details>
</p>


Thermal Conductivity Distribution
----------------------------------
<p>
  <details>
    <summary>Click here for more</summary>
    <p align="center"> <img src="assets/img/estimation/kdistribution.png"> </p>
  </details>
</p>

Thermal Conductivity vs MOF Properties
--------------------------------------

<p>
  <details>
    <summary>Click here for more</summary>
    <p align="center"> <img src="assets/img/estimation/kproperties-x.png"> </p>
    This plot is for thermal conudctivity in x direction. Other directions show the same trends.
  </details>
</p>

Displacement Analysis for MOFs with Unphysical Thermal Conductivities
---------------------------------------------------------------------

<p>
  <details>
    <summary>Click here for more</summary>
    I separated the MOFs that have a k estimation between 0 - 20 W/mK and the MOFs where k is not calculated
    or k is calculated out of this range. Then I calculated the mean displacement (MD) for one of the framework atoms
    for each MOF using the formula below:
    <p align="center"> <img src="assets/img/estimation/mean-displacement-formula.png" height="60"> </p>

    I mainly did this to see whether MOFs with unphysical k values have higher displacement
    that MOFs with normal k values. For some of the MOFs we saw that the framework was drifting which was causing
    unphysically high k values.

    Even though there is some difference between the displacements the difference is not much.
    More analysis is required.
    <p align="center"> <img src="assets/img/estimation/kdisplacement-normal.png"> </p>
    <p align="center"> <img src="assets/img/estimation/kdisplacement-unphysical.png"> </p>
    This plot is for thermal conudctivity in x direction. Other directions show the same trends.
  </details>
</p>
