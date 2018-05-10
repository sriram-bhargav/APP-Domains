# Instructions

1. Install python and other dependencies
2. To search if a particular .app domain is available:
   `./domain_search.py -app {APP_DOMAIN_NAME}`
   For example, if you want to know `best.app` is available, you should run `./domain_search.py -app best`
3. To explore all currently available .app domains which are valid *English words*:
   try `./domain_search.py -min 4 -max 8` to find all available domain names with atleast 4 and atmost 8 characters.
4. You can also check available.app file for available English .app domains (upto 8 chars).
5. (TODO) Use Godaddy API (https://api.godaddy.com/v1/appraisal/{APP_NAME}.app) to extract estimated domain value.
