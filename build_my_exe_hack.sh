pip install pyinstaller || exit 1
#python setup.py install || exit 1
export PYTHONPATH=.
pyinstaller --onefile examc/console.py --add-data 'examc/Exercise.tx:examc' --add-data 'examc/Config.tx:examc' --add-data 'examc/Exam.tx:examc' --add-data 'examc/master.tex.template:examc' -n examc || exit 1
find dist/examc || exit 1
echo "copy the exe to your favorite path"
echo "cp dist/examc ~/Documents/tools"

