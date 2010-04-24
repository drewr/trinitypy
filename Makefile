LOCALDB = tcnash-local.db
PRODDB = /apps/tcnash/tcnash-prod.db
STAGEDB = /apps/tcnash-stage/tcnash-stage.db
WEBHOST = valve

default:
	@echo no target specified

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

