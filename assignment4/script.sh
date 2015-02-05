wc -l permits.csv
grep -i "Hyde Park" permits.csv > permits_hydepark.csv

#part 2
git add permits_hydepark.csv
git commit -m "adding permits_hydepark"
