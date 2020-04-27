# clean staging area
rm -r html/*

# cp main index
cp util/index.html  html/

# types of plot to show
for what in main average template
do
    # make subdir and index html
    mkdir -p html/${what}/
    cp util/main_template.html  html/${what}/${what}.html

    # update templates
    sed -i "s/TEMPLATE1/`cat plots/${what}/6hr.txt`/g"  html/${what}/${what}.html
    sed -i "s/TEMPLATE2/`cat plots/${what}/24hr.txt`/g" html/${what}/${what}.html
    sed -i "s/TEMPLATE3/`cat plots/${what}/3day.txt`/g" html/${what}/${what}.html
    sed -i "s/TEMPLATE4/`cat plots/${what}/1wk.txt`/g"  html/${what}/${what}.html
    sed -i "s/TEMPLATE5/`cat plots/${what}/1mo.txt`/g"  html/${what}/${what}.html
    sed -i "s/TIMESTAMP/`date`/g" html/${what}/${what}.html
    
    # stage plots
    mkdir -p html/${what}/plots/
    for time in 6hr 24hr 3day 1wk 1mo
    do
        cp plots/main/${time}_mois.png  html/${what}/plots/
        cp plots/main/${time}_temp.png  html/${what}/plots/
    done

done

sudo cp -r html/* /var/www/html/
