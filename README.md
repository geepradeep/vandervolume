[![Build Status](https://travis-ci.org/geepradeep/vandervolume.svg?branch=master)](https://travis-ci.org/geepradeep/vandervolume)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4018406.svg)](https://doi.org/10.5281/zenodo.4018406)

# vandervolume
Compute the van der Waals volume of molecules using brute-force MC simulated darts. Why? Because why not?

Prerequisites can be installed via:

    pip install joblib tqdm --upgrade matplotlib

Usage:

    python vandervolume.py <input.xyz>

Change the parallel_flag from False to True if needed (example: very large molecules).

Default # of iterations = 10000. Increase for larger molecules.

Example:

    > python vandervolume.py oxygen.xyz
    100%|██████████| 10000/10000 [00:00<00:00, 26070.65it/s]
    Approximate volume is 14.75

![](oxygen.png "Image output from matplotlib")

License: The unlicense. Use as you wish.
Citation: Gurunathan, P. K., https://github.com/geepradeep/vandervolume/, [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4018406.svg)](https://doi.org/10.5281/zenodo.4018406)
