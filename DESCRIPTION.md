# ICON

## Purpose

The ICON atmosphere model consists of a non-hydrostatic dynamical core, a
tracer transport model, and parametrization packages for numerical weather
prediction, and climate simulations. For the spatial
discretization the ICON model uses an icosahedral grid and a hybrid height-based vertical
coordinate. The ICON code is written in Fortran and C and parallelized with MPI and OpenMP. A GPU-enabled variant of the ICON code has been developed jointly by ETHZ, MPI-M, DWD, and MeteoSwiss.
ICON employs triangular and hex-/pentagonal grids arising from iterative subdividing of the edges of the icosahedron (polyhedron with 20 triangular faces) mapped to the globe.

The ICON NWP (Numerical Weather Prediction) benchmark provides a global simulation with the following two sub-benchmarks:

**Sub-Benchmark 1 (R02B09)**:

- Global Simulation
- Model resolution: R02B09, 90 vertical levels
- Grid point distance: 5 km
- Number of grid cells: 20971520 x 90
- Time step: 40 sec
- Simulated time period: 1 day (2018-04-01, 00 UTC to 2018-04-02, 00 UTC) (2160 time steps)
- output written every three hours for 3D variables and every 30 minutes for 2D variables, no restart files

**Sub-Benchmark 2 (R02B10)**:

- Global Simulation
- Model resolution: R02B10, 90 vertical levels
- Grid point distance: 2.5 km
- Number of grid cells: 83886080 x 90
- Time step: 20 s
- Simulated time period: 2 h (2021-07-12, 00 UTC to 2021-07-12, 02 UTC) (360 time steps)
- output written every three hours for 3D variables and every 30 minutes for 2D variables, no restart files

In addition, further datasets for smaller test cases are provided for evaluation purposes, R02B04, R02B06, and R02B07.

## Source

The ICON benchmark is delivered as `icon-bench.tar.gz`. The input data is delivered separately as `icon-dataset.tar.gz`; the sample datasets are provided in `icon-dataset-sample.tar.gz`.

The 2024.01 open source release of ICON is available in this repostiory as a git submodule in the direcotry `src/icon`, **as a git submodule**. Make sure to either recursively clone this repository, or to use the `git submodule init`  and `git submodule update` commands.
An up-to-date build configuration wrapper for JUWELS Booster is also provided with `src/juwels_booster.gpu.ompi_nvhpc-24.1`, as well as a patch to build ICON version `2024.01` for GPUs with `src/2024.01-lzacc_undefined.patch`.



## Building

While ICON can also be built to run on CPUs, this benchmark is made for the ICON GPU version.

ICON depends on other packages: NVIDIA HPC SDK, OpenMPI, netCDF-Fortran, Python, CUDA, ecCodes, CMake.

On JUWELS Booster, the following modules have been loaded: NVHPC/24.1-CUDA-12 OpenMPI/4.1.6 ecCodes/2.31.0 netCDF-Fortran/4.9.2 CMake/3.26.3

### Configuration

To configure the ICON build, a configure file needs to be used. The source already consists of configure files for the most commonly used HPC machines across Europe (JSC, CSCS, ECMWF, DKRZ, and others), with different versions corresponding to different MPI implementations and compilers. Please adapt the one you feel is closest to your hardware and software stack, and if you are unsure, please resort to using the ones in config/generic. Please modify the configure file according to your own system, to ensure that the correct modules and libraries are used. 

The configure file for JUWELS Booster is provided in `src/juwels_booster.gpu.ompi_nvhpc-24.1` and needs to be copied into the `src/icon/config/jsc` folder.

### Patching

To build the ICON 2024.01 release for GPUs, you will need to apply the patch `src/2024.01-lzacc_undefined.patch` to the ICON releae in `src/icon/`.

```
$ cd src/icon
$ patch -p1 < ../2024.01-lzacc_undefined.patch
```

### Compilation

On JUWELS Booster, the script provided in `src/juwels_booster.gpu.ompi_nvhpc-24.1` needs to be copied into the `src/icon/config/jsc` folder.

ICON will then be automatically build as part of the JUBE benchmark execution.

## Execution

The necessary files for execution can be found in the `benchmark/` directory, once for execution with JUBE and once for execution without JUBE.

The benchmark consists of two sub-benchmarks. Sub-benchmark 1 is for R02B09 and sub-benchmark 2 for R02B10. The individual sub-benchmark can be selected by using different grids, where grid ID 3 is for R02B09 and grid ID 4 is for R02B10.

| Sub-Benchmark | Resolution | Grid ID | Reference Nodes JUWELS Booster | JUBE Tag |
| ------------- | ---------- | ------- | ------------------------------ | -------- |
| 1             | R02B09     | 3       | 120                            | `R02B09` |
| 2             | R02B10     | 4       | 300                            | `R02B10` |

