# upwork_002
Hi, you can do this tutorial:

Clone this repository
Create venv in new folder
Run main.py
Get output from output folder
These are the commands:
mkdir web_scraping

git clone https://github.com/NguyenAnMinhThien/upwork_002.git web_scraping

cd web_scraping

python -m venv venv

Depend on your OS

source venv/Scripts/activate

OR

source venv/bin/activate

pip install -r requirement.txt

python main.py -min 0 -max 1 -output myfile.csv -records 65 -url 'https://app.apollo.io/#/people?contactLabelIds[]=672e5c63c3285602cf472fef&prospectedByCurrentTeam[]=yes&sortByField=%5Bnone%5D&sortAscending=false&page=1' -con n -rows 25

and when you turn off your pc, rerun again by new command: (all the same, just change "-con n" to "-con y"

python main.py -min 0 -max 1 -output myfile.csv -records 65 -url 'https://app.apollo.io/#/people?contactLabelIds[]=672e5c63c3285602cf472fef&prospectedByCurrentTeam[]=yes&sortByField=%5Bnone%5D&sortAscending=false&page=1' -con y -rows 25


(remember the quote in url)

If you forget the way you want to run your code, then run this command:
python main.py -h
