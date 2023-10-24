# Combine multiple .ini files to run through geomxngspipeline
# all together

import sys
import glob
import configparser

inis_to_combine = glob.glob("*.ini")

# create main .ini using 1st ini file as
# template
main_ini = configparser.ConfigParser()
main_ini.optionxform = str 
main_ini.read(inis_to_combine[0])

# iterate over remaining .ini files
# and add their information. Ensure [Targets]
# are the same i.e. transcript probes

target_targets = main_ini["Targets"].items()
for ini in inis_to_combine[1:]:
    config = configparser.ConfigParser()
    config.optionxform = str 
    config.read(ini)
    targets = config["Targets"].items()

    if not bool(set(targets).intersection(set(target_targets))):
        raise ValueError("targets in files do not match")

    # only need to update the AOI_List
    main_ini["AOI_List"] = {**main_ini["AOI_List"], **config["AOI_List"]}

with open("combined_config.ini", "w") as configfile:
    main_ini.write(configfile)
                