Each sub-benchmark has the following parameters to be chosen for best performance by the benchmarker:

* `nproma`: The compute domain in each MPI process is divided into blocks of fixed lengths (`nproma`), determining the length of the inner loop.
* `rrtmgp_chunk`: This parameter is responsible for sub-chunking within the radiation scheme
* `grid`: This parameter determines the grid used for the respective benchmark and needs to be either 3 or 4

To utilize GPUs best, `nproma` should be set as large as possible, ideally resulting in a local block per MPI process (reducing host-device memory traffic). On the other hand, the local domain (and therefore `nproma`) gets smaller with larger numbers of MPI processes. In general, `nproma` should be optimized according to the number of MPI processes while at the same time maximizing `rrtmgp_chunk` according to the memory available. The number of nodes and MPI processes are further free parameters, of course.

Actual values used on JUWELS Booster can be found for JUBE in `default.xml` and for the manual case in `exp.exabench_gpu_JUWELS.run`.

For configuration details for the sample data sets, please refer to the definitions in the JUBE script at `benchmark/jube/default.xml`.

### JUBE

Start `jube run benchmark/jube/default.xml --tag [R02B09|R02B10]`, which launches the ICON run script `exp.exabench_gpu.run`. The tag (`--tag`) is given to enable the respective sub-benchmark. JUBE will build ICON, adapt the runscript and submit the benchmarks to the batch system.

The benchmarks can be analysed with `jube analyse` and `jube result` to extract different timers from the ICON standard output file.

For the sample datasets, the tags `R02B04`, `R02B06`, `R02B07` exist in the JUBE script.

### Manual

To start the benchmark manually execute the ICON runscript `manual/exp.exabench_gpu.run` after adapting variables to the environment. Beyond the variables mentioned above (`#GRID#` for the grid configuration (3 or 4), `#NPROMA#`, and `#RRTMGPCHUNK#`), also `#RUNDIR#` and `#ICONDIR#` need to be adapted according to your needs.

Actual values used on JUWELS Booster for these parameters can be extracted from the run script `exp.exabench_gpu_JUWELS.run`.

## Verification

Margins for the most common meteorological parameters have been defined and the atmospheric parameters at the end of the simulation period should lie within these margins. The verification step creates a file `evaluation.out` in which `Verification has run successfully` must be returned.

### JUBE

Verification is triggered by continuing the JUBE run:

```
jube continue run --id <id>
```

### Manual

A Python script `aux/evaluate.py` is provided to verify a certain output file for a given grid (with Grid ID 3 for R02B09 and Grid ID 4 for R02B10):

```
python evaluate.py <path to Output> <Grid ID>
```

## Result

Execution of the benchmark creates a logfile (`job.err`). At the end of the logfile, a timer report is given, which is used for evaluation. For the benchmark, maximum time of the integrate\_nh category will be evaluated (`intnhmax` or integrate\_nh\_max\[s\]); `intnhmax` is the metric of choice for the benchmark.

This value is the time spent by the slowest node during the forecast loop of the simulation (without I/O and initial model set-up).

### JUBE

Using `jube analyse` and a subsequent `jube result` prints an overview table
with the number of nodes, total runtime, **`intnhmax`**, and some further values (like `intnhmin`, `exch_data_[max|min]`, and `wrt_output_[max|min]`.

### Manual

The benchmark metric is displayed as "_total max (s)_" for _integrate\_nh_ is to be extracted from the logfile.

## Baseline

For sub-benchmark 1 (R02B9), the baseline configuration must be chosen such that the simulation time metric (in seconds), reported as `intnhmax`, is below or equal to 400 s. On the JUWELS Booster system at JSC, this value is reached with 120 nodes or 480 MPI tasks.  (Table displayed shortened.)

| Nodes | total time [s] | intnhmax time [s] | exch_data_max time [s] | wrt_output_max time [s] |
| ----- | -------------- | ----------------- | ---------------------- | ----------------------- |
| 120   | 1101.8         | 393.1             | 97.3                   | 696.8                   |

For sub-benchmark 2 (R02B10), the baseline configuration must be chosen such that the simulation time metric `intnhmax` is below of or equal to 100 s. This value was reached on JUWELS Booster on 300 nodes (1200 MPI tasks). (Table displayed shortened.)

| Nodes | total time [s] | intnhmax time [s] | exch_data_max time [s] | wrt_output_max time [s] |
| ----- | -------------- | ----------------- | ---------------------- | ----------------------- |
| 300   | 563.8          | 97.9              | 256.0                  | 465.3                   |


