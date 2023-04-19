This is repository all necessary files used with my Research Project

TITLE: "Using passive mthods for detection of pfishing internet domains"

Author: Krzysztof Legenza


Folders:
data - test database used in Project
dict - dictionaries used in aplication:
    d-----        dozwolone
        -a----        allowed.txt
    d-----        kluczowe
        -a----        apple.txt
        -a----        blik.txt
        -a----        facebook.txt
        -a----        netflix.txt
        -a----        office.txt
        -a----        paypal.txt
        -a----        spotify.txt
    d-----        pomocnicze
        -a----        auxiliary.txt
    d-----        sld_tld
        -a----        sld_plus_tld.txt
    d-----        tlds
        -a----        tlds.txt
    d-----        wystawcy
        -a----        cert_issuers.txt

source - source database collected by certstream application on linux OS (using certstream_collector.sh from PYTHON_CODE main forder)

Research_project - all python scripts used during realize the research project:
        -a----        cert_issuers_collect.py       - collecting all certificate issuers from test dataset
        -a----        count_auxiliary.py            - count auxiliarity words occurances in test dataset
        -a----        count_free_tlds.py            - count free tlds occurances in test dataset
        -a----        count_keyword.py              - count keywords occurances in test dataset
        -a----        data_collector.py             - the first version of CertStream collector (unuseful for bigger dataset, because of problems with Error code from CertStream server stream stability)
        -a----        find_auxiliary.py             - find records with auxiliarity words occurances and write then into JSON file
        -a----        find_auxiliary_weight.py      - find records with auxiliarity words occurances and write then into JSON file with calculated weight
        -a----        find_dash.py                  - find records with dash occurances and write then into JSON file
        -a----        find_dash_weight.py           - find records with dash occurances and write then into JSON file with calculated weight
        -a----        find_dots.py                  - find records with dots occurances and write then into JSON file
        -a----        find_dots_weight.py           - find records with dots occurances and write then into JSON file with calculated weight
        -a----        find_free_issuers.py          - find records with free issuers certificates and write then into JSON file
        -a----        find_free_tlds.py             - find records with free TLD and SLD+TLD occurances and write then into JSON file
        -a----        find_free_tlds_weight.py      - find records with free TLD and SLD+TLD occurances and write then into JSON file with calculated weight
        -a----        find_idn.py                   - find records in IDN format and write then into JSON file
        -a----        find_idn_weight.py            - find records in IDN format and write then into JSON file with calculated weight
        -a----        find_keywords.py              - find records with keywords occurances and write then into JSON file
        -a----        find_keywords_weight.py       - find records with keywords occurances and write then into JSON file with calculated weight
        -a----        find_longdomains.py           - find records with long domain names and write then into JSON file
        -a----        find_longdomains_weight.py    - find records with long domain names and write then into JSON file with calculated weight
        -a----        find_total.py                 - find records matching all methods together and write then into JSON file
        -a----        find_total_avoid_duplcated.py - find records matching all methods together and write all unique records into JSON file
        -a----        new_collector.py              - second version of CertStream collector
        -a----        new_collector_local.py        - second version of CerStream collector (require local CerStream server installed)
        -a----        writer.py                     - the first reader single record from CerStream server


The final script used in project was:    find_total_avoid_duplcated.py    

Files:
-a----        result_high.json      - list of detected phishing domains with high probability
-a----        result_low.json       - list of detected phishing domains with low probability
-a----        result_medium.json    - list of detected phishing domains with medium probability

-a----        certstream_collector.sh - linux shell script used for CertStream source data collection

