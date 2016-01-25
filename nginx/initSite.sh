#!/bin/bash

conf_path="/home/huajie/Develop/nginx/conf.d"
html_path="/home/huajie/Develop/nginx/html"
host_file="/home/huajie/Develop/nginx/hosts"
tpl_file=$conf_path"/default.conf.tpl"

default_site_string="{site}"
default_site_path_string="{site_path}"
default_site="default_site"

if [  -n "$1" ] ;then
    default_site=$1
fi

if [  -n "$2" ] ;then
    html_path=$2
fi

site_path=$html_path'/'$default_site
site='www.'$default_site'.com'

if [ ! -d $site_path ]; then 
    mkdir $site_path
else
    echo "The folder exist,please check again"
    exit
fi
checkSed(){
    if hash sed 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

doBySed(){
    sed -e "s!$default_site_string!$site!ig;s!$default_site_path_string!$site_path!ig;" $tpl_file > $conf_path"/"$default_site".conf"
    sed -i "s!127.0.0.1\slocalhost!&\n127.0.0.1\t$site!" $host_file
}

doByNative(){
    echo "native";
}

run(){
    checkSed
    ck=$?
    if [ $ck == 0 ]
    then
       doBySed
    else
        doByNative
    fi
}
run
echo "The Site $default_site initialized successfully"