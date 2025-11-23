@echo off
echo Deleting old Git history...
rd /s /q .git

echo Initializing new repository...
git init

echo Staging files...
git add .

echo Creating initial commit...
git commit -m "Initial commit after removing secrets"

echo.
echo Git history has been reset.
echo Please add your remote and push manually:
echo git remote add origin https://github.com/metechmohit/Assessment-Recommender-System.git
echo git push -u origin main --force
