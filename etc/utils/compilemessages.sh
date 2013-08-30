#! /bin/bash

APPS=( "saal" "smat" "spat" )

django-admin.py compilemessages -l $1

for APP in "${APPS[@]}"
do
	cd $APP
	django-admin.py compilemessages -l $1
	cd ..
done

echo "Done!"
