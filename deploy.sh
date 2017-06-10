# copy source files
mkdir -p dist
cp *.py dist/

# install deps
cp prod-requirements.txt dist/
cd dist
pip install -r prod-requirements.txt -t .

# create lambda zip file
zip -r  ../add1.zip *

# upload lambda zip file to z3
cd ..
aws s3 cp ./add1.zip s3://custom-podcasts/code.zip

# update the lambda function using s3 URL
# assumes lambda function already there
aws lambda update-function-code --function-name add --s3-bucket custom-podcasts --s3-key code.zip