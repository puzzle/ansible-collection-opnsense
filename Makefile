COLLECTION_PATH=~/ansible_collections:~/.ansible/collections:/usr/share/ansible/collections

build-doc:
	rm -rf dest && mkdir --mode 0700 dest && \
	ANSIBLE_COLLECTIONS_PATHS=${COLLECTION_PATH} antsibull-docs sphinx-init --use-current --dest-dir dest puzzle.opnsense > /dev/null && \
	cd dest && \
	pip install -r requirements.txt >/dev/null && ANSIBLE_COLLECTIONS_PATHS=${COLLECTION_PATH} ./build.sh; \
	echo "\n\nTo view the built doc page visit file://$$PWD/build/html/index.html in a browser of your choice\n\n"
