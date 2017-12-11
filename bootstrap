#!/bin/sh
#
# This script allows you to install openbaton. To execute it:
#
# sh <(curl -s http://get.openbaton.org/bootstrap) [help | clean | enable-persistence | configure-remote-rabbitmq] | [[upgrade] [--openbaton-components=<all | openbaton-xxx,openbaton-yyy,...>]] | [[release | develop] [--openbaton-bootstrap-version=X.Y.Z (with X.Y.Z >= 3.2.0)] [--config-file=<absolute path to configuration file>]]
#
# If you need support, get in contact with us at: info@openbaton.org



##########################
#### General Settings ####
##########################

set -u
#set -x # only for DEBUG

# Make available the functions defined in /lib/lsb/init-functions
. /lib/lsb/init-functions


##############################
#### Execution privileges ####
##############################

USER="$(id -un 2>/dev/null || true)"

check_binary () {
  echo -n " * Checking for '${1}' ... "
  if command -v ${1} >/dev/null 2>&1; then
     echo "OK"
     return 0
  else
     echo >&2 "FAILED"
     return 1
  fi
}

_ex='sh -c'
if [ "${USER}" != "root" ]; then
    if check_binary sudo; then
        _ex='sudo -E sh -c'
    elif check_binary su; then
        _ex='su -c'
    fi
fi


##########################
#### Global Variables ####
##########################

OPENBATON_BOOTSTRAP_VERSION_DEFAULT=latest
openbaton_bootstrap_version=${openbaton_bootstrap_version:-$OPENBATON_BOOTSTRAP_VERSION_DEFAULT}

OPENBATON_BOOTSTRAP_ENV_FILE="/tmp/bootstrap_env"

OPENBATON_BOOTSTRAP_FUNCTIONS_BASE_URL=http://get.openbaton.org/bootstraps/

DEBIAN_FRONTEND_DEFAULT="dialog"
export DEBIAN_FRONTEND=${DEBIAN_FRONTEND:-$DEBIAN_FRONTEND_DEFAULT}

OS_ARCHITECTURE=$(uname -m)
OS_TYPE=$(uname -a | awk -F' ' '{ print $1 }')

case "${OS_TYPE}" in
    'Linux')
        $_ex 'apt-get update && apt-get install -y lsb-core'
        OS_DISTRIBUTION_ID=$( lsb_release -a 2>/dev/null | grep "Distributor ID" | sed "s/[ \t]*//g" | awk -F':' '{ print $2 }')
        OS_DISTRIBUTION_RELEASE=$( lsb_release -a 2>/dev/null | grep "Release" | sed "s/[ \t]*//g" | awk -F':' '{ print $2 }' )
        OS_DISTRIBUTION_CODENAME=$( lsb_release -a 2>/dev/null | grep "Codename" | sed "s/[ \t]*//g" | awk -F':' '{ print $2 }' )
        ;;
    'Darwin')
        OS_DISTRIBUTION_ID=$( sw_vers -productName )
        OS_DISTRIBUTION_RELEASE=$( sw_vers -productVersion )
        ;;
    *)
        OS_DISTRIBUTION_ID=undefined
        OS_DISTRIBUTION_RELEASE=undefined
        ;;
esac

if [ "${OS_DISTRIBUTION_RELEASE}" != "undefined" ]; then
    OS_DISTRIBUTION_RELEASE_MAJOR=$( echo ${OS_DISTRIBUTION_RELEASE} | awk -F'.' '{ print $1 }' )
else
    OS_DISTRIBUTION_RELEASE_MAJOR=undefined
fi

OPENBATON_BOOTSTRAP_SUBCOMMAND_DEFAULT=release


###############
#### Usage ####
###############

usage () {
    echo ""
    echo " * Usage: (The 'release' installation is the DEFAULT)"
    echo "    ./bootstrap [help | clean | enable-persistence | configure-remote-rabbitmq] | [[upgrade] [--openbaton-components=<all | openbaton-xxx,openbaton-yyy,...>]] | [[release | develop] [--openbaton-bootstrap-version=X.Y.Z (with X.Y.Z >= 3.2.0)] [--config-file=<absolute path to configuration file>]]                                         (if bootstrap already locally available)"
    echo "    sh <(curl -s http://get.openbaton.org/bootstrap) [help | clean | enable-persistence | configure-remote-rabbitmq] | [[upgrade] [--openbaton-components=<all | openbaton-xxx,openbaton-yyy,...>]] | [[release | develop] [--openbaton-bootstrap-version=X.Y.Z (with X.Y.Z >= 3.2.0)] [--config-file=<absolute path to configuration file>]]    (otherwise)"
    echo ""
    echo " * If you need support, get in contact with us at: info@openbaton.org"
}


##############
#### Main ####
##############

prereq () {
    $_ex 'apt-get install -y wget whiptail'

    wget -O bootstrap-common-functions "${OPENBATON_BOOTSTRAP_FUNCTIONS_BASE_URL}/${openbaton_bootstrap_version}/bootstrap-common-functions"
    . ./bootstrap-common-functions
}

