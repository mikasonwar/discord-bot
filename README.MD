python -m pip install -r requirements.txt

crontab -e

15 * * * * cd /dir/to/project ; python mangadex_job.py
0 0 * * 3 cd /dir/to/project ; python woo_job.py
