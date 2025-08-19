source env.sh
echo "[INFO] run case backprop"
cd ~/ZeroSpec/cases/backprop
bash run.sh &> /dev/null
echo "[INFO] run case QuEST"
cd ~/ZeroSpec/cases/QuEST
bash run.sh &> /dev/null
echo "[INFO] run case NPB"
cd ~/ZeroSpec/cases/NPB3.4.3/NPB3.4-OMP
bash run.sh &> /dev/null
cd ~/ZeroSpec/scripts
echo "[INFO] run analysis"
bash analysis.sh &> /dev/null
mv *.pdf ~/ZeroSpec/results
mv *.csv ~/ZeroSpec/results
