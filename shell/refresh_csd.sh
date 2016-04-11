#!/bin/bash
# Refresh cocostudio csd

CSD_FILE=$1

if [[ ! -f ${CSD_FILE} ]]; then
    echo "${CSD_FILE} is not existed!"
    exit 1
fi

# cp ${CSD_FILE}{,-bak}
# echo "Backup original ${CSD_FILE} to ${CSD_FILE}-bak"

RES_PATH=`dirname ${CSD_FILE}`
for PNG in `cat ${CSD_FILE} | grep Plist | grep -o 'Path="[^"]*' | sed 's/Path=\"//' | grep png | sort | uniq`; do
#    echo ${PNG}
    PNG_NAME=`echo ${PNG} | awk -F"/" '{print $NF}'`
    OLD_NAMESPACE=`echo ${PNG} | awk -F"/" '{print $(NF-1)}'`
#    echo ${PNG_NAME}
    PNG_REAL_PATHS=`find ${RES_PATH} -name ${PNG_NAME}`
    IS_NAMESPACE_CHANGED=false
    for PNG_REAL_PATH in ${PNG_REAL_PATHS[@]}; do
        REAL_NAMESPACE=`echo ${PNG_REAL_PATH} | awk -F "/" '{print $(NF-1)}'`
        if [[ "${OLD_NAMESPACE}" = "${REAL_NAMESPACE}" ]]; then
            IS_NAMESPACE_CHANGED=true
            break
        fi
    done
    if [[ ${IS_NAMESPACE_CHANGED} = false ]]; then
#        echo "old namespace: ${OLD_NAMESPACE}"
#        echo "real namespace: ${REAL_NAMESPACE}"
#        cat ${CSD_FILE} | grep ${PNG_NAME} | grep Path | grep Plist | sed 's/${OLD_NAMESPACE}/${REAL_NAMESPACE}/g'
        REPLACE_LINES=`cat ${CSD_FILE} | grep -n ${PNG_NAME} | grep Path | grep Plist | awk -F":" '{print $1}'`
        declare -a lines=( $REPLACE_LINES )
#        echo ${lines}
        for line in "${lines[@]}"; do
#            echo "Replace ${line}"
            sed -i.bak "${line}s/${OLD_NAMESPACE}/${REAL_NAMESPACE}/g" ${CSD_FILE}
        done
        rm ${CSD_FILE}.bak
    fi
done
