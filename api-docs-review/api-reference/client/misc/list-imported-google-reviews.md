> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# List imported Google Reviews

> List the Google Reviews pulled in by an import, with paging and your remaining import capacity. Use it to build a review inbox or monitor rating trends.



## OpenAPI

````yaml https://api.bundle.social/swagger-json get /api/v1/misc/google-business/reviews
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
  /api/v1/misc/google-business/reviews:
    get:
      tags:
        - misc
      summary: List imported Google Reviews
      description: >-
        List the Google Reviews pulled in by an import, with paging and your
        remaining import capacity. Use it to build a review inbox or monitor
        rating trends.
      operationId: misc.google_business.getReviews
      parameters:
        - name: teamId
          in: query
          required: true
          schema:
            type: string
        - name: limit
          in: query
          schema:
            default: 50
            type: number
            minimum: 1
            maximum: 100
        - name: offset
          in: query
          schema:
            default: 0
            type: number
            minimum: 0
            nullable: true
      responses:
        '200':
          description: '200'
          content:
            application/json:
              schema:
                type: object
                properties:
                  reviews:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: string
                        socialAccountId:
                          type: string
                        teamId:
                          type: string
                        externalReviewId:
                          type: string
                        reviewerDisplayName:
                          type: string
                          nullable: true
                        reviewerProfilePhotoUrl:
                          type: string
                          nullable: true
                        starRating:
                          type: string
                          enum:
                            - ONE
                            - TWO
                            - THREE
                            - FOUR
                            - FIVE
                          nullable: true
                        comment:
                          type: string
                          nullable: true
                        reviewReplyComment:
                          type: string
                          nullable: true
                        reviewReplyUpdatedAt:
                          type: string
                          format: date-time
                          nullable: true
                        reviewReplyState:
                          type: string
                          enum:
                            - REVIEW_REPLY_STATE_UNSPECIFIED
                            - PENDING
                            - REJECTED
                            - APPROVED
                          nullable: true
                        reviewReplyPolicyViolation:
                          type: string
                          nullable: true
                        reviewReplyUrl:
                          type: string
                          nullable: true
                        createTime:
                          type: string
                          format: date-time
                          nullable: true
                        updateTime:
                          type: string
                          format: date-time
                          nullable: true
                        importedAt:
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
                        deletedAt:
                          type: string
                          format: date-time
                          nullable: true
                      required:
                        - id
                        - socialAccountId
                        - teamId
                        - externalReviewId
                        - createdAt
                        - updatedAt
                  total:
                    type: number
                  limit:
                    type: number
                  remainingCapacity:
                    type: number
                required:
                  - reviews
                  - total
                  - limit
                  - remainingCapacity
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