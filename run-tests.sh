#!/bin/sh
# Usage: ./run-tests.sh <language-folder>    e.g. ./run-tests.sh c
lang="$1"
runner="$lang/run.sh"
[ -x "$runner" ] || { echo "no executable $runner"; exit 2; }

pass=0; fail=0
tmp=$(mktemp); trap 'rm -f "$tmp"' EXIT

for bf in tests/*.bf; do
    name=${bf%.bf}
    input=/dev/null; [ -f "$name.in" ] && input="$name.in"

    timeout 5 "$runner" "$bf" < "$input" > "$tmp" 2>/dev/null
    status=$?

    if [ $status -eq 124 ]; then
        result="TIMEOUT"
    elif [ -f "$name.fail" ]; then          # test expects an error exit
        [ $status -ne 0 ] && result=ok || result="expected an error, got exit 0"
    elif [ $status -ne 0 ]; then
        result="exit code $status"
    elif cmp -s "$tmp" "$name.out"; then
        result=ok
    else
        result="wrong output"
    fi

    if [ "$result" = ok ]; then
        pass=$((pass + 1)); echo "PASS  $(basename "$name")"
    else
        fail=$((fail + 1)); echo "FAIL  $(basename "$name")  ($result)"
        [ "$result" = "wrong output" ] && { echo "   expected: $(od -c "$name.out" | head -2)"; echo "   got:      $(od -c "$tmp" | head -2)"; }
    fi
done

echo "$pass passed, $fail failed"
[ $fail -eq 0 ]
