#! /bin/bash
count=0

for file in $(ls *.py *.sql static/js/*.js); do
   if [[ ! -d $file ]]; then
      count=$((count + $(wc -l < $file)))
   fi
done

echo "Lines: $count"