check_jre_8_installed () {
    jre_8_available=$($_ex 'apt-cache search openjdk-8-jre | wc -l')
    if [ "${jre_8_available}" != "0" ]; then
        return
    fi

    jre_8_installed=$(dpkg -l | grep "openjdk-8-jre:" | awk -F' ' '{print $1}' | wc -l)
    if [ "${jre_8_installed}" = "0" ]; then
        log_failure_msg "The 'openjdk-8-jre' package is a required dependency and it seems to be not installed and not available"
        exit 1
    fi
}

main_src () {
    wget -O bootstrap-src-functions "${OPENBATON_BOOTSTRAP_FUNCTIONS_BASE_URL}/${openbaton_bootstrap_version}/bootstrap-src-functions"
    . ./bootstrap-src-functions
    src_bootstrap
}

main_deb () {
    check_jre_8_installed

    wget -O bootstrap-deb-functions "${OPENBATON_BOOTSTRAP_FUNCTIONS_BASE_URL}/${openbaton_bootstrap_version}/bootstrap-deb-functions"
    . ./bootstrap-deb-functions
    deb_bootstrap "${1}" "${2}"           # ${1} = release/nightly ; ${2} = distribution codename
}

main () {
    # In case of "noninteractive" FRONTEND the latest RELEASE package will be installed
    if [ "${DEBIAN_FRONTEND}" != "Noninteractive" -a "${DEBIAN_FRONTEND}" != "noninteractive" ]; then
        bootstrap_subcommand=$( whiptail --title "Open Baton General Menu" --menu "\nPlease, choose the operation to be executed:" 15 140 5 \
            "1" "Print Open Baton usage" \
            "2" "Procede with the Open Baton installation" \
            "3" "Procede with the Open Baton installation cleaning" \
            "4" "Enable the Open Baton persistence" \
            "5" "Configure a remote RabbitMQ instance to work with Open Baton" 3>&1 1>&2 2>&3 )

        case ${bootstrap_subcommand} in
            1 )
                bootstrap_subcommand="help"
                ;;
            2 )
                bootstrap_subcommand="install"
                ;;
            3 )
                bootstrap_subcommand="clean"
                ;;
            4 )
                bootstrap_subcommand="enable-persistence"
                ;;
            5 )
                bootstrap_subcommand="configure-remote-rabbitmq"
                ;;
        esac

        if [ -z "${bootstrap_subcommand}" ]; then
            log_warning_msg "Exiting Open Baton Menu."
            exit 0
        elif [ "${bootstrap_subcommand}" = "install" ]; then
            install_type=$( whiptail --title "Open Baton Installation Menu" --menu "\nPlease, choose the preferred Open Baton installation:" 15 140 5 \
                "1" "RELEASE: it will be executed the installation of the DEBIAN packages of the latest released components" \
                "2" "DEVELOP: it will be executed the download of the SOURCE code for the desired components (which will be run in screens)" 3>&1 1>&2 2>&3 )
            case ${install_type} in
                1 )
                    prereq
                    main_deb release "${OS_DISTRIBUTION_CODENAME}"
                    ;;
                2 )
                    prereq
                    main_src
                    ;;
                #3 )
                #    main_deb nightly "${OS_DISTRIBUTION_CODENAME}"
                #    ;;
                * )
                    log_warning_msg "Open Baton installation aborted."
                    exit 1
                    ;;
            esac
        else
            exec_bootstrap_subcommand "${bootstrap_subcommand}"
        fi
    else
        # Non interactive debian release installation with the default values (when non interactive installation and no config file has been passed)
        prereq
        main_deb release "${OS_DISTRIBUTION_CODENAME}"
    fi

    log_success_msg "Open Baton operation completed"
}

exec_bootstrap_subcommand () {
    bootstrap_subcommand="${1}"

    case ${bootstrap_subcommand} in
        "help")
            usage
            exit 1
            ;;
        "release" )
            echo " * Installing the latest RELEASE package"
            prereq
            main_deb release "${OS_DISTRIBUTION_CODENAME}"
            ;;
        "develop" )
            # Check for OS: the develop installation works (i.e.: it has been tested) on Ubuntu 16.04 or later
            if [ "${OS_DISTRIBUTION_ID}" = "Ubuntu" -a "${OS_DISTRIBUTION_RELEASE}" \< "16.04" ]; then
                echo " * Sorry, If you want to install the source code through this bootstrap you need a machine with Ubuntu Xenial (16.04) or later."
                echo " * In case you want to install the source code on a different OS you need to manually install Java 8 (if needed) and clone the repositories from ${OPENBATON_HOME_REPO_URL}"
                exit 0
            fi

            echo " * Installing the latest source code"
            prereq
            main_src
            ;;
        "clean" )
            echo " * Cleaning the Open Baton installation"
            prereq
            clean
            exit 0
            ;;
        "enable-persistence" )
            prereq
            install_mysql
            exit 0
            ;;
        "configure-remote-rabbitmq" )
            prereq
            configure_remote_rabbitmq
            exit 0
            ;;
        "upgrade" )
            echo " * Upgrade the Open Baton installation"
            prereq
            upgrade
            exit 0
            ;;
        "*")
            usage
            exit 1
            ;;
    esac
}


