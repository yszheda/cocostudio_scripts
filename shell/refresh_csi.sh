#!/bin/bash
# Refresh cocostudio SpriteFrameSheet *.csi

CSI_FILE=$1

if [[ ! -f ${CSI_FILE} ]]; then
    echo "${CSI_FILE} is not existed!"
    exit 1
fi

# echo ${CSI_FILE}
ATLAS_NAME=`echo ${CSI_FILE} | awk -F"/" '{print $NF}' | sed 's/.csi//'`
# echo "${ATLAS_NAME}"
RES_PATH="$(dirname ${CSI_FILE})/../"
# echo "${RES_PATH}"
ATLAS_RES_PATH="${RES_PATH}/${ATLAS_NAME}"
if [[ -d ${ATLAS_RES_PATH} ]]; then
#    echo "${ATLAS_RES_PATH} exist!"
    sed -i.bak '/FilePathData/d' ${CSI_FILE}
    line=`cat "${CSI_FILE}" | grep -n "<ImageFiles>" | awk -F":" '{print $1}'`
    line=`expr ${line} + 1`
#    echo $line
    for PNG_FILE in `ls "${ATLAS_RES_PATH}/" | grep ".png$" | awk -F"/" '{print $NF}'`; do
#        echo ${PNG_FILE}
        # Note: on mac, sed is different (e.g. command i expects \ followed by text)
        # Please use gsed instead, or set `alias sed=gsed`
        gsed -i.bak "${line}i\ \ \ \ \ \ <FilePathData Path=\"${ATLAS_NAME}/${PNG_FILE}\" />" ${CSI_FILE}
    done
    rm ${CSI_FILE}.bak
fi
