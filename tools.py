# An auxiliary function for pruning exported yaml files
def remove_collections_from_yaml_objective(yaml_file, inplace=False, only_remove_chained=False):
    # Load the yaml file as a python object
    import yaml
    with open(yaml_file, 'r') as f:
        y = yaml.safe_load(f)

    # Browse y['data'] and drop the items that are of type: collection
    indices_to_drop = []
    for i, item in enumerate(y['data']):
        if item['type'] == 'collection':
            if only_remove_chained:
                if item['collection_type'] == 'CHAINED':
                    indices_to_drop.append(i)
            else:
                indices_to_drop.append(i)

    y['data'] = [item for i, item in enumerate(y['data']) if i not in indices_to_drop]

    # Write the yaml object back to a file
    if inplace:
        dest_file = yaml_file
    else:
        dest_file = yaml_file+".mod"

    with open(dest_file, 'w') as f:
        yaml.dump(y, f, sort_keys=False)

    return y
