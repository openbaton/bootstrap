#!/usr/bin/env bash
set -e

export DEBIAN_FRONTEND=noninteractive
_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

_openbaton_base_repo="https://github.com/openbaton/NFVO.git"
_openbaton_generic_vnfm_repo="https://github.com/openbaton/generic-vnfm.git"

_message_queue_base="apache-activemq-5.11.1"
_message_queue_archive="${_message_queue_base}-bin.tar.gz"
_message_queue_url="http://mirrors.sonic.net/apache/activemq/5.11.1/${_message_queue_archive}"

_base=/opt
_openbaton_base="${_base}/openbaton"
_nfvo="${_openbaton_base}/nfvo"
_generic_vnfm="${_openbaton_base}/generic-vnfm"

_installer_folder="${_base}/tmp"
_logfile="${_installer_folder}/log"

function checkBinary {
  echo -n " * Checking for '$1'..."
  if command -v $1 >/dev/null 2>&1; then
     echo "OK"
     return 0
   else
     echo >&2 "FAILED."
     return 1
   fi
}

function installMessageQueue() {
    echo "Downloading message queue.."
    pushd "${_openbaton_base}"
    wget "${_message_queue_url}"
    echo "Installing message queue..."
    tar -zxvf "${_openbaton_base}/${_message_queue_archive}"
    chown -R activemq ${_openbaton_base}/${_message_queue_base}
    ${_openbaton_base}/${_message_queue_base}/bin/activemq start
    popd
}

function prereq(){
    # TODO differentiate between fedora, OS X, ubuntu..
    sudo apt-get update && sudo apt-get -y install mysql-server openjdk-7-jdk curl wget screen git
}


function checkEnvironment {
  _error=0
  echo "Checking environment..."
  checkBinary java; _error=$(($_error + $?))
  checkBinary javac; _error=$(($_error + $?))
  checkBinary curl; _error=$(($_error + $?))
  checkBinary screen; _error=$(($_error + $?))
  checkBinary wget; _error=$(($_error + $?))
  if [ "0" != "$_error" ]; then
    echo >&2 "FAILED. Please install the above mentioned binaries."
    exit 1
  fi
}

function checkContainer {
    echo "Checking is running..."
    isRunning="$(curl -s -m 2 http://localhost:8080 > /dev/null; echo $?)"
    if [ "${isRunning}" != "0" ]; then
      startContainer
    fi
}

function checkoutOpenBaton {
    echo "Getting OpenBaton..."
    rm -rf "${_openbaton_base}"
    git clone --recursive "${_openbaton_base_repo}" "${_nfvo}"
}

function checkoutGenericVNFM {
    echo "Getting generic-vnfm..."
    git clone --recursive "${_openbaton_generic_vnfm_repo}" "${_generic_vnfm}"
}


function compileNFVO {
    echo "compiling the NFVO"
    pushd "${_nfvo}"
    ./openbaton.sh compile
    popd
}

function startNFVO {
    echo "starting the NFVO"
    pushd ${_nfvo}
    ./openbaton.sh start
}

function deployOpenBaton {
    pushd "${_nfvo}"
    compileNFVO
    startNFVO
}

function compileGenericVNFM {
    echo "compiling the generic VNFM"
    pushd "${_generic_vnfm}"
    git checkout develop
    ./generic-vnfm.sh compile
    popd
}

function startGenericVNFM {
    echo "starting the generic VNFM"
    pushd ${_generic_vnfm}
    ./generic-vnfm.sh start
}

function deployGenericVNFM {
    pushd "${_generic_vnfm}"
    compileGenericVNFM
    startGenericVNFM
}



function bootstrap() {
    [ ! -d ".git" ] || { echo "Do not bootstrap within a repository"; exit 4; }
    # install prerq
    prereq
    # checkout OpenBaton
    checkoutOpenBaton
    # moved message queue installation part
    installMessageQueue
    # check if all the required libraries are available
    checkEnvironment
    # checkout the generic VNFM code
    checkoutGenericVNFM
    # deploy and compile OpenBaton orchestrator
    deployOpenBaton
    # deploy and compile the Generic VNFM
    deployGenericVNFM
    echo "Now open http://localhost:8080/"

}

bootstrap

