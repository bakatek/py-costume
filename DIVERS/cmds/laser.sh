gpio mode 1 out

if gpio read 1 | grep 1; then
	gpio write 1 0
else
	gpio write 1 1
fi
