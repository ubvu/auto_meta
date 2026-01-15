"""
Code that is run at the initiation of a project as part of the SetupProj.bat
script. This gathers all the relevant software and hardware info and saves
it to a JSON. The JSON can be reffered to when reproducing results as some
hardware and software can have differing results, such as how the RNG works.
"""

import json
import platform

import GPUtil
import psutil


# Function to convert from bytes to a user friendly value
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


# Dict to store data and save as JSON
device_data = {}
# Basic vals


uname = platform.uname()
device_data["System"] = uname.system
device_data["Node Name"] = uname.node
device_data["Release"] = uname.release
device_data["Version"] = uname.version
device_data["Machine"] = uname.machine
device_data["Processor"] = uname.processor

# number of cores
device_data["Physical_cores"] = psutil.cpu_count(logical=False)
device_data["Total_cores"] = psutil.cpu_count(logical=True)
# CPU frequencies
cpufreq = psutil.cpu_freq()
device_data["Max_Frequency"] = f"{cpufreq.max:.2f}Mhz"
device_data["Min_Frequency"] = f"{cpufreq.min:.2f}Mhz"

# Get the memory details
svmem = psutil.virtual_memory()
device_data["Total"] = get_size(svmem.total)
device_data["Available"] = get_size(svmem.available)

# Get GPU data
gpus = GPUtil.getGPUs()

if not gpus:
    print("No GPU detected.")
    device_data["GPU"] = "NA"
else:
    for i, gpu in enumerate(gpus):  # noqa B007
        device_data["GPU_{i + 1}_ID"] = gpu.id
        device_data["GPU_{i + 1}_Name"] = gpu.name
        device_data["GPU_{i + 1}_Driver"] = gpu.driver
        device_data["GPU_{i + 1}_Memory_Total"] = f"{gpu.memoryTotal} MB"
    device_data["Number_GPUs"] = str(i)

# Serializing json
json_object = json.dumps(device_data, indent=4)
# Writing to sample.json
with open("Development_spec.json", "w") as outfile:
    outfile.write(json_object)
