#! /bin/bash

APPS=( "saal" "smat" "spat" )

IGNORE_LIST=""
for APP in "${APPS[@]}"
do
	 IGNORE_LIST="$IGNORE_LIST -i $APP"
done


if [ ! -d "conf/locale" ]; then
	mkdir -p conf/locale
fi

django-admin.py makemessages -l $1 $IGNORE_LIST

for APP in "${APPS[@]}"
do
	echo -n "$APP: "
	cd $APP
	if [ ! -d "locale" ]; then
		mkdir locale
	fi
	django-admin.py makemessages -l $1
	cd ..
done

echo "Done!"