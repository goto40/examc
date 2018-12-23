pip install pyinstaller
export PYTHONPATH=.
pyinstaller --onefile examc/console.py -n examc
find dist/examc
echo "copy the exe to your favorite path"
echo "cp dist/examc ~/Documents/tools"
