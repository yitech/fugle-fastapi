#!/bin/bash

# Define output folder
OUTPUT_DIR="fugle-go-client"

# Step 1: Create or empty the "fugle-go-client" directory
if [ -d "$OUTPUT_DIR" ]; then
    rm -rf "${OUTPUT_DIR:?}/"*
else
    mkdir "$OUTPUT_DIR"
fi

# Step 2: Generate initial client library from the local OpenAPI server
openapi-generator-cli generate -i http://localhost:8000/openapi.json -g go -o "./$OUTPUT_DIR"

# Step 3: Modify APCode in the generated OpenAPI file using yq (./fugle-go-client/api/openapi.yaml)
yq eval '
    .components.schemas.APCode |= . + { "x-enum-varnames": ["Common", "AfterMarket", "Odd", "Emg", "IntradayOdd"] } |
    .components.schemas.Action |= . + { "x-enum-varnames": ["Buy", "Sell"] } |
    .components.schemas.Trade |= . + { "x-enum-varnames": ["Cash", "Margin", "Short", "DayTradingSell"] } |
    .components.schemas.PriceFlag |= . + { "x-enum-varnames": ["Limit", "Flat", "LimitDown", "LimitUp", "Market"] } |
    .components.schemas.BSFlag |= . + { "x-enum-varnames": ["FOK", "IOC", "ROD"] }
' -i "$OUTPUT_DIR/api/openapi.yaml"


# Step 4: Regenerate the client code based on the modified openapi.yaml file
openapi-generator-cli generate \
    -i "./$OUTPUT_DIR/api/openapi.yaml" \
    -g go \
    -o "./$OUTPUT_DIR" \
    --package-name fuglego \
    --git-host github.com \
    --git-user-id yitech \
    --git-repo-id fugle-go

cd "$OUTPUT_DIR" && chmod +x ./git_push.sh && /bin/sh ./git_push.sh yitech fugle-go "minor update" "github.com"

echo "Client code has been successfully generated and modified in ./$OUTPUT_DIR"
