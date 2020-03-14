git checkout https://github.com/covid19cz/bt-tracing-webapp.git
cd bt-tracing-webapp

python3 -m venv env
source env/bin/activate # . env/bin/activate.fish for fish

cd src/btwa_frontend \
    && npm i \
    && npm run build \
    && cd ../..


pip install .