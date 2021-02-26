rm -R modelling_deployment.zip
mkdir data_modelling/my-deployment-packages
cp -r utils data_modelling/my-deployment-packages
cd data_modelling
cp database_interaction.py my-deployment-packages
cp lambda_function.py my-deployment-packages
cp connection_details.py my-deployment-packages
cd my-deployment-packages
zip -r ../../modelling_deployment.zip *
cd ../..
aws lambda update-function-code --function-name uploadProcessedData  --zip-file fileb://modelling_deployment.zip
rm -r data_modelling/my-deployment-packages