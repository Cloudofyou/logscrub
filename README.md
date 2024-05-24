# deltatime.py

Use:
./deltatime.py &lt;logfile&gt;

This will show the highest time delta between timestamp entries in the logfile indicitive of when the reboot/event happened.
You can use this information to run logscrub to see differences of notifications before and/or after the event.

# logscrub.py

Use:
./logscrub.py <logfile.txt> [<starting_line>]

This will show each time GPU_SXM_<i>x</i> or NVSwitch_<i>x</i> is shown along with its associated XID or SXID and the number of times it was observed in the file.

# Example

For example, if you have a logfile named mylogs.csv and deltatime returns a value of 154:

$ ./deltatime.py mylogs.csv
Processed 7401 total lines and found 7399 times where it crossed 0 threshold.<br>
High water mark: 745 seconds at line number 154 in log.

$ ./logscrub.py mylogs.csv 154<br>
<table>
    <thead>
        <tr>
            <th>Device name</th>
            <th>Error</th>
            <th>Count</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>GPU_SXM_2</td>
            <td>XID-43</td>
            <td>19</td>
        </tr>
        <tr>
            <td>GPU_SXM_3</td>
            <td>XID-43</td>
            <td>19</td>
        </tr>
        <tr>
            <td>GPU_SXM_7</td>
            <td>XID-37</td>
            <td>1009</td>
        </tr>
    </tbody>
</table>
