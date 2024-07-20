# JUPITER Benchmark Suite: ICON

[![DOI](https://zenodo.org/badge/831374575.svg)](https://zenodo.org/badge/latestdoi/831374575) [![Static Badge](https://img.shields.io/badge/DOI%20(Suite)-10.5281%2Fzenodo.12737073-blue)](https://zenodo.org/badge/latestdoi/764615316)

This benchmark is part of the [JUPITER Benchmark Suite](https://github.com/FZJ-JSC/jubench). See the repository of the suite for some general remarks.

This repository contains the ICON benchmark. [`DESCRIPTION.md`](DESCRIPTION.md) contains details for compilation, execution, and evaluation.

[ICON](https://www.icon-model.org/) (ICOsahedral Non-hydrostatic model) originated as a joint project for operational numerical weather forecasting and climate research by the German Weather Service (DWD) and the Max Planck Institute for Meteorology (MPI-M), and is presently further developed and maintained together with the German Climate Computing Center (DKRZ), and the Karlsruhe Institute of Technology (KIT). 

The ICON benchmark provides a global forecast simulation in model resolution R02B09 (5 km grid point distance) and R02B10 (2.5 km grid point distance). 

The source code of ICON is included in the `./src/` subdirectory as a submodule from the ICON repository at [gitlab.dkrz.de/icon/icon-model](https://gitlab.dkrz.de/icon/icon-model).