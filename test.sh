echo 'Hello World' > /tmp/greeting.txt

if [ -f /tmp/greeting.txt ]; then
  echo 'continue'
else
  tail -f /dev/null
fi
