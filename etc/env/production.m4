divert(`-1')
define(_TIMESTAMP_, patsubst(esyscmd(`date +%Y%m%d%H%M%S'), `
', `'))
define(_ADMINEMAIL_, root@draines.com)
define(_HOST_, valve)
define(_VHOST_, www.trinitynashville.org)
define(_VHOST2_, `trinitynashville.org www.tcnash.org tcnash.org www.trinity.tc trinity.tc')
define(_PROJECT_, tcnash)
define(_PROJECTBASE_, /apps/_PROJECT_)
define(_PROJECTROOT_, _PROJECTBASE_/current)
define(_CURRENT_, _PROJECTROOT_)
define(_RELEASEROOT_, _PROJECTBASE_/releases/_TIMESTAMP_)
define(_DOCUMENTROOT_, _PROJECTROOT_/static)
define(_TEMPLATEROOT_, /home/trinity/Dropbox/Trinity-WWW/www.tcnash.org)
define(_CONFIGROOT_, _PROJECTROOT_/etc)
define(_DJANGOROOT_, /apps/shared/django/1.1.1/django)
define(_DATABASE_NAME_, _PROJECTBASE_/tcnash-prod.db)
define(_USER_, deploy)
define(_GROUP_, nogroup)
divert
