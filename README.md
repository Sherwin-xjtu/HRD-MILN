# HRD-MILN

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/Sherwin-xjtu/PEcnv/edit/master/README.md)

HRD-MILN: Accurately estimate tumor homologous recombination deficiency status from targeted panel sequencing data


## Table of Contents

- [Features](#features)
- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Features

1. HRD-MILN is among the first practical tool for estimating HRD status from targeted panel sequencing data, and could benefit the clinical applications.
2. HRD-MILN developed and incorporated a multi-instance learning-based model, which solve the key computational issue that, it is hard to model the unclear/non-significant associations between a LOH mutation on genomic level and the HRD status on patient level. 
3. By establishing the intrinsic associations among HRD biomarkers and HRD status, HRD-MILN is much less sensitive to false positive mutation calls (e.g. LOHs) than the existing methods.
4. HRD-MILN is not only efficiently applicable to targeted panel sequencing data, but works well for whole exome sequencing and whole genome sequencing data as well. 

## Background

Homologous recombination deficiency (HRD) is a critical feature guiding drug and treatment selection, mainly for ovarian and breast cancers. As it cannot be directly observed, HRD status is estimated on a small set of genomic instability features from sequencing data. The existing methods often perform poorly when handling targeted panel sequencing data; however, the targeted panel is the most popular sequencing strategy in clinical practices. Thus, we proposed HRD-MILN to overcome the computational challenges from targeted panel sequencing. HRD-MILN incorporated a multi-instance learning framework to discover as many loss of heterozygosity (LOH) associated with HRD status to cluster as possible. Then the HRD score is obtained based on the association between the LOHs and the cluster in the sample to be estimated, and finally, the HRD status is estimated based on the score.

## Install
Uncompress the installation zip:

    $ cd /my/install/dir/
    $ unzip /path/to/HRD-MILN.zip
    

## Usage


```sh
$ python hrdmiln.py -i input.csv -o out.csv
```


## Maintainers

[@Sherwin](https://github.com/Sherwin-xjtu).

## Contributing

Feel free to dive in! [Open an issue](https://github.com/Sherwin-xjtu/PEcnv/issues/new) or submit PRs.

## License

[MIT](LICENSE) © Sherwin


