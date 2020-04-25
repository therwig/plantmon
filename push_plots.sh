# stage plots
cp plots/6hr_mois.png  html/
cp plots/6hr_temp.png  html/
cp plots/24hr_mois.png html/
cp plots/24hr_temp.png html/
cp plots/3day_mois.png html/
cp plots/3day_temp.png html/
cp plots/1wk_mois.png  html/
cp plots/1wk_temp.png  html/
cp plots/1mo_mois.png  html/
cp plots/1mo_temp.png  html/

# edit time info
cp util/index_template.html  html/index.html
sed -i "s/TEMPLATE1/`cat plots/6hr.txt`/g" html/index.html
sed -i "s/TEMPLATE2/`cat plots/24hr.txt`/g" html/index.html
sed -i "s/TEMPLATE3/`cat plots/3day.txt`/g" html/index.html
sed -i "s/TEMPLATE4/`cat plots/1wk.txt`/g" html/index.html
sed -i "s/TEMPLATE5/`cat plots/1mo.txt`/g" html/index.html
sed -i "s/TIMESTAMP/`date`/g" html/index.html
sudo cp html/* /var/www/html/
