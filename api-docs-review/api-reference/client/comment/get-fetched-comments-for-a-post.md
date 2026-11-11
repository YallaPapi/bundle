> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Get fetched comments for a post

> List the comments pulled in by a comment import, with pagination. Use this to read audience replies and decide which ones need a response.



## OpenAPI

````yaml https://api.bundle.social/swagger-json get /api/v1/comment/import/comments
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
  /api/v1/comment/import/comments:
    get:
      tags:
        - comment
      summary: Get fetched comments for a post
      description: >-
        List the comments pulled in by a comment import, with pagination. Use
        this to read audience replies and decide which ones need a response.
      operationId: comment.importGetFetchedComments
      parameters:
        - name: teamId
          in: query
          required: true
          schema:
            type: string
        - name: postId
          in: query
          schema:
            type: string
        - name: importedPostId
          in: query
          schema:
            type: string
        - name: platform
          in: query
          schema:
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
        - name: socialAccountId
          in: query
          schema:
            type: string
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