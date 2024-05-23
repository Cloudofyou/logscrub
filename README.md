# logscrub.py
# deltatime.py

Use:
./deltatime.py <logfile>

This will show the highest time delta in the logfile indicitive of when the reboot/event happened.
You can use this information to run logscrub to see differences of notifications before and/or after the event.

Use:
./logscrub.py <logfile.txt> [<starting_line>]

For example, if you have a logfile named mylogs.csv and deltatime returns a value of 154:

$ ./deltatime.py mylogs.csv
Processed 7401 total lines and found 7399 times where it crossed 0 threshold.
High water mark: 745 seconds at line number 154 in log.
$ ./logscrub.py mylogs.csv 154
Device name        Error            Count
-----------------  ---------------  -----
GPU_SXM_2          XID-43           19
GPU_SXM_3          XID-43           19
GPU_SXM_4          XID-43           19
