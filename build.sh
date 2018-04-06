# This script will flatten the virtual packages into a top level directory, then zip all contents
# for deployment within a Lambda function

echo '--------------------------------------------'
echo 'Flattening virtualenv modules into'
echo 'top level application directory'
rm -rf ./package_zip && rm -rf ./package.zip
mkdir -p ./package_zip
echo 'Move application files into package...'
rsync -av . --exclude='venv' --exclude='package_zip' ./package_zip > /dev/null
echo 'Copy virtual environment modules into package...'
cp -r venv/lib/python3.6/site-packages/* ./package_zip

echo 'Create a zip archive of the package...'
cd ./package_zip
zip -FSr package.zip . > /dev/null
cd ..
mv package_zip/package.zip .
rm -rf ./package_zip
echo 'Clean directory'
echo '--------------------------------------------'
echo 'Complete! Upload `package.zip` to AWS Lambda'
exit