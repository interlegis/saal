#! /bin/bash

APPS=( "saal" "smat" )

django-admin.py compilemessages

for APP in "${APPS[@]}"
do
	cd $APP
	django-admin.py compilemessages
	cd ..
done

echo "Done!"
