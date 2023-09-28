# dc2-replication-workshop
A continer for the code (and data) used for creating a small version of the DC2 butler repository on a VM.

![image](https://github.com/lsst-dm/dc2-replication-workshop/assets/12162156/3a82adbe-059f-4658-ba77-9da0d43f4143)
BE EXTREMELY CAREFUL: If you enter the correct admin passwords for a database server, 
```diff
- the script WILL DELETE your existing database. 
```
So make sure you know what you're doing, before playing with any code found in this repository.


### Data:
You'll notice that the script refers to multiple folder names. Below you can see the content of each of them at the time this script was used for restoring a hetrogenous version of the DC2:
- /repo/dc2_ncsa_backup/
  A (possibly broken) back up *of the directory* that contained dc2 data on disk, in the old days:
  ```
  /repo/dc2_ncsa_backup/
  ├── 2.2i
  │   ├── calib
  │   │   ├── DM-30694
  │   │   │   ├── curated
  │   │   │   └── unbounded
  │   │   └── PREOPS-301
  │   │       └── unbounded
  │   └── raw
  │       └── all
  │           └── raw
  ├── butler.yaml
  └── u
      └── nsedaghat
          ├── Dataset0.1.1-sciCalexps
          │   └── 20220521T042355Z
          ├── DLDataset0.0
          │   ├── 20220108T003039Z
          │   ├── 20220112T182518Z
          │   ├── 20220119T010921Z
          │   └── 20220119T130340Z
          ├── DLDataset0.1.1-diffs
          │   └── 20220522T064105Z
          └── DLDataset0.1.1-templates
              └── 20220522T031531Z
  ```
  
- /repo/raw/
  butler-exported set of .yaml files, only raws, from the current USDF version of the repository -- contains no actual data files, a.k.a. artifacts.
  ```
  /repo/raw
  ├── _export_000.yaml
  ├── _export_001.yaml
  ├── _export_002.yaml
  ├── _export_003.yaml
  ├── _export_004.yaml
  ├── _export_005.yaml
  ├── _export_006.yaml
  ├── _export_007.yaml
  ├── _export_008.yaml
  ...
  ```

- /repo/usdf_export_calib/
  butler-exported set of .yaml files for calibration datasets -- contains no actual data files, a.k.a. artifacts.
  ```
  /repo/usdf_export_calib
  ├── bfk
  │   ├── _export_000.yaml
  │   ├── _export_000.yaml.mod
  │   └── _files.txt
  └── camera
      ├── _export_000.yaml
      ├── _export_000.yaml.mod
      └── _files.txt
  ```

- /repo/usdf_export_full_latest
  Similar export, all dataset types, this time preserving the data collections structure.
  ```
  ├── apdb_marker
  ├── assembleCoadd_config
  ├── assembleCoadd_log
  ├── assembleCoadd_metadata
  ├── bfk
  ├── bias
  ├── calexp
  ├── calexpBackground
  ├── calibrate_config
  ├── calibrate_log
  ├── calibrate_metadata
  ├── cal_ref_cat_2_2
  ├── camera
  ├── characterizeImage_config
  ├── characterizeImage_log
  ...

  ```

- /repo/dp02_raws
  This is a specific set of raws corresponding to the above backed up run collections (u/nsedaghat/D*).
  It does contain the corresponding fits files (artifacts) too.
  Note that coming up with this specific subset was an extra-complicated process, involving a cross-machine, cross-butler transfer, while the source was a half-way restored /repo/dc2. The provided scripts in this package do not generate such output.
  ```
  ├── 2.2i
  │   └── raw
  │       └── all
  │           └── raw
  │               ├── 20240805
  │               ├── 20240807
  │               ├── 20240808
        ...
  │               ├── 20261230
  │               └── 20261231
  └── export_raw.yaml
  ```
