## Initial setup
import os, sys
from lsst.daf.butler import Butler, CollectionType
import getpass
import psycopg2
import time

from .tools import remove_collections_from_yaml_objective

REPO = "/repo/dc2"
DBNAME = "lsst"

# Set PGHOST, PGUSER and PGPASSWORD environment variables
os.environ["PGHOST"] = "/var/run/postgresql"
os.environ["PGUSER"] = "postgres"
os.environ["PGPASSWORD"] = getpass.getpass("Password for postgres: ")

## Create the database on the postgresql server -- drop it if it already exists.
conn = psycopg2.connect(database="postgres")
conn.set_isolation_level(0)
cur = conn.cursor()


print("Dropping database %s, if it exists..." % DBNAME)
cur.execute("DROP DATABASE IF EXISTS %s" % DBNAME)

print("Creating database %s..." % DBNAME)
while True:
    try:
        cur.execute("CREATE DATABASE %s" % DBNAME)
        break
    except:
        print("Database %s already exists.  Trying again..." % DBNAME)
        time.sleep(1)

conn.set_isolation_level(1)
cur.close()
conn.close()
print("Database %s created." % DBNAME)

# Connect to the database and set the btree_gist extension.
print("Setting btree_gist extension...")
conn = psycopg2.connect(database=DBNAME, user="postgres", password="poshtgres")
conn.set_isolation_level(0)
cur = conn.cursor()
cur.execute("CREATE EXTENSION btree_gist")
conn.set_isolation_level(1)
cur.close()
conn.close()

## Create the butler repository
print("Creating butler repository...")
# delete the repo dir if it already exists
if os.path.exists(REPO):
    os.system("rm -rf %s" % REPO)

# Create a temporary seed-config.yaml file (in /tmp) with the below content,
# but replace the database name accordingly:
#
# content:
# datastore:
#  root: <butlerRoot>
#
# registry:
#  db: postgresql+psycopg2://localhost:5432/lsst
seed_file = "/tmp/seed-config.yaml"
with open(seed_file, 'w') as f:
    f.write("content:\n")
    f.write(" datastore:\n")
    f.write("  root: %s\n" % REPO)
    f.write("\n")
    f.write("registry:\n")
    f.write(" db: postgresql+psycopg2://localhost:5432/%s\n" % DBNAME)

# Now create the repository with the temp seed file.
os.system(f'butler create --seed-config /tmp/seed-config.yaml {REPO}')

## Create a Butler object
writeable_butler = Butler(REPO, writeable=True)

## Replace file paths before importing
print("Replacing file paths before importing...")
os.system(f'find /repo/dc2_ncsa_backup/ -iname "*.yaml" -exec sed -i s#/projects/HSC#/repo/dc2_ncsa_backup# {{}} \;')
os.system(f'find /repo/raw/ -iname "*.yaml" -exec sed -i s#/projects/HSC#/repo/raw# {{}} \;')
os.system(f'find /repo/usdf_export_calib/ -iname "*.yaml" -exec sed -i s#/projects/HSC/repo/dc2/#/repo/dc2_ncsa_backup/# {{}} \;')

## Register the instrument
print("Registering the instrument...")
os.system(f'butler register-instrument {REPO} lsst.obs.lsst.LsstCamImSim')

## Register the skymap
print("Registering the skymap...")
os.system(f'butler register-skymap {REPO} -C $OBS_LSST_DIR/config/makeSkyMap.py -c name="DC2"')

## Import curated calibrations
print("Importing curated calibrations...")
INDIR = "/repo/usdf_export_calib/bfk"
YAMLS = [x for x in os.listdir(INDIR) if x.endswith(".yaml")]

for YAML in YAMLS:

    remove_collections_from_yaml_objective(os.path.join(INDIR, YAML),
                                           inplace=False,
                                           only_remove_chained=True)

    writeable_butler.import_(
        directory = None,
        filename = INDIR+"/"+YAML+".mod",
        format = "yaml",
        transfer = 'symlink',
    )
    print("Imported", YAML)

