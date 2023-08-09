export DJANGO_DB=default
export POSTGRE_NAME=spsither
export POSTGRE_USER=spsither
export POSTGRE_PASSWORD=<enter password here>
export POSTGRE_PORT=5432
export POSTGRE_HOST=localhost
export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/home/spsither/

label-studio start --host https://work.pecha.tools/label_studio -db postgresql