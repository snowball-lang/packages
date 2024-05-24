
import os
import json

has_error = False

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Iterate all packages inside "pkgs" folder
for pkg in os.listdir("pkgs"):
    print("\n=========================================\n")
    # Get package name
    pkg_name = pkg.split(".")[0]
    # Open package file
    with open("pkgs/" + pkg, "r") as pkg_file:
        # Load package data
        pkg_data = json.load(pkg_file)

        print("CHECKING " + pkg_name + "...")
        if "versions" not in pkg_data:
            print(RED + "INVALID (no verion tree)" + RESET)
            has_error = True
            continue

        versions = pkg_data["versions"]
        for version in versions:
            download_url = pkg_data["download_url"]
            print(" VERSION " + GREEN + version + RESET + ":")
            try:
                print("    DOWNLOAD: ...", end=' ')
                # clone the package into ".temp" folder
                exit = os.system("git clone " + download_url + " .temp --quiet --depth 1 --branch " + version)
                if exit != 0:
                    print(RED + "ERROR" + RESET)
                    has_error = True
                    continue
                print(GREEN + "OK" + RESET)

                # See if the package has a "sn.toml" file
                print("    PACKAGE DEPS: ...", end=' ')
                if os.path.isfile(".temp/sn.reky"):
                    # If it does, then it's a valid package
                    print(GREEN + "OK" + RESET)
                    content = open(".temp/sn.reky", "r").read()
                    for dep in content.splitlines():
                        line = dep.strip()
                        if line.startswith("#"):
                            continue
                        if line == "":
                            continue
                        split = line.split("==")
                        if len(split) != 2:
                            print(RED + "INVALID" + RESET)
                            has_error = True
                            break
                        dep_name = split[0].strip()
                        dep_version = split[1].strip()
                        print("        " + dep_name + " " + dep_version + ": ...", end=' ')
                        try:
                            # Check if the dependency exists
                            with open("pkgs/" + dep_name + ".json", "r") as dep_file:
                                dep_data = json.load(dep_file)
                                if dep_version in dep_data["versions"]:
                                    print(GREEN + "OK" + RESET)
                                else:
                                    print(RED + "INVALID" + RESET)
                                    has_error = True
                        except Exception as e:
                            print(RED + "ERROR" + RESET)
                            print(e)
                            has_error = True

                else:
                    # If it doesn't, then it's an invalid package
                    print(GREEN + "OK" + RESET)
                
            except Exception as e:
                print(RED + "ERROR" + RESET)
                print(e)
                has_error = True

            # Delete the ".temp" folder
            os.system("rm -rf .temp")

if has_error:
    exit(1)
