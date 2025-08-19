rm logs/*targets.log
python3 run.py -b --fake -c bt cg ep ft is lu mg sp ua  -m detect --threshold 10
python3 run.py -b --fake -c suite -m detect --threshold 10
python3 run.py -c suite -m detect --threshold 10
