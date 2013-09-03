#!/bin/bash
#
# Unified SAAL installer script
# Maintainer: Sesostris Vieira (sesostris at interlegis.leg.br)
#
# Note: For SERVER installation, this script must be run as root.
#       For DEV installation, that uses python virtualenv
#       environment, run as simple user.

usage() {
	echo ""
	echo "Unified SAAL installer script"
	echo "Maintainer: Sesostris Vieira (sesostris at interlegis.leg.br)"
	echo ""
	echo "Usage $0 dev|server [options]"
	echo ""
	echo "For SERVER installation, this script must be run as root."
	echo "For DEV installation, that uses python virtualenv environment, run as simple user."
	echo ""
	echo "Valid options are (only to server installation):"
	echo "	-e | --engine <engine name>	: Database engine to connect to. Engine names can be: $ENGINE_LIST. Default is postgresql_psycopg2"
	echo "	-h | --host <host name>		: Database hostname. Default: localhost"
	echo "	-p | --port <port number>	: TCP/IP port number to connect with database server. Default: 5432"
	echo "	-n | --name <db name>		: Database name. Default: saal"
	echo "	-u | --user <user name>		: User name to connect to database. Default: saal"
	echo "	-w | --password <password>	: User password to connect to database. Empty default value"
	echo "	-s | --server <server name>	: Apache server name that runs the saal. Default: www.saal.leg.br"
	echo "	--help				: Show this help"
	echo ""
	echo "IMPORTANT NOTE!"
	echo "==============="
	echo "For Oracle installations you need manually install and configure the cx_oracle"
	echo "python extension module (http://cx-oracle.sourceforge.net/)."
	echo "See https://docs.djangoproject.com/en/dev/ref/databases/#oracle-notes"
	echo "for more details."
}

try()
{
	echo "## runing: $@ ##"
	"$@"
	if [ $? -ne 0 ]
	then
		echo "Error trying $@"
		exit 1
	fi
}

apt_install()
{
	echo "Some needed packages will be installed with apt-get, in sudo mode."
	echo "If requested give your SUDOer password"
	try $1 apt-get install build-essential graphviz graphviz-dev git python-pip python-dev python-cairo libxml2-dev libxslt1-dev gettext
}

apache_install()
{
	echo "WARNING: Apache will be installed but not tunned. You will tune it after installation!"
	SAAL_PATH=`pwd`
	SERVER_NAME=$1
	try apt-get install apache2 libapache2-mod-wsgi
	try a2enmod wsgi
	echo "## Configuring Apache Virtual Host ##"
	sed "s/www.saal.leg.br/$SERVER_NAME/g" etc/sites-avaiable/saal.erb | sed "s:/var/interlegis/saal:$SAAL_PATH:g" > /etc/apache2/sites-available/saal.erb
	if [ $? -ne 0 ]
	then
		echo "Error configuring Apache Virtual Host with SERVER_NAME=$SERVER_NAME, SAAL_PATH=$SAAL_PATH."
		exit 1
	fi
	try rm -Rf static_collected/
	try python manage.py collectstatic
	try a2ensite saal.erb
	try a2dissite default
	try service apache2 restart
}

virtual_env()
{
	try sudo pip install virtualenv
	try rm -Rf ./env/
	try virtualenv ./env/
	CAIRO_PATH=`python -c 'import cairo; print cairo.__path__[0]'`
	try ln -s $CAIRO_PATH env/lib/python2.7/site-packages/
}

pip_install()
{
	try pip install $1 --requirement=requirements.txt
}

treemenus_install()
{
	try git clone https://github.com/jphalip/django-treemenus.git
	try cd django-treemenus/
	try python setup.py install
	cd ..
	rm -Rf django-treemenus/
}

