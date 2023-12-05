##
import os
import glob
import lsst.daf.butler as dafButler

butler = dafButler.Butler('/dc2/dc2')
## First, get the number of calexps, templates in the 0.1.1 dataset.

# Count the backed up calexp fits files on the disk.
n_calexps_on_disk = len(glob.glob('/repo/dc2_ncsa_backup/u/nsedaghat/Dataset0.1.1-sciCalexps/20220521T042355Z/**/*fits', recursive=True))
print('Number of backed-up calexps on disk: ', n_calexps_on_disk)


# Now number of calexps that butler gives us.
n_calexps_in_butler = butler.registry.queryDatasets('calexp', collections=['u/nsedaghat/Dataset0.1.1-sciCalexps/20220521T042355Z']).count()
print('Number of calexps through butler: ', n_calexps_in_butler)

# And number of regenerated calexps.
n_calexps_regenerated = butler.registry.queryDatasets('calexp', collections=['u/nsedaghat/RegeneratedCalexps_w_2022_20_nobfk/20231002T214649Z']).count()
print('Number of regenerated calexps: ', n_calexps_regenerated)

# Count the backed up templates fits files on the disk.
n_templates_on_disk = len(glob.glob('/repo/dc2_ncsa_backup/u/nsedaghat/DLDataset0.1.1-templates/20220522T031531Z/**/*fits', recursive=True))
print('Number of backed-up templates on disk: ', n_templates_on_disk)

# Now number of templates that butler gives us.
n_templates_in_butler = butler.registry.queryDatasets('goodSeeingDiff_templateExp', collections=['u/nsedaghat/DLDataset0.1.1-templates/20220522T031531Z']).count()
print('Number of templates through butler: ', n_templates_in_butler)

## Now count only those with exposure > 1M. Only using butler.
n_calexps_in_butler_1M = butler.registry.queryDatasets('calexp', collections=['u/nsedaghat/Dataset0.1.1-sciCalexps/20220521T042355Z'], where="instrument='LSSTCam-imSim' AND skymap='DC2' AND exposure > 1000000").count()
print('Number of calexps through butler with exposure > 1M: ', n_calexps_in_butler_1M)

n_regenerated_calexps_1M = butler.registry.queryDatasets('calexp', collections=['u/nsedaghat/RegeneratedCalexps_w_2022_20_nobfk/20231002T214649Z'], where="instrument='LSSTCam-imSim' AND skymap='DC2' AND exposure > 1000000").count()
print('Number of regenerated calexps with exposure > 1M: ', n_regenerated_calexps_1M)

n_templates_in_butler_1M = butler.registry.queryDatasets('goodSeeingDiff_templateExp', collections=['u/nsedaghat/DLDataset0.1.1-templates/20220522T031531Z'], where="instrument='LSSTCam-imSim' AND skymap='DC2' AND exposure > 1000000").count()
print('Number of templates through butler with exposure > 1M: ', n_templates_in_butler_1M)

# ## Show a histogram of the exposure numbers for calexps.
# # For this let's query dataids, create a list of exposures, and then plot the histogram.
# calexp_dataids = butler.registry.queryDataIds(['exposure'],
#                                               datasets=['calexp'],
#                                               collections=['u/nsedaghat/Dataset0.1.1-sciCalexps/20220521T042355Z'],
#                                               where="instrument='LSSTCam-imSim' AND skymap='DC2'")
# exposures = []
# for dataid in calexp_dataids:
#     exposures.append(dataid['exposure'])

# import matplotlib.pyplot as plt
# plt.hist(exposures, bins=100)
# plt.xlabel('Exposure')
# plt.ylabel('Number of calexps')
# plt.title('Histogram of calexps exposures')
# plt.show()

# ##But let's also get the histogram of raws
# raw_dataids = butler.registry.queryDataIds(['exposure'],
#                                            datasets=['raw'],
#                                            collections=['2.2i/defaults'],
#                                            where="instrument='LSSTCam-imSim' AND skymap='DC2'")

# raw_exposures = []
# for dataid in raw_dataids:
#     raw_exposures.append(dataid['exposure'])
##
# print the number of raws above 1M, and those between 1M, 3M
n_raws_in_butler_1M = butler.registry.queryDatasets('raw', collections=['2.2i/defaults'], where="instrument='LSSTCam-imSim' AND skymap='DC2' AND exposure > 1000000").count()
print('Number of raws through butler with exposure > 1M: ', n_raws_in_butler_1M)

n_raws_in_butler_1M_3M = butler.registry.queryDatasets('raw', collections=['2.2i/defaults'], where="instrument='LSSTCam-imSim' AND skymap='DC2' AND exposure > 1000000 AND exposure < 3000000").count()
print('Number of raws through butler with exposure > 1M and < 3M: ', n_raws_in_butler_1M_3M)


# and do the same for raws in 'u/nsedaghat/CorrespondingRaws' collection, but also number of all raws in that collection.
n_raws_in_corresponding_raws = butler.registry.queryDatasets('raw', collections=['u/nsedaghat/CorrespondingRaws'], where="instrument='LSSTCam-imSim' AND skymap='DC2'").count()
print('Number of CorrespondingRaws through butler: ', n_raws_in_corresponding_raws)

n_raws_in_butler_1M = butler.registry.queryDatasets('raw', collections=['u/nsedaghat/CorrespondingRaws'], where="instrument='LSSTCam-imSim' AND skymap='DC2' AND exposure > 1000000").count()
print('Number of CorrespondingRaws through butler with exposure > 1M: ', n_raws_in_butler_1M)

n_raws_in_butler_1M_3M = butler.registry.queryDatasets('raw', collections=['u/nsedaghat/CorrespondingRaws'], where="instrument='LSSTCam-imSim' AND skymap='DC2' AND exposure > 1000000 AND exposure < 3000000").count()
print('Number of CorrespondingRaws through butler with exposure > 1M and < 3M: ', n_raws_in_butler_1M_3M)

# number of corresponding raws, but this time with tract 3080
n_raws_in_corresponding_raws_3080 = butler.registry.queryDatasets('raw', collections=['u/nsedaghat/CorrespondingRaws'], where="instrument='LSSTCam-imSim' AND skymap='DC2' AND tract=3080").count()
print('Number of CorrespondingRaws through butler with tract 3080: ', n_raws_in_corresponding_raws_3080)

## How many rows are there in the list file then?
list_file = '/home/nima/lsst-dl/lists/u__nsedaghat__Dataset0.1.1-sciCalexps_fitsList.lst.gt1M'
with open(list_file) as f:
    lines = f.readlines()
    print('Number of lines in the list file: ', len(lines))
