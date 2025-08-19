rm -rf logs_threshold0/*targets.log
python3 run.py -b --fake -c bt cg ep ft is lu mg sp ua -m detect --threshold ${THRESHOLD} --logdir logs_threshold0
python3 run.py -b --fake -c suite -m detect --threshold ${THRESHOLD} --logdir logs_threshold0
python3 run.py -c suite -m detect --threshold ${THRESHOLD} --logdir logs_threshold0
