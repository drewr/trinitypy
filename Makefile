LOCALDB = tcnash-local.db
PRODDB = /apps/tcnash/tcnash-prod.db
STAGEDB = /apps/tcnash-stage/tcnash-stage.db
WEBHOST = valve

default:
	@echo -n bootstrapping...
	@sed s,_DATABASE_NAME_,$(LOCALDB), <settings.py.in >settings.py.tmp
	@sed s,_TEMPLATEROOT_,user_templates, <settings.py.tmp >settings.py
	@rm settings.py.tmp
	@echo done

stage:
	bin/deploy stage

stagedb:
	@echo overwriting remote STAGE database...
	scp ${LOCALDB} deploy@${WEBHOST}:${STAGEDB}

clonestage:
	scp deploy@${WEBHOST}:${STAGEDB} ${LOCALDB}

production:
	bin/deploy production

proddb:
	@echo overwriting remote PRODUCTION database...
	scp ${LOCALDB} deploy@${WEBHOST}:${PRODDB}

cloneprod:
	scp deploy@${WEBHOST}:${STAGEDB} ${LOCALDB}

itunes:
	bin/ping-itunes
