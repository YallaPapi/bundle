> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Google Business Food menus

> Read and update food menus for restaurant-class Google Business Profile locations.

**Food menus** apply to many restaurant and food categories. Google may disable the feature for a given location. In that case GET and PATCH return an error explaining that food menus are not available.

Availability and accepted menu structure can differ by category, region, and profile eligibility.

**Base path:** `/api/v1/misc/google-business`

***

## Get food menus

**Endpoint:** `GET /api/v1/misc/google-business/location/food-menus`

| Query | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team identifier. |
| `fields` | No | Subset to return: `name`, `menus`. If omitted, both are requested. Comma-separated or repeated param style. |

***

## Update food menus

**Endpoint:** `PATCH /api/v1/misc/google-business/location/food-menus`

| Field | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team identifier. |
| `fields` | Yes | Must include `menus` in the **update payload**. |
| `menus` | Optional | Array of menu objects (sections, items, prices) as defined by Google's food menu schema. |

The location should have food menus enabled (`canHaveFoodMenus`). Otherwise the API responds with an error.

Best practice: fetch current menus first and edit from returned objects, because some nested fields can be accepted/rejected depending on the location's Google configuration.

If your UI allows menu editing, fetch `metadata` from `GET /location` and gate editing by `metadata.canHaveFoodMenus`.

### Example (minimal structure)

Menus are hierarchical (menu, sections, items). Field names must match Google's API.

```json theme={null}
{
  "teamId": "00000000-0000-4000-8000-000000000001",
  "fields": ["menus"],
  "menus": [
    {
      "labels": [
        {
          "displayName": "Main menu",
          "languageCode": "en"
        }
      ],
      "sections": [
        {
          "labels": [{ "displayName": "Starters", "languageCode": "en" }],
          "items": [
            {
              "attributes": {
                "price": { "currencyCode": "USD", "units": "8" }
              },
              "labels": [{ "displayName": "Soup of the day", "languageCode": "en" }]
            }
          ]
        }
      ]
    }
  ]
}
```

Treat Google's returned objects from **GET** as the source of truth for nesting and optional fields, then adjust for your PATCH.

***

## Related

* [Service list](/api-reference/platforms/google-business-service-list) for non-menu structured services.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.