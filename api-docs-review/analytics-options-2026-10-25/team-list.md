> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Get list of teams

> List the teams in your organization with pagination. Use this to discover team IDs, which are required by most publishing and analytics endpoints.



## OpenAPI

````yaml https://api.bundle.social/swagger-json get /api/v1/team/
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
  /api/v1/team/:
    get:
      tags:
        - team
      summary: Get list of teams
      description: >-
        List the teams in your organization with pagination. Use this to
        discover team IDs, which are required by most publishing and analytics
        endpoints.
      operationId: team.getList
      parameters:
        - name: offset
          in: query
          schema:
            default: 0
            type: number
            nullable: true
        - name: limit
          in: query
          schema:
            default: 10
            type: number
            nullable: true
        - name: search
          in: query
          schema:
            type: string
            nullable: true
      responses:
        '200':
          description: '200'
          content:
            application/json:
              schema:
                type: object
                properties:
                  items:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: string
                        name:
                          type: string
                        avatarUrl:
                          type: string
                          nullable: true
                        organizationId:
                          type: string
                        createdById:
                          type: string
                        createdAt:
                          type: string
                          format: date-time
                          nullable: true
                        updatedAt:
                          type: string
                          format: date-time
                          nullable: true
                        deletedAt:
                          type: string
                          format: date-time
                          nullable: true
                        organization:
                          type: object
                          properties:
                            id:
                              type: string
                            createdById:
                              type: string
                            promotionCodeId:
                              type: string
                              nullable: true
                            name:
                              type: string
                              nullable: true
                            avatarUrl:
                              type: string
                              nullable: true
                            ref:
                              type: string
                              nullable: true
                            dailyPostLimit:
                              type: object
                              properties:
                                TWITTER:
                                  type: number
                                FACEBOOK:
                                  type: number
                                INSTAGRAM:
                                  type: number
                                LINKEDIN:
                                  type: number
                                YOUTUBE:
                                  type: number
                                TIKTOK:
                                  type: number
                                THREADS:
                                  type: number
                                PINTEREST:
                                  type: number
                                REDDIT:
                                  type: number
                                DISCORD:
                                  type: number
                                SLACK:
                                  type: number
                                MASTODON:
                                  type: number
                                BLUESKY:
                                  type: number
                                GOOGLE_BUSINESS:
                                  type: number
                                SNAPCHAT:
                                  type: number
                              nullable: true
                            dailyCommentLimit:
                              type: object
                              properties:
                                TWITTER:
                                  type: number
                                FACEBOOK:
                                  type: number
                                INSTAGRAM:
                                  type: number
                                LINKEDIN:
                                  type: number
                                YOUTUBE:
                                  type: number
                                TIKTOK:
                                  type: number
                                THREADS:
                                  type: number
                                PINTEREST:
                                  type: number
                                REDDIT:
                                  type: number
                                DISCORD:
                                  type: number
                                SLACK:
                                  type: number
                                MASTODON:
                                  type: number
                                BLUESKY:
                                  type: number
                                GOOGLE_BUSINESS:
                                  type: number
                                SNAPCHAT:
                                  type: number
                              nullable: true
                            monthlyImportLimitPerAccount:
                              type: number
                              nullable: true
                            commentImportLimitPerPost:
                              type: number
                              nullable: true
                            monthlyReviewImportLimitPerAccount:
                              type: number
                              nullable: true
                            monthlyMessageLimitPerAccount:
                              type: number
                              nullable: true
                            monthlyAutomationExecutionLimitPerAccount:
                              type: number
                              nullable: true
                            apiAccess:
                              type: boolean
                            analyticsDisabled:
                              type: boolean
                            analyticsPostsDisabled:
                              type: boolean
                            uploadsCompressionEnabled:
                              type: boolean
                            analyticsInterval:
                              type: number
                              nullable: true
                            analyticsPostsInterval:
                              type: number
                              nullable: true
                            forcedAccountAnalyticsDailyLimit:
                              type: number
                              nullable: true
                            forcedPostAnalyticsDailyLimit:
                              type: number
                              nullable: true
                            showVerboseErrors:
                              type: boolean
                            disconnectCheckEnabled:
                              type: boolean
                            deleteAccountAfter:
                              type: integer
                              minimum: 0
                              maximum: 168
                            createdAt:
                              type: string
                              format: date-time
                              nullable: true
                            updatedAt:
                              type: string
                              format: date-time
                              nullable: true
                            deletedAt:
                              type: string
                              format: date-time
                              nullable: true
                            suspended:
                              type: boolean
                          required:
                            - id
                            - createdById
                            - apiAccess
                            - analyticsDisabled
                            - analyticsPostsDisabled
                            - uploadsCompressionEnabled
                            - showVerboseErrors
                            - disconnectCheckEnabled
                            - deleteAccountAfter
                            - createdAt
                            - updatedAt
                        createdBy:
                          type: object
                          properties:
                            id:
                              type: string
                            externalId:
                              type: string
                            email:
                              type: string
                            emailVerified:
                              type: string
                              format: date-time
                              nullable: true
                            firstName:
                              type: string
                              nullable: true
                            lastName:
                              type: string
                              nullable: true
                            avatarUrl:
                              type: string
                              nullable: true
                            timezone:
                              type: string
                              nullable: true
                            role:
                              type: string
                              enum:
                                - ADMIN
                                - CUSTOMER
                            createdAt:
                              type: string
                              format: date-time
                              nullable: true
                            updatedAt:
                              type: string
                              format: date-time
                              nullable: true
                            deletedAt:
                              type: string
                              format: date-time
                              nullable: true
                          required:
                            - id
                            - externalId
                            - email
                            - role
                            - createdAt
                            - updatedAt
                        bots:
                          type: array
                          items:
                            type: object
                            properties:
                              id:
                                type: string
                              name:
                                type: string
                              avatarUrl:
                                type: string
                                nullable: true
                              teamId:
                                type: string
                              createdAt:
                                type: string
                                format: date-time
                                nullable: true
                              updatedAt:
                                type: string
                                format: date-time
                                nullable: true
                              deletedAt:
                                type: string
                                format: date-time
                                nullable: true
                            required:
                              - id
                              - name
                              - teamId
                              - createdAt
                              - updatedAt
                        socialAccounts:
                          type: array
                          items:
                            type: object
                            properties:
                              id:
                                type: string
                              type:
                                type: string
                                enum:
                                  - TIKTOK
                                  - YOUTUBE
                                  - INSTAGRAM
                                  - FACEBOOK
                                  - TWITTER
                                  - THREADS
                                  - LINKEDIN
                                  - PINTEREST
                                  - REDDIT
                                  - MASTODON
                                  - DISCORD
                                  - SLACK
                                  - BLUESKY
                                  - GOOGLE_BUSINESS
                                  - SNAPCHAT
                              teamId:
                                type: string
                              username:
                                type: string
                                nullable: true
                              displayName:
                                type: string
                                nullable: true
                              bio:
                                type: string
                                nullable: true
                              avatarUrl:
                                type: string
                                nullable: true
                              externalId:
                                type: string
                                nullable: true
                              providerPageId:
                                type: string
                                nullable: true
                              userUsername:
                                type: string
                                nullable: true
                              userDisplayName:
                                type: string
                                nullable: true
                              userEmail:
                                type: string
                                nullable: true
                              userId:
                                type: string
                                nullable: true
                              channels:
                                type: array
                                items:
                                  type: object
                                  properties:
                                    id:
                                      type: string
                                    name:
                                      type: string
                                      nullable: true
                                    username:
                                      type: string
                                      nullable: true
                                    address:
                                      type: string
                                      nullable: true
                                    avatarUrl:
                                      type: string
                                      nullable: true
                                    webhook:
                                      type: object
                                      properties:
                                        id:
                                          type: string
                                          nullable: true
                                        name:
                                          type: string
                                          nullable: true
                                        avatar:
                                          type: string
                                          nullable: true
                                        url:
                                          type: string
                                          nullable: true
                                      nullable: true
                                    metadata:
                                      type: object
                                      properties:
                                        allowImages:
                                          type: boolean
                                          nullable: true
                                        allowVideos:
                                          type: boolean
                                          nullable: true
                                        allowGalleries:
                                          type: boolean
                                          nullable: true
                                        linkFlairEnabled:
                                          type: boolean
                                          nullable: true
                                        facebookPageId:
                                          type: string
                                          nullable: true
                                      nullable: true
                                  required:
                                    - id
                                nullable: true
                              mastodonServerId:
                                type: string
                                nullable: true
                              instagramConnectionMethod:
                                type: string
                                enum:
                                  - FACEBOOK
                                  - INSTAGRAM
                                nullable: true
                              twitterSubType:
                                type: string
                                enum:
                                  - none
                                  - basic
                                  - premium
                                  - premium_plus
                                nullable: true
                              isTiktokBusinessAccount:
                                type: boolean
                                nullable: true
                              disconnectedCheckTryAt:
                                type: string
                                format: date-time
                                nullable: true
                              deleteOn:
                                type: string
                                format: date-time
                                nullable: true
                              messagingStatus:
                                default: DISABLED
                                type: string
                                enum:
                                  - DISABLED
                                  - ENABLED
                                  - DISABLE_PENDING
                              messagingStatusUpdatedAt:
                                type: string
                                format: date-time
                                nullable: true
                              messagingLastError:
                                type: string
                                nullable: true
                              createdAt:
                                type: string
                                format: date-time
                                nullable: true
                              updatedAt:
                                type: string
                                format: date-time
                                nullable: true
                              deletedAt:
                                type: string
                                format: date-time
                                nullable: true
                            required:
                              - id
                              - type
                              - teamId
                              - createdAt
                              - updatedAt
                        bio:
                          type: object
                          properties:
                            id:
                              type: string
                            username:
                              type: string
                            name:
                              type: string
                              nullable: true
                            description:
                              type: string
                              nullable: true
                            avatarUrl:
                              type: string
                              nullable: true
                            socials:
                              type: object
                              additionalProperties:
                                type: string
                                format: uri
                                maxLength: 2048
                                nullable: true
                              nullable: true
                            teamId:
                              type: string
                            createdAt:
                              type: string
                              format: date-time
                              nullable: true
                            updatedAt:
                              type: string
                              format: date-time
                              nullable: true
                            items:
                              type: array
                              items:
                                type: object
                                properties:
                                  id:
                                    type: string
                                  bioId:
                                    type: string
                                  name:
                                    type: string
                                  link:
                                    type: string
                                  icon:
                                    type: string
                                    nullable: true
                                  enabled:
                                    type: boolean
                                  order:
                                    type: number
                                    nullable: true
                                  createdAt:
                                    type: string
                                    format: date-time
                                    nullable: true
                                  updatedAt:
                                    type: string
                                    format: date-time
                                    nullable: true
                                  analytics:
                                    type: array
                                    items:
                                      type: object
                                      properties:
                                        id:
                                          type: string
                                        count:
                                          type: number
                                        bioItemId:
                                          type: string
                                        deviceType:
                                          type: object
                                          additionalProperties:
                                            type: number
                                        country:
                                          type: object
                                          additionalProperties:
                                            type: number
                                        createdAt:
                                          type: string
                                          format: date-time
                                          nullable: true
                                        updatedAt:
                                          type: string
                                          format: date-time
                                          nullable: true
                                      required:
                                        - id
                                        - count
                                        - bioItemId
                                        - deviceType
                                        - country
                                        - createdAt
                                        - updatedAt
                                required:
                                  - id
                                  - bioId
                                  - name
                                  - link
                                  - enabled
                                  - createdAt
                                  - updatedAt
                                  - analytics
                          required:
                            - id
                            - username
                            - name
                            - description
                            - avatarUrl
                            - socials
                            - teamId
                            - createdAt
                            - updatedAt
                            - items
                          nullable: true
                      required:
                        - id
                        - name
                        - organizationId
                        - createdById
                        - createdAt
                        - updatedAt
                        - organization
                        - createdBy
                        - bots
                        - socialAccounts
                  total:
                    type: number
                required:
                  - items
                  - total
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