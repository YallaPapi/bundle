> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Get automation flow executions

> List the runs of a single automation flow, newest first. Use it to see which events matched and how each run ended. Paginate with `offset` (`limit` max 500, default 10) or by passing the previous response's `nextCursor` back as `cursor`; the two cannot be combined. `total` is returned on the first page only.



## OpenAPI

````yaml https://api.bundle.social/swagger-json get /api/v1/automations/{id}/executions
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
  /api/v1/automations/{id}/executions:
    get:
      tags:
        - automation
      summary: Get automation flow executions
      description: >-
        List the runs of a single automation flow, newest first. Use it to see
        which events matched and how each run ended. Paginate with `offset`
        (`limit` max 500, default 10) or by passing the previous response's
        `nextCursor` back as `cursor`; the two cannot be combined. `total` is
        returned on the first page only.
      operationId: automation.getFlowExecutions
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
        - name: teamId
          in: query
          required: true
          schema:
            type: string
        - name: flowVersionId
          in: query
          schema:
            type: string
        - name: triggerId
          in: query
          schema:
            type: string
        - name: socialAccountId
          in: query
          schema:
            type: string
        - name: platform
          in: query
          schema:
            type: string
            enum:
              - INSTAGRAM
              - FACEBOOK
              - TIKTOK
        - name: status
          in: query
          schema:
            type: string
            enum:
              - QUEUED
              - RUNNING
              - COMPLETED
              - FAILED
              - CANCELED
              - SKIPPED
        - name: conversationId
          in: query
          schema:
            type: string
        - name: fetchedCommentId
          in: query
          schema:
            type: string
        - name: offset
          in: query
          schema:
            default: 0
            type: integer
            minimum: 0
            nullable: true
        - name: limit
          in: query
          schema:
            default: 10
            type: integer
            minimum: 1
            maximum: 500
            nullable: true
        - name: cursor
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
                        teamId:
                          type: string
                        organizationId:
                          type: string
                          nullable: true
                        flowId:
                          type: string
                        flowVersionId:
                          type: string
                        triggerId:
                          type: string
                          nullable: true
                        platform:
                          type: string
                          enum:
                            - INSTAGRAM
                            - FACEBOOK
                            - TIKTOK
                        socialAccountId:
                          type: string
                        conversationId:
                          type: string
                          nullable: true
                        conversationMessageId:
                          type: string
                          nullable: true
                        fetchedCommentId:
                          type: string
                          nullable: true
                        senderExternalId:
                          type: string
                          nullable: true
                        currentStepId:
                          type: string
                          nullable: true
                        status:
                          type: string
                          enum:
                            - QUEUED
                            - RUNNING
                            - COMPLETED
                            - FAILED
                            - CANCELED
                            - SKIPPED
                        idempotencyKey:
                          type: string
                        input:
                          default: {}
                          type: object
                          properties:
                            type:
                              type: string
                              enum:
                                - COMMENT_CREATED
                                - DM_RECEIVED
                                - QUICK_REPLY_CLICKED
                                - BUTTON_CLICKED
                                - MANUAL_TEST
                              nullable: true
                            platform:
                              type: string
                              enum:
                                - INSTAGRAM
                                - FACEBOOK
                                - TIKTOK
                              nullable: true
                            socialAccountId:
                              type: string
                              nullable: true
                            postId:
                              type: string
                              nullable: true
                            conversationId:
                              type: string
                              nullable: true
                            conversationMessageId:
                              type: string
                              nullable: true
                            fetchedCommentId:
                              type: string
                              nullable: true
                            senderExternalId:
                              type: string
                              nullable: true
                            externalMessageId:
                              type: string
                              nullable: true
                            text:
                              type: string
                              nullable: true
                            payload:
                              type: string
                              nullable: true
                          additionalProperties:
                            nullable: true
                        output:
                          default: {}
                          type: object
                          properties: {}
                          additionalProperties:
                            nullable: true
                        error:
                          type: object
                          properties:
                            code:
                              type: string
                              nullable: true
                            message:
                              type: string
                              nullable: true
                            retryable:
                              type: boolean
                              nullable: true
                          additionalProperties:
                            nullable: true
                          nullable: true
                        startedAt:
                          type: string
                          format: date-time
                          nullable: true
                        completedAt:
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
                        flow:
                          type: object
                          properties:
                            id:
                              type: string
                            teamId:
                              type: string
                            organizationId:
                              type: string
                              nullable: true
                            name:
                              type: string
                            status:
                              type: string
                              enum:
                                - DRAFT
                                - ACTIVE
                                - PAUSED
                                - ARCHIVED
                            platformScope:
                              type: string
                              enum:
                                - INSTAGRAM
                                - FACEBOOK
                                - BOTH
                                - TIKTOK
                            createdByUserId:
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
                            draftVersion:
                              type: object
                              properties:
                                id:
                                  type: string
                                flowId:
                                  type: string
                                version:
                                  type: number
                                status:
                                  type: string
                                  enum:
                                    - DRAFT
                                    - PUBLISHED
                                    - RETIRED
                                definition:
                                  type: object
                                  properties:
                                    trigger:
                                      type: object
                                      properties:
                                        keywords:
                                          type: array
                                          items:
                                            type: string
                                            minLength: 1
                                            maxLength: 200
                                          maxItems: 100
                                        matchMode:
                                          default: ANY
                                          type: string
                                          enum:
                                            - ANY
                                            - ALL
                                        caseSensitive:
                                          default: false
                                          type: boolean
                                        senderExternalIds:
                                          type: array
                                          items:
                                            type: string
                                            minLength: 1
                                            maxLength: 64
                                          maxItems: 100
                                        payloads:
                                          type: array
                                          items:
                                            type: string
                                            minLength: 1
                                            maxLength: 1000
                                          maxItems: 100
                                        actionDelaySeconds:
                                          default: 0
                                          type: integer
                                          minimum: 0
                                          maximum: 86400
                                        id:
                                          type: string
                                          minLength: 1
                                          maxLength: 36
                                        type:
                                          type: string
                                          enum:
                                            - COMMENT_CREATED
                                            - DM_RECEIVED
                                            - QUICK_REPLY_CLICKED
                                            - BUTTON_CLICKED
                                            - MANUAL_TEST
                                        platform:
                                          type: string
                                          enum:
                                            - INSTAGRAM
                                            - FACEBOOK
                                            - TIKTOK
                                        socialAccountId:
                                          type: string
                                        postId:
                                          type: string
                                          nullable: true
                                      required:
                                        - type
                                        - platform
                                        - socialAccountId
                                    steps:
                                      type: array
                                      items:
                                        discriminator:
                                          propertyName: type
                                        oneOf:
                                          - type: object
                                            properties:
                                              id:
                                                type: string
                                                minLength: 1
                                                maxLength: 36
                                              type:
                                                type: string
                                                enum:
                                                  - CONDITION
                                              conditions:
                                                type: array
                                                items:
                                                  type: object
                                                  properties:
                                                    id:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 36
                                                    field:
                                                      type: string
                                                      enum:
                                                        - TEXT
                                                        - PAYLOAD
                                                        - PLATFORM
                                                        - SENDER_ID
                                                    operator:
                                                      type: string
                                                      enum:
                                                        - CONTAINS
                                                        - EQUALS
                                                        - MATCHES_ANY
                                                    value:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 1000
                                                    caseSensitive:
                                                      default: false
                                                      type: boolean
                                                  required:
                                                    - field
                                                    - operator
                                                    - value
                                                minItems: 1
                                            required:
                                              - type
                                              - conditions
                                          - type: object
                                            properties:
                                              id:
                                                type: string
                                                minLength: 1
                                                maxLength: 36
                                              type:
                                                type: string
                                                enum:
                                                  - SEND_MESSAGE
                                              message:
                                                type: object
                                                properties:
                                                  text:
                                                    type: string
                                                    maxLength: 1000
                                                  attachments:
                                                    type: array
                                                    items:
                                                      type: object
                                                      properties:
                                                        uploadId:
                                                          type: string
                                                          minLength: 1
                                                        type:
                                                          type: string
                                                          enum:
                                                            - IMAGE
                                                            - VIDEO
                                                            - AUDIO
                                                            - FILE
                                                      required:
                                                        - uploadId
                                                        - type
                                                    maxItems: 10
                                                  quickReplies:
                                                    type: array
                                                    items:
                                                      type: object
                                                      properties:
                                                        id:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 36
                                                        label:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 20
                                                        payload:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 1000
                                                      required:
                                                        - id
                                                        - label
                                                        - payload
                                                    maxItems: 13
                                                  buttons:
                                                    type: array
                                                    items:
                                                      discriminator:
                                                        propertyName: type
                                                      oneOf:
                                                        - type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            type:
                                                              type: string
                                                              enum:
                                                                - POSTBACK
                                                            label:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 20
                                                            payload:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 1000
                                                          required:
                                                            - id
                                                            - type
                                                            - label
                                                            - payload
                                                        - type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            type:
                                                              type: string
                                                              enum:
                                                                - URL
                                                            label:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 20
                                                            url:
                                                              type: string
                                                              format: uri
                                                          required:
                                                            - id
                                                            - type
                                                            - label
                                                            - url
                                                        - type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            type:
                                                              type: string
                                                              enum:
                                                                - PHONE
                                                            label:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 20
                                                            phoneNumber:
                                                              type: string
                                                              minLength: 3
                                                              maxLength: 30
                                                          required:
                                                            - id
                                                            - type
                                                            - label
                                                            - phoneNumber
                                                    maxItems: 3
                                                  carousel:
                                                    type: object
                                                    properties:
                                                      cards:
                                                        type: array
                                                        items:
                                                          type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            title:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 80
                                                            subtitle:
                                                              type: string
                                                              maxLength: 80
                                                              nullable: true
                                                            imageUploadId:
                                                              type: string
                                                              minLength: 1
                                                              nullable: true
                                                            buttons:
                                                              type: array
                                                              items:
                                                                discriminator:
                                                                  propertyName: type
                                                                oneOf:
                                                                  - type: object
                                                                    properties:
                                                                      id: {}
                                                                      type: {}
                                                                      label: {}
                                                                      payload: {}
                                                                    required:
                                                                      - id
                                                                      - type
                                                                      - label
                                                                      - payload
                                                                  - type: object
                                                                    properties:
                                                                      id: {}
                                                                      type: {}
                                                                      label: {}
                                                                      url: {}
                                                                    required:
                                                                      - id
                                                                      - type
                                                                      - label
                                                                      - url
                                                                  - type: object
                                                                    properties:
                                                                      id: {}
                                                                      type: {}
                                                                      label: {}
                                                                      phoneNumber: {}
                                                                    required:
                                                                      - id
                                                                      - type
                                                                      - label
                                                                      - phoneNumber
                                                              maxItems: 3
                                                          required:
                                                            - id
                                                            - title
                                                        minItems: 1
                                                        maxItems: 10
                                                    required:
                                                      - cards
                                            required:
                                              - type
                                              - message
                                          - type: object
                                            properties:
                                              id:
                                                type: string
                                                minLength: 1
                                                maxLength: 36
                                              type:
                                                type: string
                                                enum:
                                                  - SEND_PRIVATE_REPLY
                                              message:
                                                type: object
                                                properties:
                                                  text:
                                                    type: string
                                                    maxLength: 1000
                                                  attachments:
                                                    type: array
                                                    items:
                                                      type: object
                                                      properties:
                                                        uploadId:
                                                          type: string
                                                          minLength: 1
                                                        type:
                                                          type: string
                                                          enum:
                                                            - IMAGE
                                                            - VIDEO
                                                            - AUDIO
                                                            - FILE
                                                      required:
                                                        - uploadId
                                                        - type
                                                    maxItems: 10
                                                  quickReplies:
                                                    type: array
                                                    items:
                                                      type: object
                                                      properties:
                                                        id:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 36
                                                        label:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 20
                                                        payload:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 1000
                                                      required:
                                                        - id
                                                        - label
                                                        - payload
                                                    maxItems: 13
                                                  buttons:
                                                    type: array
                                                    items:
                                                      discriminator:
                                                        propertyName: type
                                                      oneOf:
                                                        - type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            type:
                                                              type: string
                                                              enum:
                                                                - POSTBACK
                                                            label:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 20
                                                            payload:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 1000
                                                          required:
                                                            - id
                                                            - type
                                                            - label
                                                            - payload
                                                        - type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            type:
                                                              type: string
                                                              enum:
                                                                - URL
                                                            label:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 20
                                                            url:
                                                              type: string
                                                              format: uri
                                                          required:
                                                            - id
                                                            - type
                                                            - label
                                                            - url
                                                        - type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            type:
                                                              type: string
                                                              enum:
                                                                - PHONE
                                                            label:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 20
                                                            phoneNumber:
                                                              type: string
                                                              minLength: 3
                                                              maxLength: 30
                                                          required:
                                                            - id
                                                            - type
                                                            - label
                                                            - phoneNumber
                                                    maxItems: 3
                                                  carousel:
                                                    type: object
                                                    properties:
                                                      cards:
                                                        type: array
                                                        items:
                                                          type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            title:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 80
                                                            subtitle:
                                                              type: string
                                                              maxLength: 80
                                                              nullable: true
                                                            imageUploadId:
                                                              type: string
                                                              minLength: 1
                                                              nullable: true
                                                            buttons:
                                                              type: array
                                                              items:
                                                                discriminator:
                                                                  propertyName: type
                                                                oneOf:
                                                                  - type: object
                                                                    properties:
                                                                      id: {}
                                                                      type: {}
                                                                      label: {}
                                                                      payload: {}
                                                                    required:
                                                                      - id
                                                                      - type
                                                                      - label
                                                                      - payload
                                                                  - type: object
                                                                    properties:
                                                                      id: {}
                                                                      type: {}
                                                                      label: {}
                                                                      url: {}
                                                                    required:
                                                                      - id
                                                                      - type
                                                                      - label
                                                                      - url
                                                                  - type: object
                                                                    properties:
                                                                      id: {}
                                                                      type: {}
                                                                      label: {}
                                                                      phoneNumber: {}
                                                                    required:
                                                                      - id
                                                                      - type
                                                                      - label
                                                                      - phoneNumber
                                                              maxItems: 3
                                                          required:
                                                            - id
                                                            - title
                                                        minItems: 1
                                                        maxItems: 10
                                                    required:
                                                      - cards
                                            required:
                                              - type
                                              - message
                                          - type: object
                                            properties:
                                              id:
                                                type: string
                                                minLength: 1
                                                maxLength: 36
                                              type:
                                                type: string
                                                enum:
                                                  - SEND_PUBLIC_COMMENT_REPLY
                                              text:
                                                type: string
                                                minLength: 1
                                                maxLength: 1000
                                            required:
                                              - type
                                              - text
                                          - type: object
                                            properties:
                                              id:
                                                type: string
                                                minLength: 1
                                                maxLength: 36
                                              type:
                                                type: string
                                                enum:
                                                  - LIKE_COMMENT
                                            required:
                                              - type
                                          - type: object
                                            properties:
                                              id:
                                                type: string
                                                minLength: 1
                                                maxLength: 36
                                              type:
                                                type: string
                                                enum:
                                                  - ARCHIVE_CONVERSATION
                                            required:
                                              - type
                                          - type: object
                                            properties:
                                              id:
                                                type: string
                                                minLength: 1
                                                maxLength: 36
                                              type:
                                                type: string
                                                enum:
                                                  - OPEN_CONVERSATION
                                            required:
                                              - type
                                  required:
                                    - trigger
                                    - steps
                                publishedAt:
                                  type: string
                                  format: date-time
                                  nullable: true
                                publishedByUserId:
                                  type: string
                                  nullable: true
                                createdAt:
                                  type: string
                                  format: date-time
                                  nullable: true
                              required:
                                - id
                                - flowId
                                - version
                                - status
                                - definition
                                - createdAt
                            publishedVersion:
                              type: object
                              properties:
                                id:
                                  type: string
                                flowId:
                                  type: string
                                version:
                                  type: number
                                status:
                                  type: string
                                  enum:
                                    - DRAFT
                                    - PUBLISHED
                                    - RETIRED
                                definition:
                                  type: object
                                  properties:
                                    trigger:
                                      type: object
                                      properties:
                                        keywords:
                                          type: array
                                          items:
                                            type: string
                                            minLength: 1
                                            maxLength: 200
                                          maxItems: 100
                                        matchMode:
                                          default: ANY
                                          type: string
                                          enum:
                                            - ANY
                                            - ALL
                                        caseSensitive:
                                          default: false
                                          type: boolean
                                        senderExternalIds:
                                          type: array
                                          items:
                                            type: string
                                            minLength: 1
                                            maxLength: 64
                                          maxItems: 100
                                        payloads:
                                          type: array
                                          items:
                                            type: string
                                            minLength: 1
                                            maxLength: 1000
                                          maxItems: 100
                                        actionDelaySeconds:
                                          default: 0
                                          type: integer
                                          minimum: 0
                                          maximum: 86400
                                        id:
                                          type: string
                                          minLength: 1
                                          maxLength: 36
                                        type:
                                          type: string
                                          enum:
                                            - COMMENT_CREATED
                                            - DM_RECEIVED
                                            - QUICK_REPLY_CLICKED
                                            - BUTTON_CLICKED
                                            - MANUAL_TEST
                                        platform:
                                          type: string
                                          enum:
                                            - INSTAGRAM
                                            - FACEBOOK
                                            - TIKTOK
                                        socialAccountId:
                                          type: string
                                        postId:
                                          type: string
                                          nullable: true
                                      required:
                                        - type
                                        - platform
                                        - socialAccountId
                                    steps:
                                      type: array
                                      items:
                                        discriminator:
                                          propertyName: type
                                        oneOf:
                                          - type: object
                                            properties:
                                              id:
                                                type: string
                                                minLength: 1
                                                maxLength: 36
                                              type:
                                                type: string
                                                enum:
                                                  - CONDITION
                                              conditions:
                                                type: array
                                                items:
                                                  type: object
                                                  properties:
                                                    id:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 36
                                                    field:
                                                      type: string
                                                      enum:
                                                        - TEXT
                                                        - PAYLOAD
                                                        - PLATFORM
                                                        - SENDER_ID
                                                    operator:
                                                      type: string
                                                      enum:
                                                        - CONTAINS
                                                        - EQUALS
                                                        - MATCHES_ANY
                                                    value:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 1000
                                                    caseSensitive:
                                                      default: false
                                                      type: boolean
                                                  required:
                                                    - field
                                                    - operator
                                                    - value
                                                minItems: 1
                                            required:
                                              - type
                                              - conditions
                                          - type: object
                                            properties:
                                              id:
                                                type: string
                                                minLength: 1
                                                maxLength: 36
                                              type:
                                                type: string
                                                enum:
                                                  - SEND_MESSAGE
                                              message:
                                                type: object
                                                properties:
                                                  text:
                                                    type: string
                                                    maxLength: 1000
                                                  attachments:
                                                    type: array
                                                    items:
                                                      type: object
                                                      properties:
                                                        uploadId:
                                                          type: string
                                                          minLength: 1
                                                        type:
                                                          type: string
                                                          enum:
                                                            - IMAGE
                                                            - VIDEO
                                                            - AUDIO
                                                            - FILE
                                                      required:
                                                        - uploadId
                                                        - type
                                                    maxItems: 10
                                                  quickReplies:
                                                    type: array
                                                    items:
                                                      type: object
                                                      properties:
                                                        id:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 36
                                                        label:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 20
                                                        payload:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 1000
                                                      required:
                                                        - id
                                                        - label
                                                        - payload
                                                    maxItems: 13
                                                  buttons:
                                                    type: array
                                                    items:
                                                      discriminator:
                                                        propertyName: type
                                                      oneOf:
                                                        - type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            type:
                                                              type: string
                                                              enum:
                                                                - POSTBACK
                                                            label:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 20
                                                            payload:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 1000
                                                          required:
                                                            - id
                                                            - type
                                                            - label
                                                            - payload
                                                        - type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            type:
                                                              type: string
                                                              enum:
                                                                - URL
                                                            label:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 20
                                                            url:
                                                              type: string
                                                              format: uri
                                                          required:
                                                            - id
                                                            - type
                                                            - label
                                                            - url
                                                        - type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            type:
                                                              type: string
                                                              enum:
                                                                - PHONE
                                                            label:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 20
                                                            phoneNumber:
                                                              type: string
                                                              minLength: 3
                                                              maxLength: 30
                                                          required:
                                                            - id
                                                            - type
                                                            - label
                                                            - phoneNumber
                                                    maxItems: 3
                                                  carousel:
                                                    type: object
                                                    properties:
                                                      cards:
                                                        type: array
                                                        items:
                                                          type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            title:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 80
                                                            subtitle:
                                                              type: string
                                                              maxLength: 80
                                                              nullable: true
                                                            imageUploadId:
                                                              type: string
                                                              minLength: 1
                                                              nullable: true
                                                            buttons:
                                                              type: array
                                                              items:
                                                                discriminator:
                                                                  propertyName: type
                                                                oneOf:
                                                                  - type: object
                                                                    properties:
                                                                      id: {}
                                                                      type: {}
                                                                      label: {}
                                                                      payload: {}
                                                                    required:
                                                                      - id
                                                                      - type
                                                                      - label
                                                                      - payload
                                                                  - type: object
                                                                    properties:
                                                                      id: {}
                                                                      type: {}
                                                                      label: {}
                                                                      url: {}
                                                                    required:
                                                                      - id
                                                                      - type
                                                                      - label
                                                                      - url
                                                                  - type: object
                                                                    properties:
                                                                      id: {}
                                                                      type: {}
                                                                      label: {}
                                                                      phoneNumber: {}
                                                                    required:
                                                                      - id
                                                                      - type
                                                                      - label
                                                                      - phoneNumber
                                                              maxItems: 3
                                                          required:
                                                            - id
                                                            - title
                                                        minItems: 1
                                                        maxItems: 10
                                                    required:
                                                      - cards
                                            required:
                                              - type
                                              - message
                                          - type: object
                                            properties:
                                              id:
                                                type: string
                                                minLength: 1
                                                maxLength: 36
                                              type:
                                                type: string
                                                enum:
                                                  - SEND_PRIVATE_REPLY
                                              message:
                                                type: object
                                                properties:
                                                  text:
                                                    type: string
                                                    maxLength: 1000
                                                  attachments:
                                                    type: array
                                                    items:
                                                      type: object
                                                      properties:
                                                        uploadId:
                                                          type: string
                                                          minLength: 1
                                                        type:
                                                          type: string
                                                          enum:
                                                            - IMAGE
                                                            - VIDEO
                                                            - AUDIO
                                                            - FILE
                                                      required:
                                                        - uploadId
                                                        - type
                                                    maxItems: 10
                                                  quickReplies:
                                                    type: array
                                                    items:
                                                      type: object
                                                      properties:
                                                        id:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 36
                                                        label:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 20
                                                        payload:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 1000
                                                      required:
                                                        - id
                                                        - label
                                                        - payload
                                                    maxItems: 13
                                                  buttons:
                                                    type: array
                                                    items:
                                                      discriminator:
                                                        propertyName: type
                                                      oneOf:
                                                        - type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            type:
                                                              type: string
                                                              enum:
                                                                - POSTBACK
                                                            label:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 20
                                                            payload:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 1000
                                                          required:
                                                            - id
                                                            - type
                                                            - label
                                                            - payload
                                                        - type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            type:
                                                              type: string
                                                              enum:
                                                                - URL
                                                            label:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 20
                                                            url:
                                                              type: string
                                                              format: uri
                                                          required:
                                                            - id
                                                            - type
                                                            - label
                                                            - url
                                                        - type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            type:
                                                              type: string
                                                              enum:
                                                                - PHONE
                                                            label:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 20
                                                            phoneNumber:
                                                              type: string
                                                              minLength: 3
                                                              maxLength: 30
                                                          required:
                                                            - id
                                                            - type
                                                            - label
                                                            - phoneNumber
                                                    maxItems: 3
                                                  carousel:
                                                    type: object
                                                    properties:
                                                      cards:
                                                        type: array
                                                        items:
                                                          type: object
                                                          properties:
                                                            id:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 36
                                                            title:
                                                              type: string
                                                              minLength: 1
                                                              maxLength: 80
                                                            subtitle:
                                                              type: string
                                                              maxLength: 80
                                                              nullable: true
                                                            imageUploadId:
                                                              type: string
                                                              minLength: 1
                                                              nullable: true
                                                            buttons:
                                                              type: array
                                                              items:
                                                                discriminator:
                                                                  propertyName: type
                                                                oneOf:
                                                                  - type: object
                                                                    properties:
                                                                      id: {}
                                                                      type: {}
                                                                      label: {}
                                                                      payload: {}
                                                                    required:
                                                                      - id
                                                                      - type
                                                                      - label
                                                                      - payload
                                                                  - type: object
                                                                    properties:
                                                                      id: {}
                                                                      type: {}
                                                                      label: {}
                                                                      url: {}
                                                                    required:
                                                                      - id
                                                                      - type
                                                                      - label
                                                                      - url
                                                                  - type: object
                                                                    properties:
                                                                      id: {}
                                                                      type: {}
                                                                      label: {}
                                                                      phoneNumber: {}
                                                                    required:
                                                                      - id
                                                                      - type
                                                                      - label
                                                                      - phoneNumber
                                                              maxItems: 3
                                                          required:
                                                            - id
                                                            - title
                                                        minItems: 1
                                                        maxItems: 10
                                                    required:
                                                      - cards
                                            required:
                                              - type
                                              - message
                                          - type: object
                                            properties:
                                              id:
                                                type: string
                                                minLength: 1
                                                maxLength: 36
                                              type:
                                                type: string
                                                enum:
                                                  - SEND_PUBLIC_COMMENT_REPLY
                                              text:
                                                type: string
                                                minLength: 1
                                                maxLength: 1000
                                            required:
                                              - type
                                              - text
                                          - type: object
                                            properties:
                                              id:
                                                type: string
                                                minLength: 1
                                                maxLength: 36
                                              type:
                                                type: string
                                                enum:
                                                  - LIKE_COMMENT
                                            required:
                                              - type
                                          - type: object
                                            properties:
                                              id:
                                                type: string
                                                minLength: 1
                                                maxLength: 36
                                              type:
                                                type: string
                                                enum:
                                                  - ARCHIVE_CONVERSATION
                                            required:
                                              - type
                                          - type: object
                                            properties:
                                              id:
                                                type: string
                                                minLength: 1
                                                maxLength: 36
                                              type:
                                                type: string
                                                enum:
                                                  - OPEN_CONVERSATION
                                            required:
                                              - type
                                  required:
                                    - trigger
                                    - steps
                                publishedAt:
                                  type: string
                                  format: date-time
                                  nullable: true
                                publishedByUserId:
                                  type: string
                                  nullable: true
                                createdAt:
                                  type: string
                                  format: date-time
                                  nullable: true
                              required:
                                - id
                                - flowId
                                - version
                                - status
                                - definition
                                - createdAt
                          required:
                            - id
                            - teamId
                            - name
                            - status
                            - platformScope
                            - createdAt
                            - updatedAt
                        flowVersion:
                          type: object
                          properties:
                            id:
                              type: string
                            flowId:
                              type: string
                            version:
                              type: number
                            status:
                              type: string
                              enum:
                                - DRAFT
                                - PUBLISHED
                                - RETIRED
                            definition:
                              type: object
                              properties:
                                trigger:
                                  type: object
                                  properties:
                                    keywords:
                                      type: array
                                      items:
                                        type: string
                                        minLength: 1
                                        maxLength: 200
                                      maxItems: 100
                                    matchMode:
                                      default: ANY
                                      type: string
                                      enum:
                                        - ANY
                                        - ALL
                                    caseSensitive:
                                      default: false
                                      type: boolean
                                    senderExternalIds:
                                      type: array
                                      items:
                                        type: string
                                        minLength: 1
                                        maxLength: 64
                                      maxItems: 100
                                    payloads:
                                      type: array
                                      items:
                                        type: string
                                        minLength: 1
                                        maxLength: 1000
                                      maxItems: 100
                                    actionDelaySeconds:
                                      default: 0
                                      type: integer
                                      minimum: 0
                                      maximum: 86400
                                    id:
                                      type: string
                                      minLength: 1
                                      maxLength: 36
                                    type:
                                      type: string
                                      enum:
                                        - COMMENT_CREATED
                                        - DM_RECEIVED
                                        - QUICK_REPLY_CLICKED
                                        - BUTTON_CLICKED
                                        - MANUAL_TEST
                                    platform:
                                      type: string
                                      enum:
                                        - INSTAGRAM
                                        - FACEBOOK
                                        - TIKTOK
                                    socialAccountId:
                                      type: string
                                    postId:
                                      type: string
                                      nullable: true
                                  required:
                                    - type
                                    - platform
                                    - socialAccountId
                                steps:
                                  type: array
                                  items:
                                    discriminator:
                                      propertyName: type
                                    oneOf:
                                      - type: object
                                        properties:
                                          id:
                                            type: string
                                            minLength: 1
                                            maxLength: 36
                                          type:
                                            type: string
                                            enum:
                                              - CONDITION
                                          conditions:
                                            type: array
                                            items:
                                              type: object
                                              properties:
                                                id:
                                                  type: string
                                                  minLength: 1
                                                  maxLength: 36
                                                field:
                                                  type: string
                                                  enum:
                                                    - TEXT
                                                    - PAYLOAD
                                                    - PLATFORM
                                                    - SENDER_ID
                                                operator:
                                                  type: string
                                                  enum:
                                                    - CONTAINS
                                                    - EQUALS
                                                    - MATCHES_ANY
                                                value:
                                                  type: string
                                                  minLength: 1
                                                  maxLength: 1000
                                                caseSensitive:
                                                  default: false
                                                  type: boolean
                                              required:
                                                - field
                                                - operator
                                                - value
                                            minItems: 1
                                        required:
                                          - type
                                          - conditions
                                      - type: object
                                        properties:
                                          id:
                                            type: string
                                            minLength: 1
                                            maxLength: 36
                                          type:
                                            type: string
                                            enum:
                                              - SEND_MESSAGE
                                          message:
                                            type: object
                                            properties:
                                              text:
                                                type: string
                                                maxLength: 1000
                                              attachments:
                                                type: array
                                                items:
                                                  type: object
                                                  properties:
                                                    uploadId:
                                                      type: string
                                                      minLength: 1
                                                    type:
                                                      type: string
                                                      enum:
                                                        - IMAGE
                                                        - VIDEO
                                                        - AUDIO
                                                        - FILE
                                                  required:
                                                    - uploadId
                                                    - type
                                                maxItems: 10
                                              quickReplies:
                                                type: array
                                                items:
                                                  type: object
                                                  properties:
                                                    id:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 36
                                                    label:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 20
                                                    payload:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 1000
                                                  required:
                                                    - id
                                                    - label
                                                    - payload
                                                maxItems: 13
                                              buttons:
                                                type: array
                                                items:
                                                  discriminator:
                                                    propertyName: type
                                                  oneOf:
                                                    - type: object
                                                      properties:
                                                        id:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 36
                                                        type:
                                                          type: string
                                                          enum:
                                                            - POSTBACK
                                                        label:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 20
                                                        payload:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 1000
                                                      required:
                                                        - id
                                                        - type
                                                        - label
                                                        - payload
                                                    - type: object
                                                      properties:
                                                        id:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 36
                                                        type:
                                                          type: string
                                                          enum:
                                                            - URL
                                                        label:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 20
                                                        url:
                                                          type: string
                                                          format: uri
                                                      required:
                                                        - id
                                                        - type
                                                        - label
                                                        - url
                                                    - type: object
                                                      properties:
                                                        id:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 36
                                                        type:
                                                          type: string
                                                          enum:
                                                            - PHONE
                                                        label:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 20
                                                        phoneNumber:
                                                          type: string
                                                          minLength: 3
                                                          maxLength: 30
                                                      required:
                                                        - id
                                                        - type
                                                        - label
                                                        - phoneNumber
                                                maxItems: 3
                                              carousel:
                                                type: object
                                                properties:
                                                  cards:
                                                    type: array
                                                    items:
                                                      type: object
                                                      properties:
                                                        id:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 36
                                                        title:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 80
                                                        subtitle:
                                                          type: string
                                                          maxLength: 80
                                                          nullable: true
                                                        imageUploadId:
                                                          type: string
                                                          minLength: 1
                                                          nullable: true
                                                        buttons:
                                                          type: array
                                                          items:
                                                            discriminator:
                                                              propertyName: type
                                                            oneOf:
                                                              - type: object
                                                                properties:
                                                                  id:
                                                                    type: string
                                                                    minLength: 1
                                                                    maxLength: 36
                                                                  type:
                                                                    type: string
                                                                    enum:
                                                                      - POSTBACK
                                                                  label:
                                                                    type: string
                                                                    minLength: 1
                                                                    maxLength: 20
                                                                  payload:
                                                                    type: string
                                                                    minLength: 1
                                                                    maxLength: 1000
                                                                required:
                                                                  - id
                                                                  - type
                                                                  - label
                                                                  - payload
                                                              - type: object
                                                                properties:
                                                                  id:
                                                                    type: string
                                                                    minLength: 1
                                                                    maxLength: 36
                                                                  type:
                                                                    type: string
                                                                    enum:
                                                                      - URL
                                                                  label:
                                                                    type: string
                                                                    minLength: 1
                                                                    maxLength: 20
                                                                  url:
                                                                    type: string
                                                                    format: uri
                                                                required:
                                                                  - id
                                                                  - type
                                                                  - label
                                                                  - url
                                                              - type: object
                                                                properties:
                                                                  id:
                                                                    type: string
                                                                    minLength: 1
                                                                    maxLength: 36
                                                                  type:
                                                                    type: string
                                                                    enum:
                                                                      - PHONE
                                                                  label:
                                                                    type: string
                                                                    minLength: 1
                                                                    maxLength: 20
                                                                  phoneNumber:
                                                                    type: string
                                                                    minLength: 3
                                                                    maxLength: 30
                                                                required:
                                                                  - id
                                                                  - type
                                                                  - label
                                                                  - phoneNumber
                                                          maxItems: 3
                                                      required:
                                                        - id
                                                        - title
                                                    minItems: 1
                                                    maxItems: 10
                                                required:
                                                  - cards
                                        required:
                                          - type
                                          - message
                                      - type: object
                                        properties:
                                          id:
                                            type: string
                                            minLength: 1
                                            maxLength: 36
                                          type:
                                            type: string
                                            enum:
                                              - SEND_PRIVATE_REPLY
                                          message:
                                            type: object
                                            properties:
                                              text:
                                                type: string
                                                maxLength: 1000
                                              attachments:
                                                type: array
                                                items:
                                                  type: object
                                                  properties:
                                                    uploadId:
                                                      type: string
                                                      minLength: 1
                                                    type:
                                                      type: string
                                                      enum:
                                                        - IMAGE
                                                        - VIDEO
                                                        - AUDIO
                                                        - FILE
                                                  required:
                                                    - uploadId
                                                    - type
                                                maxItems: 10
                                              quickReplies:
                                                type: array
                                                items:
                                                  type: object
                                                  properties:
                                                    id:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 36
                                                    label:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 20
                                                    payload:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 1000
                                                  required:
                                                    - id
                                                    - label
                                                    - payload
                                                maxItems: 13
                                              buttons:
                                                type: array
                                                items:
                                                  discriminator:
                                                    propertyName: type
                                                  oneOf:
                                                    - type: object
                                                      properties:
                                                        id:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 36
                                                        type:
                                                          type: string
                                                          enum:
                                                            - POSTBACK
                                                        label:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 20
                                                        payload:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 1000
                                                      required:
                                                        - id
                                                        - type
                                                        - label
                                                        - payload
                                                    - type: object
                                                      properties:
                                                        id:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 36
                                                        type:
                                                          type: string
                                                          enum:
                                                            - URL
                                                        label:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 20
                                                        url:
                                                          type: string
                                                          format: uri
                                                      required:
                                                        - id
                                                        - type
                                                        - label
                                                        - url
                                                    - type: object
                                                      properties:
                                                        id:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 36
                                                        type:
                                                          type: string
                                                          enum:
                                                            - PHONE
                                                        label:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 20
                                                        phoneNumber:
                                                          type: string
                                                          minLength: 3
                                                          maxLength: 30
                                                      required:
                                                        - id
                                                        - type
                                                        - label
                                                        - phoneNumber
                                                maxItems: 3
                                              carousel:
                                                type: object
                                                properties:
                                                  cards:
                                                    type: array
                                                    items:
                                                      type: object
                                                      properties:
                                                        id:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 36
                                                        title:
                                                          type: string
                                                          minLength: 1
                                                          maxLength: 80
                                                        subtitle:
                                                          type: string
                                                          maxLength: 80
                                                          nullable: true
                                                        imageUploadId:
                                                          type: string
                                                          minLength: 1
                                                          nullable: true
                                                        buttons:
                                                          type: array
                                                          items:
                                                            discriminator:
                                                              propertyName: type
                                                            oneOf:
                                                              - type: object
                                                                properties:
                                                                  id:
                                                                    type: string
                                                                    minLength: 1
                                                                    maxLength: 36
                                                                  type:
                                                                    type: string
                                                                    enum:
                                                                      - POSTBACK
                                                                  label:
                                                                    type: string
                                                                    minLength: 1
                                                                    maxLength: 20
                                                                  payload:
                                                                    type: string
                                                                    minLength: 1
                                                                    maxLength: 1000
                                                                required:
                                                                  - id
                                                                  - type
                                                                  - label
                                                                  - payload
                                                              - type: object
                                                                properties:
                                                                  id:
                                                                    type: string
                                                                    minLength: 1
                                                                    maxLength: 36
                                                                  type:
                                                                    type: string
                                                                    enum:
                                                                      - URL
                                                                  label:
                                                                    type: string
                                                                    minLength: 1
                                                                    maxLength: 20
                                                                  url:
                                                                    type: string
                                                                    format: uri
                                                                required:
                                                                  - id
                                                                  - type
                                                                  - label
                                                                  - url
                                                              - type: object
                                                                properties:
                                                                  id:
                                                                    type: string
                                                                    minLength: 1
                                                                    maxLength: 36
                                                                  type:
                                                                    type: string
                                                                    enum:
                                                                      - PHONE
                                                                  label:
                                                                    type: string
                                                                    minLength: 1
                                                                    maxLength: 20
                                                                  phoneNumber:
                                                                    type: string
                                                                    minLength: 3
                                                                    maxLength: 30
                                                                required:
                                                                  - id
                                                                  - type
                                                                  - label
                                                                  - phoneNumber
                                                          maxItems: 3
                                                      required:
                                                        - id
                                                        - title
                                                    minItems: 1
                                                    maxItems: 10
                                                required:
                                                  - cards
                                        required:
                                          - type
                                          - message
                                      - type: object
                                        properties:
                                          id:
                                            type: string
                                            minLength: 1
                                            maxLength: 36
                                          type:
                                            type: string
                                            enum:
                                              - SEND_PUBLIC_COMMENT_REPLY
                                          text:
                                            type: string
                                            minLength: 1
                                            maxLength: 1000
                                        required:
                                          - type
                                          - text
                                      - type: object
                                        properties:
                                          id:
                                            type: string
                                            minLength: 1
                                            maxLength: 36
                                          type:
                                            type: string
                                            enum:
                                              - LIKE_COMMENT
                                        required:
                                          - type
                                      - type: object
                                        properties:
                                          id:
                                            type: string
                                            minLength: 1
                                            maxLength: 36
                                          type:
                                            type: string
                                            enum:
                                              - ARCHIVE_CONVERSATION
                                        required:
                                          - type
                                      - type: object
                                        properties:
                                          id:
                                            type: string
                                            minLength: 1
                                            maxLength: 36
                                          type:
                                            type: string
                                            enum:
                                              - OPEN_CONVERSATION
                                        required:
                                          - type
                              required:
                                - trigger
                                - steps
                            publishedAt:
                              type: string
                              format: date-time
                              nullable: true
                            publishedByUserId:
                              type: string
                              nullable: true
                            createdAt:
                              type: string
                              format: date-time
                              nullable: true
                          required:
                            - id
                            - flowId
                            - version
                            - status
                            - definition
                            - createdAt
                        steps:
                          type: array
                          items:
                            type: object
                            properties:
                              id:
                                type: string
                              executionId:
                                type: string
                              stepId:
                                type: string
                                nullable: true
                              status:
                                type: string
                                enum:
                                  - PENDING
                                  - RUNNING
                                  - COMPLETED
                                  - FAILED
                                  - SKIPPED
                              attemptCount:
                                type: number
                              input:
                                default: {}
                                type: object
                                properties:
                                  type:
                                    type: string
                                    enum:
                                      - COMMENT_CREATED
                                      - DM_RECEIVED
                                      - QUICK_REPLY_CLICKED
                                      - BUTTON_CLICKED
                                      - MANUAL_TEST
                                    nullable: true
                                  platform:
                                    type: string
                                    enum:
                                      - INSTAGRAM
                                      - FACEBOOK
                                      - TIKTOK
                                    nullable: true
                                  socialAccountId:
                                    type: string
                                    nullable: true
                                  postId:
                                    type: string
                                    nullable: true
                                  conversationId:
                                    type: string
                                    nullable: true
                                  conversationMessageId:
                                    type: string
                                    nullable: true
                                  fetchedCommentId:
                                    type: string
                                    nullable: true
                                  senderExternalId:
                                    type: string
                                    nullable: true
                                  externalMessageId:
                                    type: string
                                    nullable: true
                                  text:
                                    type: string
                                    nullable: true
                                  payload:
                                    type: string
                                    nullable: true
                                additionalProperties:
                                  nullable: true
                              output:
                                default: {}
                                type: object
                                properties: {}
                                additionalProperties:
                                  nullable: true
                              error:
                                type: object
                                properties:
                                  code:
                                    type: string
                                    nullable: true
                                  message:
                                    type: string
                                    nullable: true
                                  retryable:
                                    type: boolean
                                    nullable: true
                                additionalProperties:
                                  nullable: true
                                nullable: true
                              startedAt:
                                type: string
                                format: date-time
                                nullable: true
                              completedAt:
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
                            required:
                              - id
                              - executionId
                              - status
                              - attemptCount
                              - createdAt
                              - updatedAt
                        conversation:
                          type: object
                          properties:
                            id:
                              type: string
                            teamId:
                              type: string
                            socialAccountId:
                              type: string
                            platform:
                              type: string
                              enum:
                                - INSTAGRAM
                                - FACEBOOK
                              description: >-
                                Messaging platform. Extensible: new platforms
                                are added over time, so handle unknown values
                                gracefully rather than switching exhaustively.
                            externalConversationId:
                              type: string
                              nullable: true
                            externalParticipantId:
                              type: string
                            participantUsername:
                              type: string
                              nullable: true
                            participantDisplayName:
                              type: string
                              nullable: true
                            participantAvatarUrl:
                              type: string
                              nullable: true
                            status:
                              type: string
                              enum:
                                - OPEN
                                - ARCHIVED
                            lastMessageAt:
                              type: string
                              format: date-time
                              nullable: true
                            lastActivityAt:
                              type: string
                              format: date-time
                              nullable: true
                            lastMessagePreview:
                              type: string
                              nullable: true
                            lastReadAt:
                              type: string
                              format: date-time
                              nullable: true
                            unreadCount:
                              type: number
                            platformSeenAt:
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
                            platformData:
                              default: {}
                              type: object
                              properties:
                                canReply:
                                  type: boolean
                                  nullable: true
                                lastInboundAt:
                                  type: string
                                  format: date-time
                                  nullable: true
                                providerStateSync:
                                  type: object
                                  properties:
                                    action:
                                      type: string
                                      enum:
                                        - ARCHIVE
                                        - OPEN
                                    status:
                                      type: string
                                      enum:
                                        - SYNCED
                                        - SYNC_FAILED
                                        - UNSUPPORTED
                                    reason:
                                      type: string
                                      nullable: true
                                    error:
                                      type: string
                                      nullable: true
                                    syncedAt:
                                      type: string
                                      format: date-time
                                      nullable: true
                                  required:
                                    - action
                                    - status
                                  nullable: true
                            socialAccount:
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
                          required:
                            - id
                            - teamId
                            - socialAccountId
                            - platform
                            - externalParticipantId
                            - status
                            - lastActivityAt
                            - unreadCount
                            - createdAt
                            - updatedAt
                          nullable: true
                        conversationMessage:
                          type: object
                          properties:
                            id:
                              type: string
                            conversationId:
                              type: string
                            teamId:
                              type: string
                            socialAccountId:
                              type: string
                            platform:
                              type: string
                              enum:
                                - INSTAGRAM
                                - FACEBOOK
                              description: >-
                                Messaging platform. Extensible: new platforms
                                are added over time, so handle unknown values
                                gracefully rather than switching exhaustively.
                            direction:
                              type: string
                              enum:
                                - INBOUND
                                - OUTBOUND
                            status:
                              type: string
                              enum:
                                - PENDING
                                - SENT
                                - DELIVERED
                                - SEEN
                                - FAILED
                            source:
                              type: string
                              enum:
                                - PRIVATE_REPLY
                                - DM
                                - WEBHOOK
                                - API
                                - ECHO
                            externalMessageId:
                              type: string
                              nullable: true
                            text:
                              type: string
                              nullable: true
                            attachments:
                              default: []
                              type: array
                              items:
                                type: object
                                properties:
                                  type:
                                    type: string
                                    enum:
                                      - IMAGE
                                      - VIDEO
                                      - AUDIO
                                      - FILE
                                      - POST
                                      - UNKNOWN
                                  url:
                                    type: string
                                    nullable: true
                                  externalId:
                                    type: string
                                    nullable: true
                                  mimeType:
                                    type: string
                                    nullable: true
                                  name:
                                    type: string
                                    nullable: true
                                  captionTrackUrl:
                                    type: string
                                    nullable: true
                                  captionLanguage:
                                    type: string
                                    nullable: true
                                  captionLabel:
                                    type: string
                                    nullable: true
                                required:
                                  - type
                            sentAt:
                              type: string
                              format: date-time
                              nullable: true
                            failedAt:
                              type: string
                              format: date-time
                              nullable: true
                            error:
                              type: string
                              nullable: true
                            seenAt:
                              type: string
                              format: date-time
                              nullable: true
                            replyTo:
                              type: object
                              properties:
                                externalMessageId:
                                  type: string
                                  nullable: true
                                isSelfReply:
                                  type: boolean
                                  nullable: true
                                messageId:
                                  type: string
                                  nullable: true
                              nullable: true
                            privateReplyContext:
                              type: object
                              properties:
                                fetchedCommentId:
                                  type: string
                                externalCommentId:
                                  type: string
                                  nullable: true
                                text:
                                  type: string
                                  nullable: true
                                authorName:
                                  type: string
                                  nullable: true
                                authorAvatarUrl:
                                  type: string
                                  nullable: true
                                publishedAt:
                                  type: string
                                  format: date-time
                                  nullable: true
                                postId:
                                  type: string
                                  nullable: true
                                externalPostId:
                                  type: string
                                  nullable: true
                                postPermalink:
                                  type: string
                                  nullable: true
                                postThumbnailUrl:
                                  type: string
                                  nullable: true
                              required:
                                - fetchedCommentId
                              nullable: true
                            createdAt:
                              type: string
                              format: date-time
                              nullable: true
                            updatedAt:
                              type: string
                              format: date-time
                              nullable: true
                            platformData:
                              default: {}
                              type: object
                              properties:
                                replyTo:
                                  type: object
                                  properties:
                                    externalMessageId:
                                      type: string
                                      nullable: true
                                    isSelfReply:
                                      type: boolean
                                      nullable: true
                                  nullable: true
                                reactions:
                                  type: array
                                  items:
                                    type: object
                                    properties:
                                      senderId:
                                        type: string
                                      reaction:
                                        type: string
                                        nullable: true
                                      emoji:
                                        type: string
                                        nullable: true
                                      reactedAt:
                                        type: string
                                        format: date-time
                                        nullable: true
                                    required:
                                      - senderId
                                quickReplies:
                                  type: array
                                  items:
                                    type: object
                                    properties:
                                      id:
                                        type: string
                                        minLength: 1
                                        maxLength: 36
                                      label:
                                        type: string
                                        minLength: 1
                                        maxLength: 20
                                      payload:
                                        type: string
                                        minLength: 1
                                        maxLength: 1000
                                    required:
                                      - label
                                      - payload
                                buttons:
                                  type: array
                                  items:
                                    discriminator:
                                      propertyName: type
                                    oneOf:
                                      - type: object
                                        properties:
                                          id:
                                            type: string
                                            minLength: 1
                                            maxLength: 36
                                          type:
                                            type: string
                                            enum:
                                              - POSTBACK
                                          label:
                                            type: string
                                            minLength: 1
                                            maxLength: 20
                                          payload:
                                            type: string
                                            minLength: 1
                                            maxLength: 1000
                                        required:
                                          - type
                                          - label
                                          - payload
                                      - type: object
                                        properties:
                                          id:
                                            type: string
                                            minLength: 1
                                            maxLength: 36
                                          type:
                                            type: string
                                            enum:
                                              - URL
                                          label:
                                            type: string
                                            minLength: 1
                                            maxLength: 20
                                          url:
                                            type: string
                                            format: uri
                                        required:
                                          - type
                                          - label
                                          - url
                                      - type: object
                                        properties:
                                          id:
                                            type: string
                                            minLength: 1
                                            maxLength: 36
                                          type:
                                            type: string
                                            enum:
                                              - PHONE
                                          label:
                                            type: string
                                            minLength: 1
                                            maxLength: 20
                                          phoneNumber:
                                            type: string
                                            minLength: 3
                                            maxLength: 30
                                        required:
                                          - type
                                          - label
                                          - phoneNumber
                                carousel:
                                  type: object
                                  properties:
                                    cards:
                                      type: array
                                      items:
                                        type: object
                                        properties:
                                          id:
                                            type: string
                                            minLength: 1
                                            maxLength: 36
                                          title:
                                            type: string
                                            minLength: 1
                                            maxLength: 80
                                          subtitle:
                                            type: string
                                            maxLength: 80
                                            nullable: true
                                          imageUrl:
                                            type: string
                                            format: uri
                                            nullable: true
                                          buttons:
                                            type: array
                                            items:
                                              discriminator:
                                                propertyName: type
                                              oneOf:
                                                - type: object
                                                  properties:
                                                    id:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 36
                                                    type:
                                                      type: string
                                                      enum:
                                                        - POSTBACK
                                                    label:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 20
                                                    payload:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 1000
                                                  required:
                                                    - type
                                                    - label
                                                    - payload
                                                - type: object
                                                  properties:
                                                    id:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 36
                                                    type:
                                                      type: string
                                                      enum:
                                                        - URL
                                                    label:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 20
                                                    url:
                                                      type: string
                                                      format: uri
                                                  required:
                                                    - type
                                                    - label
                                                    - url
                                                - type: object
                                                  properties:
                                                    id:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 36
                                                    type:
                                                      type: string
                                                      enum:
                                                        - PHONE
                                                    label:
                                                      type: string
                                                      minLength: 1
                                                      maxLength: 20
                                                    phoneNumber:
                                                      type: string
                                                      minLength: 3
                                                      maxLength: 30
                                                  required:
                                                    - type
                                                    - label
                                                    - phoneNumber
                                            maxItems: 3
                                        required:
                                          - title
                                      minItems: 1
                                      maxItems: 10
                                  required:
                                    - cards
                                  nullable: true
                                isEcho:
                                  type: boolean
                                  nullable: true
                                isEdited:
                                  type: boolean
                                  nullable: true
                                editedAt:
                                  type: string
                                  format: date-time
                                  nullable: true
                                isPostback:
                                  type: boolean
                                  nullable: true
                                postbackPayload:
                                  type: string
                                  nullable: true
                                isUnsent:
                                  type: boolean
                                  nullable: true
                                unsentAt:
                                  type: string
                                  format: date-time
                                  nullable: true
                          required:
                            - id
                            - conversationId
                            - teamId
                            - socialAccountId
                            - platform
                            - direction
                            - status
                            - source
                            - createdAt
                            - updatedAt
                          nullable: true
                        fetchedComment:
                          type: object
                          properties:
                            id:
                              type: string
                            teamId:
                              type: string
                            organizationId:
                              type: string
                              nullable: true
                            postId:
                              type: string
                              nullable: true
                            importedPostId:
                              type: string
                              nullable: true
                            socialAccountId:
                              type: string
                            importId:
                              type: string
                            platform:
                              type: string
                              enum:
                                - FACEBOOK
                                - INSTAGRAM
                                - LINKEDIN
                                - YOUTUBE
                                - TIKTOK
                                - REDDIT
                                - THREADS
                                - MASTODON
                                - BLUESKY
                                - TWITTER
                            externalId:
                              type: string
                            externalParentId:
                              type: string
                              nullable: true
                            externalPostId:
                              type: string
                              nullable: true
                            authorName:
                              type: string
                              nullable: true
                            authorExternalId:
                              type: string
                              nullable: true
                            authorProfileUrl:
                              type: string
                              nullable: true
                            authorAvatarUrl:
                              type: string
                              nullable: true
                            text:
                              type: string
                              nullable: true
                            likesCount:
                              type: number
                            repliesCount:
                              type: number
                            platformData:
                              default: {}
                              type: object
                              properties:
                                canDelete:
                                  type: boolean
                                  nullable: true
                                canHide:
                                  type: boolean
                                  nullable: true
                                canLike:
                                  type: boolean
                                  nullable: true
                                canModerate:
                                  type: boolean
                                  nullable: true
                                hidden:
                                  type: boolean
                                  nullable: true
                                likedByMe:
                                  type: boolean
                                  nullable: true
                                likedByAutomation:
                                  type: boolean
                                  nullable: true
                                reactionsCount:
                                  type: number
                                  nullable: true
                                reactionType:
                                  type: string
                                  enum:
                                    - LIKE
                                    - LOVE
                                    - WOW
                                    - HAHA
                                    - SAD
                                    - ANGRY
                                  nullable: true
                                owner:
                                  type: boolean
                                  nullable: true
                                hideStatus:
                                  type: string
                                  nullable: true
                                moderationStatus:
                                  type: string
                                  nullable: true
                                approvalStatus:
                                  type: string
                                  nullable: true
                                status:
                                  type: string
                                  nullable: true
                                attachmentType:
                                  type: string
                                  nullable: true
                                attachmentUrl:
                                  type: string
                                  nullable: true
                                cid:
                                  type: string
                                  nullable: true
                                origin:
                                  type: string
                                  enum:
                                    - platform
                                    - bundle
                                  nullable: true
                                source:
                                  type: string
                                  nullable: true
                                mediaProductType:
                                  type: string
                                  nullable: true
                                bundleCommentId:
                                  type: string
                                  nullable: true
                                displayState:
                                  type: string
                                  enum:
                                    - active
                                    - thread_deleted
                                    - platform_missing
                                  nullable: true
                                disabledReason:
                                  type: string
                                  nullable: true
                              additionalProperties:
                                oneOf:
                                  - type: string
                                  - type: number
                                  - type: boolean
                                  - type: string
                                    format: 'null'
                                    nullable: true
                                nullable: true
                            publishedAt:
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
                            - teamId
                            - socialAccountId
                            - importId
                            - platform
                            - externalId
                            - likesCount
                            - repliesCount
                            - createdAt
                            - updatedAt
                          nullable: true
                        socialAccount:
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
                      required:
                        - id
                        - teamId
                        - flowId
                        - flowVersionId
                        - platform
                        - socialAccountId
                        - status
                        - idempotencyKey
                        - createdAt
                        - updatedAt
                  total:
                    type: number
                  nextCursor:
                    type: string
                    nullable: true
                required:
                  - items
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