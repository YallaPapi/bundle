> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Quote a metered X action

> Estimate the credit cost of a metered X action (post publishing, analytics reads, imports) before running it, and see whether your current balance covers it.



## OpenAPI

````yaml https://api.bundle.social/swagger-json post /api/v1/billing/billable-usage/quote
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
  /api/v1/billing/billable-usage/quote:
    post:
      tags:
        - credit
      summary: Quote a metered X action
      description: >-
        Estimate the credit cost of a metered X action (post publishing,
        analytics reads, imports) before running it, and see whether your
        current balance covers it.
      operationId: credit.quoteBillableUsage
      parameters: []
      requestBody:
        description: Body
        content:
          application/json:
            schema:
              type: object
              properties:
                teamId:
                  type: string
                  minLength: 1
                text:
                  default: ''
                  type: string
                texts:
                  type: array
                  items:
                    type: string
                action:
                  type: string
                  enum:
                    - TWITTER_CONTENT_CREATE
                    - TWITTER_CONTENT_CREATE_WITH_URL
                    - TWITTER_CONTENT_MANAGE
                    - TWITTER_INTERACTION_DELETE
                    - TWITTER_POST_READ
                    - TWITTER_USER_READ
                    - TWITTER_USER_INTERACTION_CREATE
                altTextCount:
                  type: integer
                  minimum: 0
                quantity:
                  default: 1
                  type: integer
                  minimum: 1
              required:
                - teamId
      responses:
        '200':
          description: '200'
          content:
            application/json:
              schema:
                type: object
                properties:
                  billable:
                    type: boolean
                  lines:
                    type: array
                    items:
                      type: object
                      properties:
                        action:
                          type: string
                          enum:
                            - TWITTER_CONTENT_CREATE
                            - TWITTER_CONTENT_CREATE_WITH_URL
                            - TWITTER_CONTENT_MANAGE
                            - TWITTER_INTERACTION_DELETE
                            - TWITTER_POST_READ
                            - TWITTER_USER_READ
                            - TWITTER_USER_INTERACTION_CREATE
                        label:
                          type: string
                        unitAmountMicros:
                          type: integer
                        amountMicros:
                          type: integer
                        amountCents:
                          type: integer
                        currency:
                          type: string
                          enum:
                            - usd
                      required:
                        - action
                        - label
                        - unitAmountMicros
                        - amountMicros
                        - amountCents
                        - currency
                  totalMicros:
                    type: integer
                  totalCents:
                    type: integer
                  currency:
                    type: string
                    enum:
                      - usd
                  availableMicros:
                    type: integer
                  availableCents:
                    type: integer
                  wouldExceedBalance:
                    type: boolean
                required:
                  - billable
                  - lines
                  - totalMicros
                  - totalCents
                  - currency
                  - availableMicros
                  - availableCents
                  - wouldExceedBalance
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