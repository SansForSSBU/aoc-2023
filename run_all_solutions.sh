start=$SECONDS
puzzle=1
while [ -d puzzle$puzzle ]
do
    echo PUZZLE: $puzzle
    python3 puzzle$puzzle/solution.py
    echo ""
    puzzle=$((puzzle+1))
done
duration=$(( SECONDS - start))
echo Took $duration seconds