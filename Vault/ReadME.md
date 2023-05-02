In this script, we first set the Vault token and URL using environment variables. You'll need to replace the placeholders `<your Vault token>` and `<your Vault URL>` with your own values.

Next, we set the `KV_PATH` variable to the path of the KV secret engine where we want to download secrets from.

We then use the curl command to retrieve a list of all secret keys within the `KV_PATH`, using the `/v1/secret/metadata/${KV_PATH}` endpoint. We use `jq` to extract the list of keys from the JSON response.

We then loop through each secret key and download the corresponding secret value using the `/v1/secret/data/${KV_PATH}/${KEY}` endpoint. We again use jq to extract the secret data from the JSON response.

Finally, we do something with the downloaded secret value. In this example, we simply echo it to the console, but you can modify this part of the script to suit your needs.

Note that this script assumes that you have jq installed on your system, which is a command-line JSON processor that we use to extract data from the JSON responses of the Vault API calls. If you don't have jq installed, you can install it using your system's package manager or download it from the official website: https://stedolan.github.io/jq/.