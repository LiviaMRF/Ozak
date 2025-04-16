echo "">classes.txt
grep -r "class "  --binary-files='without-match' -l | xargs cat >> classes.txt
