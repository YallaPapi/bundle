> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Google Business Profile media

> List and delete photos or videos on the Google Business Profile, and add media via uploadId.

These endpoints manage **media items** attached to the selected Business Profile location (photos and some videos). They complement post images: profile media appears in the **Photos** area of the profile, not only inside a single post.

Media capabilities are partially category/profile dependent. Some categories or media types may be limited by Google policy, moderation, or profile eligibility.

**Base path:** `/api/v1/misc/google-business`

***

## List media

**Endpoint:** `GET /api/v1/misc/google-business/media`

| Query | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team identifier. |
| `pageSize` | No | 1 to 250. |
| `pageToken` | No | Pagination. |

Response includes `mediaItems` (each may have `name`, `googleUrl`, `mediaFormat` `PHOTO` or `VIDEO`, `thumbnailUrl`, `description`, `locationAssociation` with optional `category`, and so on), plus optional `nextPageToken` and `totalMediaItemCount`.

***

## Delete media

**Endpoint:** `DELETE /api/v1/misc/google-business/media`

```json theme={null}
{
  "teamId": "team_123",
  "mediaName": "accounts/123/locations/456/media/789"
}
```

`mediaName` is the **full resource name** returned by Google for that media item.

***

## Add media (upload)

**Endpoint:** `POST /api/v1/misc/google-business/media`

Use after you uploaded a file through the standard [upload](/api-reference/upload-content) flow and obtained an `uploadId`.

| Field | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team identifier. |
| `uploadId` | Yes | From your completed upload. |
| `category` | No | One of: `CATEGORY_UNSPECIFIED`, `COVER`, `PROFILE`, `LOGO`, `EXTERIOR`, `INTERIOR`, `PRODUCT`, `AT_WORK`, `FOOD_AND_DRINK`, `MENU`, `COMMON_AREA`, `ROOMS`, `TEAMS`, `ADDITIONAL` (default behavior may treat unspecified as `ADDITIONAL`). |
| `description` | No | Max 2000 characters. |

Some `category` values may be less relevant or not applied consistently for specific business categories. If unsure, list current media first and mirror categories already used by Google on that location.

### Example

```json theme={null}
{
  "teamId": "team_123",
  "uploadId": "upload_abc123",
  "category": "EXTERIOR",
  "description": "Storefront at night"
}
```

***

## Related

* [Google Business main guide](/api-reference/platforms/google-business) for **post** images and post limits.
* [Connect social accounts](/api-reference/connect-social-accounts) if the account is not connected yet.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.