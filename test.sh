
amount=$1

echo $amount

echo $(($amount * 100))

if [[ $amount -gt 0.1 ]]; then
	echo yes
fi
