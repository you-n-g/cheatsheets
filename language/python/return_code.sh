
python -c "raise Exception('test')"
echo $?


python << "PY" > /dev/null
while True:
  try:
    raise Exception('test')
  except:
    break
PY
echo $?

python << "PY" > /dev/null
while True:
  try:
    raise ValueError('test')
  except:
    raise
PY
echo $?
