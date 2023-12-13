#!/bin/bash

function veridion_request() {
    local commercial_names="$1"
    local address_txt="$2"
    local locations_latitude="$3"
    local locations_longitude="$4"

    local url="https://data.veridion.com/match/v4/companies"

    local data=$(cat <<EOF
{
    "commercial_names": ["$commercial_names"],
    "address_txt": "$address_txt",
    "locations_latitude": "$locations_latitude",
    "locations_longitude": "$locations_longitude"
}
EOF
)

    local response=$(curl -s -X POST "$url" \
        -H "x-api-key: Lk34BnMBMFDj07xGbkQ_aNikeD4_NSKq643WxEEuQUAcjtbrVJStX9FpASw7" \
        -H "Content-type: application/json" \
        -d "$data")

    echo "$response"
}