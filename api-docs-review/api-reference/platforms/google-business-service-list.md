> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Google Business Service list

> Read and update the structured list of services for eligible Google Business Profile locations.

The **service list** is a structured set of services with optional pricing that appears on eligible profiles (Google enables this per **category** and account capabilities). If the location cannot use service lists, the API returns a clear client error instead of empty data.

Not every business category supports service list editing, and allowed service object shapes can vary by location setup.

**Base path:** `/api/v1/misc/google-business`

***

## Get service list

**Endpoint:** `GET /api/v1/misc/google-business/location/service-list`

| Query | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team with connected Google Business location. |

Response follows Google's shape: typically `name` for the resource and `serviceItems` as an array of service objects (structure depends on Google's API version).

***

## Update service list

**Endpoint:** `PATCH /api/v1/misc/google-business/location/service-list`

| Field | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team identifier. |
| `fields` | Yes | Must include `serviceItems` in the **update payload** (this is the only allowed value today). Same comma or repeated list style as elsewhere. |
| `serviceItems` | Optional | Array of service objects. Use the same structure Google returns from GET, with fields you want to set or replace per Google's rules. |

The location must allow edits to the service list (`canModifyServiceList` in Google's metadata). Otherwise you receive a validation error explaining that the feature is not available for that location.

Best practice: read the current list first and patch from those objects instead of constructing service items from scratch.

If your UI allows service editing, fetch `metadata` from `GET /location` and gate editing by `metadata.canModifyServiceList`.

### Example

The exact shape of `serviceItems` depends on Google's API. The most reliable approach is to **GET** the current list, edit objects in your application, then **PATCH** the array back.

```json theme={null}
{
  "teamId": "00000000-0000-4000-8000-000000000001",
  "fields": ["serviceItems"],
  "serviceItems": [
    {
      "freeFormServiceItem": {
        "category": "categories/gcid:example_category",
        "label": {
          "displayName": "Standard consultation",
          "description": "Initial appointment"
        }
      }
    }
  ]
}
```

<Note>
  Category and service identifiers must be valid for your business type. Prefer copying working objects from **GET** and changing only the fields you need.
</Note>

***

## Related

* [Food menus](/api-reference/platforms/google-business-food-menus) for restaurant menu content.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.