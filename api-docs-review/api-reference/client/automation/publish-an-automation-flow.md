> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Publish an automation flow

> Validate a draft flow and make it live, so that matching events start triggering it. Returns 400 when the flow is not valid.



## OpenAPI

````yaml https://api.bundle.social/swagger-json post /api/v1/automations/{id}/publish
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
  /api/v1/automations/{id}/publish:
    post:
      tags:
        - automation
      summary: Publish an automation flow
      description: >-
        Validate a draft flow and make it live, so that matching events start
        triggering it. Returns 400 when the flow is not valid.
      operationId: automation.publishFlow
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        description: Body
        content:
          application/json:
            schema:
              type: object
              properties:
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
                      minItems: 1
                      maxItems: 100
                  required:
                    - trigger
                    - steps
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
                required:
                  - id
                  - teamId
                  - name
                  - status
                  - platformScope
                  - createdAt
                  - updatedAt
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