#!/bin/sh

export MORE=-99999999 

expect -c "
spawn bash Anaconda3-4.2.0-Linux-x86_64.sh 

set timeout 500 

expect \">>>\"
send \"\n\"

expect \">>>\"
send \"yes\n\"

expect \">>>\"
send \"\n\"

expect \">>>\"
send \"yes\n\"

expect \"Sign up for free: https://anaconda.org\"
exit 0
"




#expect \"Please, press ENTER to continue\n>>>\"
#send \"\n\"


#expect -c "
#spawn bash Anaconda3-4.2.0-Linux-x86_64.sh
#
#set timeout 20
#
#expect \">>>\"
#send \"\n\"
#
#expect \"Do you approve the license terms? [yes|no]\n>>>\"
#send \"yes\n\"
#
#expect \"[/root/anaconda3] >>>\"
#send \"yes\n\"
#
#expect \"to PATH in your /root/.bashrc ? [yes|no]\n[no] >>>\"
#send \"yes\n\"
#"
