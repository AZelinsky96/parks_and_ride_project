rm -R acquisition_deployment.zip
ls
cp -r utils data_acquisition/my-deployment-packages
cd data_acquisition
cp acquire_data.py my-deployment-packages
cp lambda_function.py my-deployment-packages
cd my-deployment-packages
zip -r ../../acquisition_deployment.zip *
cd ../..
aws lambda update-function-code --function-name readS3File  --zip-file fileb://acquisition_deployment.zip
