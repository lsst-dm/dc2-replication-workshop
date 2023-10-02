# A script that installs a specific version of the LSST stack
# totally from scratch.
#
# It spawns a screen and runs the installation in there, but
# does not exit it.
# 
# IMPORTANT: Do NOT run this script while an LSST stack environment
# is active in your current shell.



# tag is the first passed argument
tag=$1
echo $tag

# Open a new bash shell and run a squence of commands, one-by-one
cmd1='cd /home/nima'
cmd2='mkdir nsst_'$tag
cmd3='cd nsst_'$tag
cmd4='curl -OL https://ls.st/lsstinstall'
cmd5='chmod +x lsstinstall'
cmd6='bash lsstinstall -X '$tag
cmd7='source "/home/nima/nsst_'$tag'/loadLSST.bash"'
cmd8='eups distrib install -t '$tag' lsst_distrib'
cmd9='setup lsst_distrib'
cmd10='cd /home/nima/lsst_startup/tickets/DM-34851'
cmd11='pipetask run -b /repo/dc2 -p /home/nima/lsst_startup/tickets/DM-34851/gen_calexps.yaml -i "u/nsedaghat/CorrespondingRawsGoodies" -o u/nsedaghat/RegeneratedCalexps_'$tag'_orig_yaml -j 30 -d "instrument='\''LSSTCam-imSim'\'' AND skymap='\''DC2'\'' AND exposure=635810"'

 
# Create a new screen session and run the commands.
screen -dmS $tag bash -c "echo $cmd1; $cmd1; echo $cmd2; $cmd2; echo $cmd3; $cmd3; echo $cmd4; $cmd4; echo $cmd5; $cmd5; echo $cmd6; $cmd6; echo $cmd7; $cmd7; echo $cmd8; $cmd8; echo $cmd9; $cmd9; echo $cmd10; $cmd10; echo $cmd11; $cmd11; exec bash"



