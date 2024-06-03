echo 'This is the  script runs logscrub.py '
echo ' --------------------------'

filename='logs/log_file_210198470012.csv'
echo '1'
echo $filename
python3 deltatime.py $filename -q
exit_code=$?
python3 logscrub.py $filename 1 $exit_code
python3 logscrub.py $filename $exit_code

