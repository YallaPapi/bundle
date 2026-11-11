> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Google Business Place action links

> List, create, update, and delete action links such as ordering, reservations, or appointments on the profile.

**Place action links** are URLs shown on the profile for actions like **order online**, **book**, or **reserve**. Google validates URLs and types. Use list to read existing links and obtain resource **names** for update or delete.

**Base path:** `/api/v1/misc/google-business`

***

## Google `PlaceActionLink` resource fields

| Field | Type | Notes |
| :- | :- | :- |
| `name` | `string` | Resource name in format `locations/{locationId}/placeActionLinks/{place_action_link_id}`. Ignored on create, used on patch/delete. |
| `providerType` | `enum` | Output-only. Provider type (`MERCHANT`, `AGGREGATOR_3P`, `PROVIDER_TYPE_UNSPECIFIED`). |
| `isEditable` | `boolean` | Output-only. Whether the link can be edited by the client. |
| `uri` | `string` | Required by Google for create. Link URL. |
| `placeActionType` | `enum` | Required by Google for create. Action type represented by the link. |
| `isPreferred` | `boolean` | Optional. Only one preferred link per `placeActionType` for a location. |
| `createTime` | `string` | Output-only RFC3339 timestamp. |
| `updateTime` | `string` | Output-only RFC3339 timestamp. |

***

## `placeActionType` values

| Value | Typical use |
| :- | :- |
| `APPOINTMENT` | Generic appointment booking. |
| `ONLINE_APPOINTMENT` | Online appointment booking. |
| `DINING_RESERVATION` | Table reservations. |
| `FOOD_ORDERING` | Order food. |
| `FOOD_DELIVERY` | Delivery. |
| `FOOD_TAKEOUT` | Takeout. |
| `SHOP_ONLINE` | E-commerce or online shopping. |

### `providerType` values (output-only)

| Value | Meaning |
| :- | :- |
| `PROVIDER_TYPE_UNSPECIFIED` | Unspecified provider type. |
| `MERCHANT` | Merchant-owned link (or agency acting for the merchant). |
| `AGGREGATOR_3P` | Third-party aggregator integration. |

### How availability is determined in Google

Google also provides place action type metadata at the API level (for example with location or region filters and optional language localization). In practice, allowed values can differ by business category and location setup.

For reliable behavior:

1. Read current links for the selected location.
2. Update only action types that are already accepted or explicitly available for that location context.

***

## List links

**Endpoint:** `GET /api/v1/misc/google-business/location/place-action-links`

| Query | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team identifier. |
| `pageSize` | No | 1 to 100. |
| `pageToken` | No | Pagination. |

Response: `placeActionLinks` array and optional `nextPageToken`. Each link may include `name`, `uri`, `placeActionType`, `isPreferred`, and output-only Google metadata such as `providerType`, `isEditable`, `createTime`, `updateTime`.

***

## Create link

**Endpoint:** `POST /api/v1/misc/google-business/location/place-action-links`

### Body

| Field | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team identifier. |
| `placeActionLink` | Yes | Nested object sent to Google. Should include at least `uri` and `placeActionType` for create. |

### Example (nested-only payload)

```json theme={null}
{
  "teamId": "team_123",
  "placeActionLink": {
    "uri": "https://example.com/order",
    "placeActionType": "FOOD_ORDERING",
    "isPreferred": true
  }
}
```

***

## Update link

**Endpoint:** `PATCH /api/v1/misc/google-business/location/place-action-links`

| Field | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team identifier. |
| `name` | Yes | Full resource name from Google, for example `locations/{locationId}/placeActionLinks/{id}`. Must belong to the selected authorized location. |
| `fields` | Yes | Subset of updated fields: `uri`, `placeActionType`, `isPreferred` (one or more). |
| `placeActionLink` | Yes | Nested object with updated values. Include keys matching `fields`. |

### Example

```json theme={null}
{
  "teamId": "team_123",
  "name": "locations/12345678901234567890/placeActionLinks/abcdef",
  "fields": ["uri", "isPreferred"],
  "placeActionLink": {
    "uri": "https://example.com/new-order",
    "isPreferred": true
  }
}
```

***

## Delete link

**Endpoint:** `DELETE /api/v1/misc/google-business/location/place-action-links`

```json theme={null}
{
  "teamId": "team_123",
  "name": "locations/12345678901234567890/placeActionLinks/abcdef"
}
```

`name` must be the full Google resource name including `/placeActionLinks/` and must belong to the selected authorized location.

***

## Availability caveats

Google may restrict place action links and action types based on business category, location, region, and profile eligibility.

* Some `placeActionType` values may be rejected for specific business categories.
* Features can vary between locations on the same account.
* Recommended flow: call **list** first, then create/update using supported values for that location.

***

## Related

* [Profile media](/api-reference/platforms/google-business-profile-media) for listing photos and videos on the profile.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.