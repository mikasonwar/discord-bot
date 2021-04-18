python -m pip install -r requirements.txt

crontab -e

0,15,30,45 * * * * cd /dir/to/project ; python mangadex_job.py

0 0 * * 3 cd /dir/to/project ; python woo_job.py
0 0 * * * cd /dir/to/project ; python birthday_job.py
