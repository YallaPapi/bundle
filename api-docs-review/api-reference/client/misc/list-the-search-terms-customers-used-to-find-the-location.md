> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# List the search terms customers used to find the location

> Monthly search keyword impressions for your selected location. `startMonth`/`endMonth` are inclusive `YYYY-MM` values; counts are aggregated across the whole range, so request a single month for a per-month figure. Each keyword returns either an exact `value` or a `threshold`, meaning the real count is below that number: low-volume keywords are only ever reported as a threshold, so treat a null `value` as suppressed rather than zero. Counts are unique users, not raw impressions. Paginated with `pageToken`/`nextPageToken`, max `pageSize` 100.



## OpenAPI

````yaml https://api.bundle.social/swagger-json get /api/v1/misc/google-business/location/search-keywords
openapi: 3.0.2
info:
  title: bundle.social API
  description: >-
    REST API for social media management. Perfect for AI assistants, GPTs,
    automation tools, and integrations. Post to 14+ platforms including Twitter,
    Instagram, Facebook, LinkedIn, TikTok, Pinterest, Reddit, Discord, Slack,
    YouTube, Mastodon, Bluesky, Threads, and Google Business. Schedule posts,
    manage content, analyze performance, and automate your social media workflow
    across all platforms.
  version: 1.0.0
  contact:
    email: contact@bundle.social
  termsOfService: https://bundle.social/terms
servers:
  - url: https://api.bundle.social
  - url: http://localhost:3001
security:
  - ApiKeyAuth: []
tags:
  - name: app
  - name: organization
  - name: team
  - name: socialAccount
  - name: upload
  - name: post
  - name: postImport
  - name: analytics
  - name: comment
  - name: conversation
    description: >-
      Read and reply to Instagram and Facebook direct message conversations,
      react to messages, and send private replies to comments.
  - name: automation
    description: >-
      Build, publish and monitor automation flows that react to incoming
      messages and comments, plus the per-account provider settings they rely
      on.
  - name: misc
  - name: postCSV
paths:
  /api/v1/misc/google-business/location/search-keywords:
    get:
      tags:
        - misc
      summary: List the search terms customers used to find the location
      description: >-
        Monthly search keyword impressions for your selected location.
        `startMonth`/`endMonth` are inclusive `YYYY-MM` values; counts are
        aggregated across the whole range, so request a single month for a
        per-month figure. Each keyword returns either an exact `value` or a
        `threshold`, meaning the real count is below that number: low-volume
        keywords are only ever reported as a threshold, so treat a null `value`
        as suppressed rather than zero. Counts are unique users, not raw
        impressions. Paginated with `pageToken`/`nextPageToken`, max `pageSize`
        100.
      operationId: misc.google_business.listSearchKeywords
      parameters:
        - name: teamId
          in: query
          required: true
          schema:
            type: string
        - name: startMonth
          in: query
          description: Month in `YYYY-MM` format, inclusive.
          required: true
          schema:
            type: string
            pattern: ^\d{4}-(0[1-9]|1[0-2])$
        - name: endMonth
          in: query
          description: Month in `YYYY-MM` format, inclusive.
          required: true
          schema:
            type: string
            pattern: ^\d{4}-(0[1-9]|1[0-2])$
        - name: pageSize
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
        - name: pageToken
          in: query
          schema:
            type: string
      responses:
        '200':
          description: '200'
          content:
            application/json:
              schema:
                type: object
                properties:
                  location:
                    type: string
                    description: >-
                      The Google Business location the keywords belong to, as
                      `locations/{locationId}`.
                  range:
                    type: object
                    properties:
                      startMonth:
                        type: string
                        pattern: ^\d{4}-(0[1-9]|1[0-2])$
                        description: Month in `YYYY-MM` format, inclusive.
                      endMonth:
                        type: string
                        pattern: ^\d{4}-(0[1-9]|1[0-2])$
                        description: Month in `YYYY-MM` format, inclusive.
                    required:
                      - startMonth
                      - endMonth
                  searchKeywords:
                    default: []
                    type: array
                    items:
                      type: object
                      properties:
                        searchKeyword:
                          type: string
                          description: >-
                            The lowercase query a customer typed to find the
                            business.
                        value:
                          type: number
                          nullable: true
                          description: >-
                            Exact number of unique users, when Google discloses
                            it. Null when `threshold` is returned instead.
                        threshold:
                          type: number
                          nullable: true
                          description: >-
                            Returned for low-volume keywords instead of `value`:
                            the real count is below this number. Ignoring it
                            drops the long tail.
                      required:
                        - searchKeyword
                      additionalProperties: true
                  nextPageToken:
                    type: string
                required:
                  - location
                  - range
                additionalProperties: true
        '400':
          description: '400'
          content:
            application/json:
              schema:
                type: object
                properties:
                  statusCode:
                    type: number
                    nullable: true
                  message:
                    type: string
                  issues:
                    type: array
                    items:
                      type: object
                      properties:
                        code:
                          type: string
                          enum:
                            - invalid_type
                            - invalid_literal
                            - custom
                            - invalid_union
                            - invalid_union_discriminator
                            - invalid_enum_value
                            - unrecognized_keys
                            - invalid_arguments
                            - invalid_return_type
                            - invalid_date
                            - invalid_string
                            - too_small
                            - too_big
                            - invalid_intersection_types
                            - not_multiple_of
                            - not_finite
                          nullable: true
                        message:
                          type: string
                        path:
                          type: array
                          items:
                            oneOf:
                              - type: string
                              - type: number
                          nullable: true
                      required:
                        - message
                    nullable: true
                required:
                  - message
        '401':
          description: '401'
          content:
            application/json:
              schema:
                type: object
                properties:
                  statusCode:
                    type: number
                    nullable: true
                  message:
                    type: string
                required:
                  - message
        '403':
          description: '403'
          content:
            application/json:
              schema:
                type: object
                properties:
                  statusCode:
                    type: number
                    nullable: true
                  message:
                    type: string
                required:
                  - message
        '404':
          description: '404'
          content:
            application/json:
              schema:
                type: object
                properties:
                  statusCode:
                    type: number
                    nullable: true
                  message:
                    type: string
                required:
                  - message
        '429':
          description: '429'
          content:
            application/json:
              schema:
                type: object
                properties:
                  statusCode:
                    type: number
                    nullable: true
                  message:
                    type: string
                required:
                  - message
        '500':
          description: '500'
          content:
            application/json:
              schema:
                type: object
                properties:
                  statusCode:
                    type: number
                    nullable: true
                  message:
                    type: string
                required:
                  - message
        '502':
          description: '502'
          content:
            application/json:
              schema:
                type: object
                properties:
                  statusCode:
                    type: number
                    nullable: true
                  message:
                    type: string
                required:
                  - message
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      name: x-api-key
      in: header

````

This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.