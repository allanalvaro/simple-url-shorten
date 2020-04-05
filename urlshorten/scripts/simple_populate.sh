a=0
while true;
do
  ((a=a+1))
  URL="https://allan.com/${a}"
  curl 'http://localhost:5000/shorten' --data "url_to_shorten=${URL}"
done
