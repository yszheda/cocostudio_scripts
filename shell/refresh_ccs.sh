#!/bin/bash
# Refresh cocostudio ccs

CCS_FILE=$1

if [[ ! -f ${CCS_FILE} ]]; then
    echo "${CCS_FILE} is not existed!"
    exit 1
fi

ATLAS_NAME=`echo ${CCS_FILE} | awk -F"/" '{print $NF}' | sed 's/.ccs//'`

HEADER="<Solution>
  <PropertyGroup Name=\"${ATLAS_NAME}\" Version=\"2.0.8.0\" Type=\"CocosStudio\" />
  <SolutionFolder>
    <Group ctype=\"ResourceGroup\">
      <RootFolder Name=\".\">
"

FOOTER="
      </RootFolder>
    </Group>
  </SolutionFolder>
</Solution>
"

INITIAL_XML_DEPTH=4

CSD_FMT="<Project Name=\"%s\" />"
CSI_FMT="<PlistInfo Name=\"%s\" />"
PNG_FMT="<Image Name=\"%s\" />"
FILE_FMT="<File Name=\"%s\" />"

CSD_EXT="csd"
CSI_EXT="csi"
PNG_EXT="png"

function file_xml {
    local FILE="$1"
    local DEPTH="$2"
#    DEPTH=`expr ${DEPTH} + ${INITIAL_XML_DEPTH}`

    local FILE_NAME=`echo ${FILE} | awk -F"/" '{print $NF}'`
    local EXTENTION=`echo ${FILE_NAME} | awk -F"." '{print $NF}'`
    local XML=""
    if [[ "${EXTENTION}" = "${CSD_EXT}" ]]; then
        XML=`printf "${CSD_FMT}" "${FILE_NAME}"`
    elif [[ "${EXTENTION}" = "${CSI_EXT}" ]]; then
        XML=`printf "${CSI_FMT}" "${FILE_NAME}"`
    elif [[ "${EXTENTION}" = "${PNG_EXT}" ]]; then
        XML=`printf "${PNG_FMT}" "${FILE_NAME}"`
    else
        XML=`printf "${FILE_FMT}" "${FILE_NAME}"`
    fi

    for ((i = 0; i < ${DEPTH}; i++)); do
        XML="  ${XML}"
    done

    echo "${XML}"
}

function folder_xml {
    local FOLDER="$1"
    local DEPTH="$2"
#    DEPTH=`expr ${DEPTH} + ${INITIAL_XML_DEPTH}`

#    echo ${FOLDER}
    local FOLDER_NAME=`basename ${FOLDER}`
#    echo ${FOLDER_NAME}
    local HEADER=`printf "<Folder Name=\"%s\">" "${FOLDER_NAME}"`
    local FOOTER="</Folder>"
    for ((i = 0; i < ${DEPTH}; i++)); do
        HEADER="  ${HEADER}"
        FOOTER="  ${FOOTER}"
    done

    local XML=`echo "${HEADER}"`

    local CONTENT=""
    local ITEM_DEPTH=`expr ${DEPTH} + 1`
    for ITEM in `ls ${FOLDER}`; do
        local ITEM_PATH="${FOLDER}/${ITEM}"
        if [[ -f "${ITEM_PATH}" ]]; then
            CONTENT="${CONTENT}\n`file_xml ${ITEM_PATH} ${ITEM_DEPTH}`"
        elif [[ -d "${ITEM_PATH}" ]]; then
            CONTENT="${CONTENT}\n`folder_xml ${ITEM_PATH} ${ITEM_DEPTH}`"
        fi
    done

    XML="${XML}`echo "${CONTENT}"`"
    XML="${XML}\n`echo "${FOOTER}"`"

    echo "${XML}"
}

RES_PATH="`dirname ${CCS_FILE}`/cocosstudio/"
# CONTENT=`folder_xml ${RES_PATH} ${INITIAL_XML_DEPTH}`
CONTENT=""
for ITEM in `ls ${RES_PATH}`; do
    ITEM_PATH="${RES_PATH}/${ITEM}"
    if [[ -f "${ITEM_PATH}" ]]; then
        CONTENT="${CONTENT}\n`file_xml ${ITEM_PATH} ${INITIAL_XML_DEPTH}`"
    elif [[ -d "${ITEM_PATH}" ]]; then
        CONTENT="${CONTENT}\n`folder_xml ${ITEM_PATH} ${INITIAL_XML_DEPTH}`"
    fi
done

printf "${HEADER}" > ${CCS_FILE}
printf "${CONTENT}" >> ${CCS_FILE}
printf "${FOOTER}" >> ${CCS_FILE}
