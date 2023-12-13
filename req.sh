curl 'https://data.veridion.com/search/v2/companies' \
  -H "x-api-key: pXStedvXkA9pMcNK1tWvx_4DesmTsIZ47qfTa6WkqFxgrCvCqJA0mpALQ53J" \
  -H "Content-type: application/json" \
  -d '{
    "filters": {
        "and": [
            {
                "attribute": "company_location",
                "relation": "in",
                "value": [
                    {
                        "country": "$1"
                    }
                ],
                "strictness": 1
            },
            {
                "attribute": "company_products",
                "relation": "match_expression",
                "value": {
                    "match": {
                        "operator": "OR",
                        "operands": [
                            "biopharma",
                            "biopharmaceutical",
                            "biopharmaceuticals"
                        ]
                    }
                },
                "strictness": 2,
                "supplier_types": [
                    "manufacturer",
                    "distributor"
                ]
            }   
        ]
    }
}'