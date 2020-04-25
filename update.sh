cd /home/pi/workspace/monitoring/
cp /home/pi/workspace/moisture/log.txt /home/pi/workspace/monitoring/data/
python3 /home/pi/workspace/monitoring/draw.py
bash /home/pi/workspace/monitoring/push_plots.sh
