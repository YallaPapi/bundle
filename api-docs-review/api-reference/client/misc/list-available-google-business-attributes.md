> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# List available Google Business attributes

> List the attributes Google allows for your location's category and country. Check this before updating attributes, since the valid set differs per business category. `regionCode`/`languageCode` are honoured by looking the attributes up through the location's primary category; when that category or a region code cannot be resolved (common for service-area businesses with no storefront address) the location's own defaults are returned instead and `lookup.by` comes back as `location`, meaning those two parameters were not applied.



## OpenAPI

````yaml https://api.bundle.social/swagger-json get /api/v1/misc/google-business/location/attributes/available
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
  /api/v1/misc/google-business/location/attributes/available:
    get:
      tags:
        - misc
      summary: List available Google Business attributes
      description: >-
        List the attributes Google allows for your location's category and
        country. Check this before updating attributes, since the valid set
        differs per business category. `regionCode`/`languageCode` are honoured
        by looking the attributes up through the location's primary category;
        when that category or a region code cannot be resolved (common for
        service-area businesses with no storefront address) the location's own
        defaults are returned instead and `lookup.by` comes back as `location`,
        meaning those two parameters were not applied.
      operationId: misc.google_business.listAvailableAttributes
      parameters:
        - name: teamId
          in: query
          required: true
          schema:
            type: string
        - name: languageCode
          in: query
          schema:
            type: string
        - name: regionCode
          in: query
          schema:
            type: string
            pattern: ^[A-Za-z]{2}$
        - name: pageSize
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 200
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
                  attributes:
                    default: []
                    type: array
                    items:
                      type: object
                      properties: {}
                      additionalProperties: true
                  nextPageToken:
                    type: string
                  lookup:
                    type: object
                    properties:
                      by:
                        type: string
                        enum:
                          - category
                          - location
                        description: >-
                          How the list was resolved. `category` means your
                          `regionCode`/`languageCode` were applied; `location`
                          means they could not be (the location has no primary
                          category or no region code, which is common for
                          service-area businesses) and the attributes are the
                          location's defaults instead.
                      categoryName:
                        type: string
                      regionCode:
                        type: string
                      languageCode:
                        type: string
                    required:
                      - by
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