INDIR = "/repo/usdf_export_calib/camera"
YAMLS = [x for x in os.listdir(INDIR) if x.endswith(".yaml")]

for YAML in YAMLS:

    remove_collections_from_yaml_objective(os.path.join(INDIR, YAML),
                                           inplace=False,
                                           only_remove_chained=True)

    writeable_butler.import_(
        directory = None,
        filename = INDIR+"/"+YAML+".mod",
        format = "yaml",
        transfer = 'symlink',
    )
    print("Imported", YAML)


## Import refcats
print("Importing refcats...")

# Create the refcats/PREOPS-301 RUN collection, and its CHAINed parent.
writeable_butler.registry.registerCollection("refcats/PREOPS-301", type=CollectionType.RUN)
writeable_butler.registry.registerCollection("refcats", type=CollectionType.CHAINED)
writeable_butler.registry.setCollectionChain("refcats", ["refcats/PREOPS-301"])

YAML = "/repo/usdf_export_full_latest/cal_ref_cat_2_2/_export_000.yaml.mod"
writeable_butler.import_(
    directory = None,
    filename = YAML,
    format = "yaml",
    transfer = 'symlink',
)
print("Imported", YAML)

## Ingest raws (only those from dp02)
print("Ingesting select raws from dp02...")

YAML = "/repo/dp02_raws/export_raw.yaml"

# Replace file paths -- be careful not to replace collection names.
with open(YAML, 'r') as f:
    lines = f.readlines()
with open(YAML, 'w') as f:
    for line in lines:
        # replace only occurences of "2.2i/raw/all/raw" that do not follow a slash ("/") character.
        # Want to replace '2.2i/raw/all/raw' with '/repo/dp02_raws/2.2i/raw/all/raw'
        import re
        line = re.sub(r'(?<!\/)2.2i/raw/all/raw', '/repo/dp02_raws/2.2i/raw/all/raw', line)
        f.write(line)

# Ingest the raws
writeable_butler.import_(
    directory = None,
    filename = YAML,
    format = "yaml",
    transfer = 'symlink',
)
print("Imported", YAML)

## Also import the big pile of raws, so the define-visits covers the entire raws, even if they are missing.
print("Ingesting the big pile of raws...")
INDIR = "/repo/raw"
YAMLS = [x for x in os.listdir(INDIR) if ".yaml" in x]

for YAML in YAMLS:
    writeable_butler.import_(
        directory = None,
        filename = INDIR+"/"+YAML,
        format = "yaml",
        transfer = 'symlink',
    )
    print("Imported", YAML)

## define visits
print("Defining visits...")
os.system(f'butler define-visits --collections 2.2i/raw/all {REPO} lsst.obs.lsst.LsstCamImSim')

## Import flats, darks, biases.
print("Importing flats, darks, biases...")
DIRS = ["/repo/usdf_export/flat",
        "/repo/usdf_export/dark",
        "/repo/usdf_export/bias"]

# create needed collections.
from lsst.daf.butler import CollectionType
writeable_butler.registry.registerCollection("2.2i/calib/gen2/20220101T000000Z", type=CollectionType.RUN)
writeable_butler.registry.registerCollection("2.2i/calib/gen2/20220806T000000Z", type=CollectionType.RUN)
writeable_butler.registry.registerCollection("2.2i/calib/gen2/20231201T000000Z", type=CollectionType.RUN)
writeable_butler.registry.registerCollection("2.2i/calib/gen2/20220101T000000Z", type=CollectionType.RUN)


for INDIR in DIRS:
    YAMLS = [x for x in os.listdir(INDIR) if x.endswith(".yaml")]

    for YAML in YAMLS:

        remove_collections_from_yaml_objective(os.path.join(INDIR, YAML),
                                               inplace=False,
                                               only_remove_chained=False)

        writeable_butler.import_(
            directory = None,
            filename = INDIR+"/"+YAML+".mod",
            format = "yaml",
            transfer = 'symlink',
        )
        print("Imported", YAML)



