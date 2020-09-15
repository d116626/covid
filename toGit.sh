#!/bin/bash
echo "=====================================run codes====================================="
echo " "
cd covid19/notebooks/
python run.py
cd ../../
echo "===================================================================================="
echo " "
echo " "

echo "=====================================sample_pages====================================="
echo " "
cd sample_pages
rm -f .gitignore
find * -size +49M | cat >> .gitignore
echo "adding"
echo " "
git add .
echo "commit"
git commit -m "all"
echo " "
echo "push"
echo " "
git push origin master

echo "===================================================================================="
echo " "
echo " "

echo "=====================================covid19====================================="
echo " "
cd ../covid19
rm -f .gitignore
find * -size +49M | cat >> .gitignore
echo "adding"
echo " "
git add .
echo "commit"
echo " "
git commit -m "all"
echo " "
echo "push"
echo " "
git push origin master


echo "===================================================================================="
echo " "
echo " "

echo "=====================================raioX Vale====================================="
echo " "
cd ../raiox_vale
rm -f .gitignore
find * -size +49M | cat >> .gitignore
echo "adding"
echo " "
git add .
echo "commit"
echo " "
git commit -m "all"
echo " "
echo "push"
echo " "
git push origin master


echo "===================================================================================="
echo " "
echo " "

echo "=====================================orcamento SP====================================="
echo " "
cd ../orcamento_sp
rm -f .gitignore
find * -size +49M | cat >> .gitignore
echo "adding"
echo " "
git add .
echo "commit"
echo " "
git commit -m "all"
echo " "
echo "push"
echo " "
git push origin master


echo "===================================================================================="
echo " "
echo " "

echo "=====================================raiox_vale====================================="
echo " "
cd ../raiox_vale
rm -f .gitignore
find * -size +49M | cat >> .gitignore
echo "adding"
echo " "
git add .
echo "commit"
echo " "
git commit -m "all"
echo " "
echo "push"
echo " "
git push origin master


echo "===================================================================================="
echo " "
echo " "
echo "=====================================emendas====================================="
echo " "
cd ../emendas
rm -f .gitignore
find * -size +49M | cat >> .gitignore
echo "adding"
echo " "
git add .
echo "commit"
echo " "
git commit -m "all"
echo " "
echo "push"
echo " "
git push origin master



echo "===================================================================================="
echo " "
echo " "

echo "=====================================gabinete_sv====================================="
echo " "
cd ../gabinete_sv
rm -f .gitignore
find * -size +49M | cat >> .gitignore
echo "adding"
echo " "
git add .
echo "commit"
echo " "
git commit -m "all"
echo " "
echo "push"
echo " "
git push origin master


echo "===================================================================================="
echo " "
echo " "

echo "=====================================raiox_os====================================="
echo " "
cd ../raiox_os
rm -f .gitignore
find * -size +49M | cat >> .gitignore
echo "adding"
echo " "
git add .
echo "commit"
echo " "
git commit -m "all"
echo " "
echo "push"
echo " "
git push origin master



echo "===================================================================================="
echo " "
echo " "

echo "=====================================do_sp====================================="
echo " "
cd ../do_sp
rm -f .gitignore
find * -size +49M | cat >> .gitignore
echo "adding"
echo " "
git add .
echo "commit"
echo " "
git commit -m "all"
echo " "
echo "push"
echo " "
git push origin master


echo "===================================================================================="
echo " "
echo " "

echo "=====================================raiox_alesp====================================="
echo " "
cd ../raioX_alesp
rm -f .gitignore
find * -size +49M | cat >> .gitignore
echo "adding"
echo " "
git add .
echo "commit"
echo " "
git commit -m "all"
echo " "
echo "push"
echo " "
git push origin master



echo "===================================================================================="
echo " "
echo " "



