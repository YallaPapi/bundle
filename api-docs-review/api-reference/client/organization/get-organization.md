> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Get organization

> Retrieve your organization's details and plan. The `teams` field is deprecated and will be removed on 2026-11-15: to discover team IDs, use the paginated GET /api/v1/team.



## OpenAPI

````yaml https://api.bundle.social/swagger-json get /api/v1/organization/
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
  /api/v1/organization/:
    get:
      tags:
        - organization
      summary: Get organization
      description: >-
        Retrieve your organization's details and plan. The `teams` field is
        deprecated and will be removed on 2026-11-15: to discover team IDs, use
        the paginated GET /api/v1/team.
      operationId: organization.getOrganization
      parameters: []
      responses:
        '200':
          description: '200'
          content:
            application/json:
              schema:
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
                  subscription:
                    type: object
                    properties:
                      id:
                        type: string
                      organizationId:
                        type: string
                      couponId:
                        type: string
                        nullable: true
                      promotionCodeId:
                        type: string
                        nullable: true
                      stripeSubscriptionId:
                        type: string
                      stripeSubscriptionItems:
                        type: array
                        items:
                          type: object
                          properties:
                            id:
                              type: string
                            price:
                              type: string
                            quantity:
                              type: number
                          required:
                            - id
                            - price
                            - quantity
                        nullable: true
                      status:
                        type: string
                        enum:
                          - trialing
                          - active
                          - canceled
                          - incomplete
                          - incomplete_expired
                          - past_due
                          - unpaid
                          - paused
                      metadata:
                        type: object
                        properties: {}
                        nullable: true
                      stripePriceId:
                        type: string
                      tier:
                        type: string
                        enum:
                          - PRO
                          - BUSINESS
                      billingInterval:
                        type: string
                        enum:
                          - MONTHLY
                          - YEARLY
                      isCustomPrice:
                        type: boolean
                      customPriceLabel:
                        type: string
                        nullable: true
                      customUnitAmount:
                        type: integer
                        nullable: true
                      customCurrency:
                        type: string
                        nullable: true
                      cancelAtPeriodEnd:
                        type: boolean
                      created:
                        type: string
                        format: date-time
                        nullable: true
                      currentPeriodStart:
                        type: string
                        format: date-time
                        nullable: true
                      currentPeriodEnd:
                        type: string
                        format: date-time
                        nullable: true
                      endedAt:
                        type: string
                        format: date-time
                        nullable: true
                      cancelAt:
                        type: string
                        format: date-time
                        nullable: true
                      canceledAt:
                        type: string
                        format: date-time
                        nullable: true
                      trialStart:
                        type: string
                        format: date-time
                        nullable: true
                      trialEnd:
                        type: string
                        format: date-time
                        nullable: true
                      maxMonthlyPosts:
                        type: number
                        nullable: true
                      maxMonthlyComments:
                        type: number
                        nullable: true
                      maxMonthlyUploads:
                        type: number
                        nullable: true
                      maxMonthlyImportedPosts:
                        type: number
                        nullable: true
                      pendingTier:
                        type: string
                        enum:
                          - PRO
                          - BUSINESS
                        nullable: true
                      pendingBillingInterval:
                        type: string
                        enum:
                          - MONTHLY
                          - YEARLY
                        nullable: true
                      pendingPriceId:
                        type: string
                        nullable: true
                      pendingEffectiveAt:
                        type: string
                        format: date-time
                        nullable: true
                      pendingScheduleId:
                        type: string
                        nullable: true
                      discountStart:
                        type: string
                        format: date-time
                        nullable: true
                      discountEnd:
                        type: string
                        format: date-time
                        nullable: true
                      createdAt:
                        type: string
                        format: date-time
                        nullable: true
                      updatedAt:
                        type: string
                        format: date-time
                        nullable: true
                      coupon:
                        type: object
                        properties:
                          id:
                            type: string
                          name:
                            type: string
                            nullable: true
                          amountOff:
                            type: number
                            nullable: true
                          percentOff:
                            type: number
                            nullable: true
                          duration:
                            type: string
                            enum:
                              - forever
                              - once
                              - repeating
                          durationInMonths:
                            type: number
                            nullable: true
                          maxRedemptions:
                            type: number
                            nullable: true
                          valid:
                            type: boolean
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
                          - duration
                          - valid
                          - createdAt
                          - updatedAt
                        nullable: true
                      promotionCode:
                        type: object
                        properties:
                          code:
                            type: string
                          coupon:
                            type: object
                            properties:
                              percentOff:
                                type: number
                              duration:
                                type: string
                                enum:
                                  - forever
                                  - once
                                  - repeating
                              durationInMonths:
                                type: number
                                nullable: true
                              valid:
                                type: boolean
                            required:
                              - percentOff
                              - duration
                              - valid
                        required:
                          - code
                          - coupon
                        nullable: true
                    required:
                      - id
                      - organizationId
                      - stripeSubscriptionId
                      - status
                      - stripePriceId
                      - tier
                      - billingInterval
                      - isCustomPrice
                      - cancelAtPeriodEnd
                      - created
                      - currentPeriodStart
                      - currentPeriodEnd
                      - createdAt
                      - updatedAt
                    nullable: true
                  promotionCode:
                    type: object
                    properties:
                      code:
                        type: string
                      coupon:
                        type: object
                        properties:
                          percentOff:
                            type: number
                          duration:
                            type: string
                            enum:
                              - forever
                              - once
                              - repeating
                          durationInMonths:
                            type: number
                            nullable: true
                          valid:
                            type: boolean
                        required:
                          - percentOff
                          - duration
                          - valid
                    required:
                      - code
                      - coupon
                    nullable: true
                  teams:
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
                      required:
                        - id
                        - name
                        - organizationId
                        - createdById
                        - createdAt
                        - updatedAt
                    description: >-
                      Deprecated: will be removed on 2026-11-15. List teams with
                      the paginated GET /api/v1/team instead.
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
                  - createdBy
                  - teams
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