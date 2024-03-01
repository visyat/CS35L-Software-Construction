#!/bin/sh

echo "Log-in Shell:"
ps -o "pid,args" | head -n 2
MY_PID=`ps -o "pid" --no-headers | head -n 1`
MY_PPID=`ps -o "ppid" --no-headers | head -n 1`

echo -e "\nAncestor Processes: "
#ps -o "pid,args" --no-headers -p $MY_PPID
while [ $MY_PPID -ne 0 ]
do
    ps -o "pid,args" --no-headers -p $MY_PPID
    MY_PPID=`ps -o "ppid" --no-headers -p $MY_PPID`
done

echo -e "\nDescendant Processes: "
get_descendants()
{
    if [ ! -z "$1" ]; then
	ps -o "pid,args" --no-headers --ppid $1

	for f in `ps -o "pid" --no-headers --ppid $1`
	do
	    get_descendants $f
	done
    fi
}
get_descendants $MY_PID

#while [ ! -z "$MY_PID"  ]
#do
#    ps -o "pid,args" --no-headers --ppid $MY_PID
#    MY_PID=`ps -o "pid" --no-headers --ppid $MY_PID | head -n 1`
#done
