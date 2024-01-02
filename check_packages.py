
import os
import json

has_error = False

# Iterate all packages inside "pkgs" folder
for pkg in os.listdir("pkgs"):
    # Get package name
    pkg_name = pkg.split(".")[0]
    # Open package file
    with open("pkgs/" + pkg, "r") as pkg_file:
        # Load package data
        pkg_data = json.load(pkg_file)
        
        download_url = pkg_data["download_url"]

        print("CHECKING " + pkg_name + "...", end=' ')

        # clone the package into ".temp" folder
        os.system("git clone " + download_url + " .temp --quiet --depth 1")

        # See if the package has a "sn.toml" file
        if os.path.isfile(".temp/sn.toml"):
            # If it does, then it's a valid package
            print("OK")
        else:
            # If it doesn't, then it's an invalid package
            print("INVALID")
            has_error = True
        
        # Delete the ".temp" folder
        os.system("rm -rf .temp")

if has_error:
    exit(1)
