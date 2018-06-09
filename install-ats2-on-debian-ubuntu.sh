#!/usr/bin/env sh

# Variation of githwxi/C9-ATS2-install.sh at https://gist.github.com/githwxi/7e31f4fd4df92125b73c
#
# This variation may be more handy to install ATS and Contrib at any proper
# location and to easily update it. The variations are in a few points:
# configurable using variables, installs Contrib in the while, moves
# additional utilities such as `atscc2js` in the installation directory then
# creates symbolic links from the main `bin` directory to `lib/*/bin`, do some
# clean‑up (make clean and safely strip libraries and executables), updates
# the source directories if they already exist instead of always cloning the
# repositories, starts with a light clone.
#
# Edit the configuration variables below. Note you still have to clear the
# install directory before each update, as this script don't do it for you,
# for safety.

# Installation directory: edit to set it to your own.
INST_DIR="$HOME/apps/ats"
# For when compiling with Z3 support: edit to set it to your own.
export C_INCLUDE_PATH="$HOME/apps/z3/include"
export LIBRARY_PATH="$HOME/apps/z3/lib"
# Values: 1 means Yes, 0 means No.
INSTALL_BUILD_DEPENDENCIES=0
WITH_PATSOLVE_Z3=0
WITH_PATSOLVE_SMT2=1
WITH_ATSCC2JS=1
WITH_ATSCC2PY3=1
WITH_ATSCC2PHP=1

######
#
# A shell script for
# installing ATS2 + ATS2-contrib
#
######
#
# Author: Hongwei Xi
# Authoremail: gmhwxiATgmailDOTcom
#
######

if [ $INSTALL_BUILD_DEPENDENCIES -eq 1 ]; then
   sudo apt-get update
   sudo apt-get install -y gcc
   sudo apt-get install -y git
   sudo apt-get install -y build-essential
   sudo apt-get install -y libgmp-dev libgc-dev libjson-c-dev
fi

######

exit_if_failed() {
   if [ $? -ne 0 ]; then
      echo "Exit on failure."
      exit 1
   fi
}

get_or_update_git_clone() {
   # Caller defines DIR and URL.
   if [ \! -d $DIR/.git ]; then
      if [ -d $DIR ]; then
         # Directory exists, but is not a valid git clone: reset.
         echo "Please, delete the $DIR directory, it is not a Git clone."
         exit 1;
      fi
      git clone -b master --single-branch --depth 1 $URL $DIR
      exit_if_failed
   else
      (cd $DIR && git fetch --depth 1 && git reset --hard origin/master)
      exit_if_failed
   fi;
}

DIR=ATS2
URL=git://git.code.sf.net/p/ats2-lang/code
get_or_update_git_clone

DIR=ATS2-contrib
URL=https://github.com/githwxi/ATS-Postiats-contrib.git
get_or_update_git_clone

######
#
# Building patsopt + patscc
#
(cd ATS2 && ./configure --prefix="$INST_DIR"); exit_if_failed
(cd ATS2 && make all && make clean); exit_if_failed
#
######
#
# Installing patscc and patsopt
#
(cd ATS2 && make install); exit_if_failed

export PATSHOME=$(find "$INST_DIR/lib" -mindepth 1 -maxdepth 1 -type d -name "ats2-postiats-*")
if [ \! $(echo $PATSHOME | wc -w) -eq 1 ]; then
   echo "Error: there should be exactly one ATS2 version in $INST_DIR/lib"
   exit
fi;
export PATSCONTRIB="$PWD/ATS2"  # The build-time one, not the final one.
export PATH="$INST_DIR/bin:$PATH"
PATSHOME_NAME=$(basename $PATSHOME)

ln -fs lib/$PATSHOME_NAME/share $INST_DIR/share
(cd ATS2-contrib && cp -r contrib "$INST_DIR/")
(cd ATS2-contrib && cp -r document "$INST_DIR/doc")
(cd ATS2 && cp -r doc "$INST_DIR/")
#
######

######
#
# For parsing constraints
#
(cd ATS2/contrib/ATS-extsolve && make DATS_C); exit_if_failed
#
# For building patsolve_z3
if [ $WITH_PATSOLVE_Z3 -eq 1 ]; then
   (cd ATS2/contrib/ATS-extsolve-z3 && make all && make clean); exit_if_failed
   (cd ATS2/contrib/ATS-extsolve-z3/bin && mv -f patsolve_z3 $PATSHOME/bin); exit_if_failed
fi;
#
# For building patsolve_smt2
if [ $WITH_PATSOLVE_SMT2 -eq 1 ]; then
   (cd ATS2/contrib/ATS-extsolve-smt2 && make all && make clean); exit_if_failed
   (cd ATS2/contrib/ATS-extsolve-smt2/bin && mv -f patsolve_smt2 $PATSHOME/bin); exit_if_failed
fi;
#
######
#
# For parsing C code
# generated from ATS source
#
(cd ATS2/contrib/CATS-parsemit && make all); exit_if_failed
#
# For building atscc2js
#
if [ $WITH_ATSCC2JS -eq 1 ]; then
   (cd ATS2/contrib/CATS-atscc2js && make all && make clean); exit_if_failed
   (cd ATS2/contrib/CATS-atscc2js && mv -f bin/atscc2js $PATSHOME/bin); exit_if_failed
   ln -s "../lib/$PATSHOME_NAME/bin/atscc2js" "$INST_DIR/bin/atscc2js"
fi;
#
# For building atscc2py3
#
if [ $WITH_ATSCC2PY3 -eq 1 ]; then
   (cd ATS2/contrib/CATS-atscc2py3 && make all && make clean); exit_if_failed
   (cd ATS2/contrib/CATS-atscc2py3 && mv -f bin/atscc2py3 $PATSHOME/bin); exit_if_failed
   ln -s "../lib/$PATSHOME_NAME/bin/atscc2py3" "$INST_DIR/bin/atscc2py3"
fi;
#
# For building atscc2php
#
if [ $WITH_ATSCC2PHP -eq 1 ]; then
   (cd ATS2/contrib/CATS-atscc2php && make all && make clean); exit_if_failed
   (cd ATS2/contrib/CATS-atscc2php && mv -f bin/atscc2php $PATSHOME/bin); exit_if_failed
   ln -s "../lib/$PATSHOME_NAME/bin/atscc2php" "$INST_DIR/bin/atscc2php"
fi;
#
# Safely strip executables and libraries
#
EXECUTABLES=$(find "$INST_DIR" -type f -perm -u=x -exec file -i {} \; | grep "charset=binary" | sed -n "s/^\(.*\):.*$/\1/p")
for FILE in $EXECUTABLES; do
   COMMAND="strip --strip-unneeded \"$FILE\""
   echo $COMMAND
   eval $COMMAND
done
#
# Reminder
#
echo "========================="
echo "Please, ensure your environement (ex. from \`.profile\`) has these:"
echo "export PATSHOME=$PATSHOME"
echo "export PATSCONTRIB=$INST_DIR"
echo "export PATH=$INST_DIR/bin:\$PATH"
echo "========================="
#
###### end of [install-ats2-on-debian-ubuntu.sh] ######
