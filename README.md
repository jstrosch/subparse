# subparse
[![Generic badge](https://img.shields.io/badge/Python-3.8.1-blue.svg)](https://www.python.org/downloads/release/python-381/)
[![Generic badge](https://img.shields.io/badge/ubuntu-20.04-brightgreen)]()
[![Generic badge](https://img.shields.io/badge/bootstrap-5.0.2-orange)]()
[![Generic badge](https://img.shields.io/badge/CAPE-v2-orange)](https://github.com/kevoreilly/CAPEv2)
[![Generic badge](https://img.shields.io/badge/docker-vue-green)]()
[![Generic badge](https://img.shields.io/badge/docker-elastic-green)]()
[![Generic badge](https://img.shields.io/badge/docker-kafka-green)]()
[![Generic badge](https://img.shields.io/badge/version-1.0-GREEN.svg)]()

Subparse, is a modular framework developed by Josh Strochein, Aaron Baker, and Odin Bernstein. The framework is designed to parse and index malware files and present the information found during the parsing in a searchable web-viewer. The framework is modular, making use of a core parsing engine, parsing modules, and a variety of enrichers that add additional information to the malware indices. The main input values for the framework are directories of malware files, which the core parsing engine or a user-specified parsing engine parses before adding additional information from any user-specified enrichment engine all before indexing the information parsed into an elasticsearch index. The information gathered can then be searched and viewed via a web-viewer, which also allows for filtering on any value gathered from any file. There is currently 3 parsing engine, the default parsing engines (PEParser, OLEParser and ELFParser), and 2 enrichment engines 
(ABUSEEnricher and CAPEEnricher ).
<p>&nbsp;</p>

# Getting Started

## Software Requirements 
To get started using Subparse there are a few requrired/recommened programs that need to be installed and setup before trying to work with our software.

| Software | Status | Link |
| ----------- | ----------- | ----------- |
| Docker | Required | [Installation Guide](https://docs.docker.com/get-docker/) |
| Python3.8.1 | Required | [Installation Guide](https://www.python.org/downloads/release/python-381/) |
| Pyenv | Recommended | [Installation Guide](https://github.com/pyenv/pyenv) |


## Additional Requirements
After getting the required/recommended software installed to your system there are a few other steps that need to be taken to get Subparse installed. 

<details>
<summary>Python Requirements</summary>
</br>
Python requires some other packages to be installed that Subparse is dependent on for its processes. To get the Python set up completed navigate to the location of your Subparse installation and go to the *parser* folder. The following commands that you will need to use to install the Python requirements is:
<pre>
sudo get apt install build-essential
pip3 install -r ./requirements.txt
</pre>
</details>

<details>
<summary>Docker Requirements</summary>
<br>
Since Subparse uses Docker for its backend and web interface, the set up of the Docker containers needs to be completed before being able to use the program. To do this navigate to the root directory of the Subparse installation location, and use the following command to set up the docker instances: 
<pre>
docker-compose up
</pre>

Note: This might take a little time due to downloading the images and setting up the containers that will be needed by Subparse. 
</details>
<p>&nbsp;</p>

## Installation steps
* [Installation Steps](/INSTALL.md)

<br/>

# Usage
## Command Line Options
Command line options that are available for *subparse/parser/subparse.py*: 

| Argument | Alternative | Required | Description |
| ----------- | ----------- | ----------- | ----------- |
| -h | --help | No | Shows help menu |
| -d SAMPLES_DIR | --directory SAMPLES_DIR | Yes | Directory of samples to parse |
| -e ENRICHER_MODULES | --enrichers ENRICHER_MODULES | No | Enricher modules to use for additional parsing | 
| -r | --reset | No | Reset/delete all data in the configured Elasticsearch cluster |
| -v | --verbose | No | Display verbose commandline output |
| -s | --service-mode | No | Enters service mode allowing for mode samples to be added to the SAMPLES_DIR while processing |

## Viewing Results
To view the results from Subparse's parsers, navigate to [localhost:8080](localhost:8080).
If you are having trouble viewing the site, make sure that you have the container started up in Docker and that there is not another process running on port 8080 that could cause the site to not be available.
<p>&nbsp;</p>

# General Information Collected
Before any parser is executed general information is collected about the sample regardless of the underlying file type. This information includes: 
* MD5 hash of the sample
* SHA256 hash of the sample
* Sample name
* Sample size
* Extension of sample
* Derived extension of sample

# Parser Modules
Parsers are ONLY executed on samples that match the file type. For example, PE files will by default have the PEParser executed against them due to the file type corresponding with those the PEParser is able to examine.

## Default Modules
<details>
<summary>ELFParser</summary>
</br>
This is the default parsing module that will be executed against ELF files. Information that is collected:

* General Information
* Program Headers
* Section Headers
* Notes
* Architecture Specific Data
* Version Information 
* Arm Unwind Information
* Relocation Data
* Dynamic Tags
</details>

<details>
<summary>OLEParser</summary>
</br>
This is the default parsing module that will be executed against OLE and RTF formatted files, this uses the OLETools package to obtain data. The information that is collected:

* Meta Data
* MRaptor
* RTF
* Times
* Indicators
* VBA / VBA Macros
* OLE Objects
</details>

<details>
<summary>PEParser</summary>
</br>
This is the default parsing module that will be executed against PE files that match or include the file types: PE32 and MS-Dos. Information that is collected:

* Section code and count
* Entry point
* Image base
* Signature
* Imports
* Exports

</details>
<p>&nbsp;</p>

# Enricher Modules
These modules are optional modules that will ONLY get executed if specified via the -e | --enrichers flag on the command line. 

## Default Modules
<details>
<summary>ABUSEEnricher</summary>
</br>
This enrichers uses the [Abuse.ch](https://abuse.ch/) API and [Malware Bazaar](https://bazaar.abuse.ch) to collect more information about the sample(s) subparse is analyzing, the information is then aggregated and stored in the Elastic database.
</details>

<details>
<summary>CAPEEnricher</summary>
</br>
This enrichers is used to communicate with a CAPEv2 Sandbox instance, to collect more information about the sample(s) through dynamic analysis, the information is then aggregated and stored in the Elastic database utilizing the Kafka Messaging Service for background processing.
</details>

<details>
<summary>STRINGEnricher</summary>
</br>
This enricher is a smart string enricher, that will parse the sample for potentially interesting strings. The categories of strings that this enricher looks for include: Audio, Images, Executable Files, Code Calls, Compressed Files, Work (Office Docs.), IP Addresses, IP Address + Port, Website URLs, Command Line Arguments.
</details>

<details>
<summary>YARAEnricher</summary>
</br>
This ericher uses a pre-compiled yara file located at: parser/src/enrichers/yara_rules. This pre-compiled file includes rules from <a href="https://github.com/virustotal/yara">VirusTotal</a> and  <a href="https://yara-rules.github.io/blog/">YaraRulesProject</a>
</details>
<p>&nbsp;</p>


# Developing Custom Parsers & Enrichers
Subparse's web view was built using *Bootstrap* for its CSS, this allows for any built in Bootstrap CSS to be used when developing your own custom Parser/Enricher Vue.js files. We have also provided an example for each to help get started and have also implemented a few custom widgets to ease the process of development and to promote standardization in the way information is being displayed. All Vue.js files are used for dynamically displaying information from the custom Parser/Enricher and are used as templates for the data. 

Note: Naming conventions with both class and file names must be strictly adheared to, this is the first thing that should be checked if you run into issues now getting your custom Parser/Enricher to be executed. The naming convention of your Parser/Enricher must use the same name across all of the files and class names.

* [Python Development](/parser/README.md)
* [Vue Development](/viewer/README.md)
* [Vue Helpers](/viewer/HELPER_README.md)

</br>
</br>

## Logging
The logger object is a singleton implementation of the default Python logger. For indepth usage please reference the [Offical Doc](https://docs.python.org/3.8/library/logging.html). 
For Subparse the only logging methods that we recommend using are the logging levels for output. These are: 
* debug
* warning
* error
* critical
* exception
* log
* info

<br/>
<br/>

## ACKNOWLEDGEMENTS

* This research and all the co-authors have been supported by NSA Grant H98230-20-1-0326.