# ## Restore CHAINED collections
# MainDir = "/repo/usdf_export_collectionsOnly"

# include_list = [
#     "raw",
#     "calexp",
#     "goodSeeingDiff_templateExp",
#     "goodSeeingDiff_differenceExp",
#     "goodSeeingDiff_diaSrcTable",
# ]

# for INDIR in include_list:
#     YAMLS = [x for x in os.listdir(MainDir+"/"+INDIR) if ".yaml" in x]
#     for YAML in YAMLS:
#         filename = MainDir+"/"+INDIR+"/"+YAML
#         writeable_butler.import_(
#             directory = None,
#             filename = filename,
#             format = "yaml",
#             transfer = 'auto',
#         )
#         print("Imported", INDIR+"/"+YAML)

## Create the "defaults" chain, as printed below:
#2.2i/defaults                                                                                   CHAINED
#  2.2i/raw/all                                                                                  RUN
#  2.2i/calib                                                                                    CHAINED
#    2.2i/calib/DM-30694                                                                         CALIBRATION
#    2.2i/calib/gen2                                                                             CALIBRATION
#    2.2i/calib/DM-30694/unbounded                                                               RUN
#  skymaps                                                                                       RUN
#  refcats                                                                                       CHAINED
#    refcats/PREOPS-301                                                                          RUN
#  2.2i/truth_summary
print("Creating the 'defaults' chain...")
writeable_butler.registry.registerCollection("2.2i/calib", type=CollectionType.CHAINED)
writeable_butler.registry.setCollectionChain("2.2i/calib", ["2.2i/calib/DM-30694", "2.2i/calib/gen2", "2.2i/calib/DM-30694/unbounded"])

writeable_butler.registry.registerCollection("2.2i/defaults", type=CollectionType.CHAINED)
writeable_butler.registry.setCollectionChain("2.2i/defaults", ["2.2i/raw/all", "2.2i/calib", "skymaps", "refcats", "2.2i/truth_summary"])


## Import my backed-up templates, sciences, diffs and detections.
MainDir = "/repo/usdf_export"

include_list = [
                "calexp",
                "goodSeeingDiff_templateExp",
                "goodSeeingDiff_differenceExp",
                "goodSeeingDiff_diaSrcTable",
                ]

for INDIR in include_list:
    YAMLS = [x for x in os.listdir(MainDir+"/"+INDIR) if ".yaml" in x]
    for YAML in YAMLS:
        filename = MainDir+"/"+INDIR+"/"+YAML
        writeable_butler.import_(
            directory = None,
            filename = filename,
            format = "yaml",
            transfer = 'symlink',
        )

## Prune datasets not backed by a file on disk
refs = writeable_butler.registry.queryDatasets(
    collections=["*"],
    datasetType="*")

rr = list(refs)
print(f"Number of datasets before pruning: {len(rr)}")

mapping = writeable_butler.stored_many(refs)

# count the number of datasets to remove
to_remove = [datasetRef for datasetRef, status in mapping.items() if not status]
print(f"Removing {len(to_remove)} datasets out of {len(mapping)}")

# Print the number of each dataset type that's being removed.
dataset_types = set([datasetRef.datasetType for datasetRef in to_remove])
for dataset_type in dataset_types:
    print(f"Removing {len([datasetRef for datasetRef in to_remove if datasetRef.datasetType == dataset_type])} {dataset_type}")

#Let's remove all of them
writeable_butler.registry.removeDatasets(to_remove)

# and print the number of datasets after pruning, by dataset type
new_refs = writeable_butler.registry.queryDatasets(
    collections=["*"],
    datasetType="*")
new_rr = list(refs)
print(f"Number of datasets after pruning: {len(new_rr)}")
for dataset_type in dataset_types:
    print(f"After pruning: {len([datasetRef for datasetRef in new_refs if datasetRef.datasetType == dataset_type])} {dataset_type}")
