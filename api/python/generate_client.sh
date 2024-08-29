# Download YAML file and store as openapi.yaml
curl -o openapi.yaml https://consumer-api.airthings.com/openapi.yaml

# Iterate over response codes and replace them in the YAML file
response_codes=(200 429)
for response_code in "${response_codes[@]}"
do
    # Replace all response codes with 'response_code' (single quotes included) to avoid issues with Python
    sed -i "" "s/$response_code/'$response_code'/g" openapi.yaml
done

# Create directory airthings_api_client if it doesn't exist
mkdir -p airthings_api_client
cd ..
# Generate Python client
openapi-python-client update --path python/openapi.yaml --config python/config.yaml
cd python