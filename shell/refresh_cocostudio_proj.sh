#!/bin/bash
# Refresh the following files of the given cocostudio project:
# *.ccs
# *.csi: cocostudio SpriteFrameSheet

UI_PROJECT_PATH=$1

PWD=`dirname $0`

for RES_PATH in `find "${UI_PROJECT_PATH}" -name "cocosstudio"`; do
#    echo ${RES_PATH}
    for CSI_FILE in `find "${RES_PATH}" -name "*.csi"`; do
        echo "Refresh CSI: ${CSI_FILE}"
        ${PWD}/refresh_csi.sh ${CSI_FILE}
    done
done

for CSD_FILE in `find "${UI_PROJECT_PATH}" -name "*.csd"`; do
    echo "Refresh CSD: ${CSD_FILE}"
    ${PWD}/refresh_csd.sh ${CSD_FILE}
done

for CCS_FILE in `find "${UI_PROJECT_PATH}" -name "*.ccs"`; do
    echo "Refresh CCS: ${CCS_FILE}"
    ${PWD}/refresh_ccs.sh ${CCS_FILE}
done

