pip install pyinstaller
python setup.py install
pyinstaller --onefile examc/console.py --add-data 'examc/Exercise.tx:examc' --add-data 'examc/Config.tx:examc' --add-data 'examc/Exam.tx:examc' --add-data 'examc/master.tex.template:examc' -n examc
find dist/examc
echo "copy the exe to your favorite path"
echo "cp dist/examc ~/Documents/tools"