database_dev()
{
	try cp -af saal/database_settings_sqlite3.py saal/database_settings.py
	try python manage.py syncdb
	try python manage.py migrate --all
	try python manage.py create_saal_groups
	try python manage.py loaddata fixtures/dev/*.json
}

database_server()
{
	ENGINE=$1
	HOST=$2
	PORT=$3
	DB_NAME=$4
	USER_NAME=$5
	PASSWORD=$6
	case "$ENGINE" in
		postgresql_psycopg2) try apt-get install python-psycopg2 ;;
		mysql) try apt-get install python-mysqldb ;;
		oracle) echo "cx_oracle will not be installed by this script!!!!!";;
	esac
	try rm saal/database_settings.py
	echo "## Generating new saal/database_settings.py ##"
	sed "s:engine_name:$ENGINE:g" saal/database_settings_server_prototype.py | sed "s:host_name:$HOST:g" | sed "s:port_number:$PORT:g" | sed "s:db_name:$DB_NAME:g" | sed "s:user_name:$USER_NAME:g" | sed "s:user_password:$PASSWORD:g" > saal/database_settings.py
	if [ $? -ne 0 ]
	then
		echo "Error generating saal/database_settings.py with ENGINE=$ENGINE, HOST=$HOST, PORT=$PORT, DB_NAME=$DB_NAME, USER_NAME=$USER_NAME, PASSWORD=$PASSWORD"
		exit 1
	fi
	try python manage.py syncdb
	try python manage.py migrate --all
	try python manage.py create_saal_groups
}

compile_messages()
{
	bash etc/utils/compilemessages.sh pt_BR
}


case "$1" in
	dev)
		echo "DEV install"
		apt_install sudo
		virtual_env
		pip_install --environment=./env/
		try source ./env/bin/activate
		treemenus_install
		database_dev
		compile_messages
		;;
	server)
		shift
		echo "SERVER install"
		# Make sure only root can run our script
		if [[ $EUID -ne 0 ]]; then
			echo "Server installation must be run as root" 1>&2
			exit 1
		fi
		OPTIONS=':e:h:p:n:u:w:s:'
		ENGINE_LIST=" postgresql_psycopg2 mysql oracle " # no sqlite in server mode!
		# Default values
		ENGINE=postgresql_psycopg2
		HOST=localhost
		PORT=5432
		DB_NAME=saal
		USER_NAME=saal
		PASSWORD=
		SERVER_NAME=www.saal.leg.br
		FLAG_ANY_OPTION=false
		while getopts $OPTIONS option
		do
			case $option in
				e )
					FLAG_ANY_OPTION=true
					ENGINE=$OPTARG
					if [[ ! "$ENGINE_LIST" =~ " $ENGINE " ]]
					then
						echo "Engine can be only: $ENGINE_LIST"
						exit 1
					fi
					;;
				h ) HOST=$OPTARG		; FLAG_ANY_OPTION=true;;
				p ) PORT=$OPTARG		; FLAG_ANY_OPTION=true;;
				n ) DB_NAME=$OPTARG		; FLAG_ANY_OPTION=true;;
				u ) USER_NAME=$OPTARG	; FLAG_ANY_OPTION=true;;
				w ) PASSWORD=$OPTARG	; FLAG_ANY_OPTION=true;;
				s ) SERVER_NAME=$OPTARG ; FLAG_ANY_OPTION=true;;
				\?) 
					echo "Unknown option: -$OPTARG" >&2
					usage
					exit 1
					;;
				: ) echo "Missing option argument for -$OPTARG" >&2; exit 1;;
				* ) echo "Unimplimented option: -$OPTARG" >&2; exit 1;;
			esac
		done
		if [[ ! $FLAG_ANY_OPTION == true ]]
		then
			usage
			exit 1
		fi
		echo "engine = $ENGINE, host = $HOST, port = $PORT, db_name = $DB_NAME, user_name = $USER_NAME, password = $PASSWORD"
		apt_install
		pip_install
		treemenus_install
		database_server $ENGINE $HOST $PORT $DB_NAME $USER_NAME $PASSWORD
		apache_install $SERVER_NAME
		compile_messages
		;;
	*)
		usage
		exit 1
		;;
esac

exit 0
