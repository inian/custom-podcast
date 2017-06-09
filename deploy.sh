mkdir -p dist
cp *.py dist/
cp -R dependencies/lib/python2.7/site-packages/* dist/
cd dist
zip -r  ../add1.zip *