#####################
#### Entry Point ####
#####################

if [ -n "${1+1}" ]; then
    if [ -f ${OPENBATON_BOOTSTRAP_ENV_FILE} ]; then
        rm ${OPENBATON_BOOTSTRAP_ENV_FILE}
    fi

    bootstrap_subcommand=""
    for arg in $@ ; do
        arg_id=$(echo $arg | cut -c1-2)
        arg_key=${arg}
        arg_value=

        if [ ${arg_id} != "--" ]; then # Subcommands
            case ${arg} in
                "release" | "develop" | "clean" | "enable-persistence" | "configure-remote-rabbitmq" | "upgrade" )
                    bootstrap_subcommand=${arg}
                    ;;
                * )
                    # TODO: temporary fix
                    #########################################################################################################################################
                    arg_key=$( echo ${arg} | cut -c2-  | awk -F'=' '{ print $1}' )
                    if [ "${arg_key}" = "configFile" ]; then
                        log_failure_msg "The argument '-configFile' will be not supported anymore from the next version. Please use '--config-file' instead."
                        arg_value=$( echo ${arg} | cut -c2- | awk -F'=' '{ print $2}' )
                        if [ -f ${arg_value} ]; then
                            echo " * Installing Open Baton using the following configuration file:"
                            echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                            cat ${arg_value}
                            echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                            set -a # Mark the variables set in the configuration file for export to the environment of subsequent commands
                            . ${arg_value}
                        else
                            log_failure_msg "Configuration file '${arg_value}' does not exist."
                        fi
                        continue
                    fi
                    #########################################################################################################################################

                    usage
                    exit 1
                    ;;
            esac
        else # Arguments
            arg_key=$( echo ${arg} | cut -c3-  | awk -F'=' '{ print $1}' )
            arg_value=$( echo ${arg} | cut -c3- | awk -F'=' '{ print $2}' )

            if [ "${arg_key}" = "config-file" ]; then
                if [ -f ${arg_value} ]; then
                    echo " * Installing Open Baton using the following configuration file:"
                    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    cat ${arg_value}
                    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    set -a # Mark the variables set in the configuration file for export to the environment of subsequent commands
                    . ${arg_value}
                else
                    log_failure_msg "Configuration file '${arg_value}' does not exist."
                fi
            else
                arg_key=$(echo ${arg_key} | tr '-' '_')
                echo "${arg_key}=${arg_value}" >> ${OPENBATON_BOOTSTRAP_ENV_FILE}
            fi
        fi
    done

    if [ -f ${OPENBATON_BOOTSTRAP_ENV_FILE} ]; then
        set -a # Mark the arguments passed by command line for export to the environment of subsequent commands
        . ${OPENBATON_BOOTSTRAP_ENV_FILE}
    fi

    #export DEBIAN_FRONTEND=${openbaton_installation_mode:-$DEBIAN_FRONTEND_DEFAULT}
    # TODO: temporary fix
    #########################################################################################################################################
    export DEBIAN_FRONTEND=${openbaton_installation_mode:-"try_old_param"}
    if [ "${DEBIAN_FRONTEND}" = "try_old_param" ]; then
        export DEBIAN_FRONTEND=${openbaton_installation_manner:-$DEBIAN_FRONTEND_DEFAULT}
    fi
    #########################################################################################################################################

    echo ""
    echo " *******************************************"
    echo " * System Details:"
    echo "     OS Architecture: ${OS_ARCHITECTURE}"
    echo "     OS Type: ${OS_TYPE}"
    echo "     OS Distribution ID: ${OS_DISTRIBUTION_ID}"
    echo "     OS Distribution Codename: ${OS_DISTRIBUTION_CODENAME}"
    echo "     OS Distribution Release: ${OS_DISTRIBUTION_RELEASE}"
    echo " *******************************************"
    echo ""

    # When invoked with only arguments passed by command line (no subcommands passed)
    if [ "${DEBIAN_FRONTEND}" != "Noninteractive" -a "${DEBIAN_FRONTEND}" != "noninteractive" ]; then
        if [ -z "${bootstrap_subcommand}" ]; then
            main
            exit 0
        fi
    fi

    bootstrap_subcommand=${bootstrap_subcommand:-$OPENBATON_BOOTSTRAP_SUBCOMMAND_DEFAULT}
    exec_bootstrap_subcommand "${bootstrap_subcommand}"

else # When invoked with 0 arguments: 'sh <(curl -s http://get.openbaton.org/bootstrap)'
    echo ""
    echo " *******************************************"
    echo " * System Details:"
    echo "     OS Architecture: ${OS_ARCHITECTURE}"
    echo "     OS Type: ${OS_TYPE}"
    echo "     OS Distribution ID: ${OS_DISTRIBUTION_ID}"
    echo "     OS Distribution Codename: ${OS_DISTRIBUTION_CODENAME}"
    echo "     OS Distribution Release: ${OS_DISTRIBUTION_RELEASE}"
    echo " *******************************************"
    echo ""

    main
fi

