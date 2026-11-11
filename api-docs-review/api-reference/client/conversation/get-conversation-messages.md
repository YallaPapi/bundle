> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Get conversation messages

> List the messages of a conversation. Pages walk backwards in time, while the messages inside a page are ordered oldest first, ready to render. Includes attachments, reactions and delivery state. Paginate with `offset` (`limit` max 500, default 10) or by passing the previous response's `nextCursor` back as `cursor`; the two cannot be combined. `total` is returned on the first page only.



## OpenAPI

````yaml https://api.bundle.social/swagger-json get /api/v1/conversations/{id}/messages
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
  /api/v1/conversations/{id}/messages:
    get:
      tags:
        - conversation
      summary: Get conversation messages
      description: >-
        List the messages of a conversation. Pages walk backwards in time, while
        the messages inside a page are ordered oldest first, ready to render.
        Includes attachments, reactions and delivery state. Paginate with
        `offset` (`limit` max 500, default 10) or by passing the previous
        response's `nextCursor` back as `cursor`; the two cannot be combined.
        `total` is returned on the first page only.
      operationId: conversation.getMessages
      parameters:
        - name: id
          in: path
          required: true
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
                            Messaging platform. Extensible: new platforms are
                            added over time, so handle unknown values gracefully
                            rather than switching exhaustively.
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