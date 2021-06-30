#!/bin/bash

INFO_TEXT="\e[1;32m[INFO]\e[0m"
ERROR_TEXT="\e[1;31m[ERROR]\e[0m"

# make all shell files executable
echo -e "${INFO_TEXT} Making shell scripts executable [...]"
chmod +x *.sh

# installing deps and running django server
echo -e "${INFO_TEXT} Entering into 'server' [...]"
cd server
echo -e "${INFO_TEXT} Installing Python Requirements [...]"
pip install -r requirements.txt
cd ..
echo -e "${INFO_TEXT} Running Django Server in Background [...]"
bash ./run.sh 5000 &

# render next.js pages and static file generation
echo -e "${INFO_TEXT} Entering into 'client' [...]"
cd client
npm install 
echo -e "${INFO_TEXT} Building Next.js [...]" 
npm run build --max_old_space_size=1024
echo -e "${INFO_TEXT} Exporting Next.js [...]" 
npm run export
cd ..

# cleaning up background django server
echo -e "${INFO_TEXT} Killing Background Django Proccess [...]" 
fuser -k 5000/tcp

# copying static assets
if [ -d "./server/githubsrm/dist" ]
then
echo -e "${INFO_TEXT} Cleaning up 'server/githubsrm/dist' folder [...]" 
rm -rf server/githubsrm/dist
fi
if [ -d "./server/githubsrm/static" ]
then
echo -e "${INFO_TEXT} Cleaning up 'server/githubsrm/static' folder [...]" 
rm -rf server/githubsrm/static
fi
echo -e "${INFO_TEXT} Moving folder 'client/out' to 'server/githubsrm/dist' [...]" 
mv client/out server/githubsrm/dist

# running collectstatic
echo -e "${INFO_TEXT} Running Django collectstatic [...]"
cd server/githubsrm
python3 manage.py collectstatic --no-input
echo -e "${INFO_TEXT} Execution of 'deploy.sh' script completed."