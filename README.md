# Metasploit auto enumeration script (msfenum)

Msfenum simplifies running multiple auxiliary modules on a specific set of targets. Running a low hanging fruit scan within a penetration test can be very useful, for example to find open shares or vulnerable services quickly. 

The Metasploit framework offers lots of useful auxiliary modules to perform low hanging fruit scans. This script simply runs all the auxiliary modules specified in the config files against the specified targets. All settings can be modified per auxiliary module and new modules can be added easily.

Feel free to share your useful auxiliary configuration for low hanging fruit scans or any code improvements :).

## Usage

``python msfenum.py [-h] [-t [THREADS]] TARGET_FILE``


## Structure:
* logs/
  * Contains all results after running the script
* modules/
  * Contains all configuration per auxiliary module
* config
  * Contains global configuration settings
* msfenum.log
  * Some logging generated when running msfenum.py
* msfenum.py
  * The main script
