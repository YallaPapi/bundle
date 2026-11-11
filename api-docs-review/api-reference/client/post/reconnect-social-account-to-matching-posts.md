> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Reconnect social account to matching posts

> Reattach a newly connected social account to posts that were orphaned when the previous account was disconnected, so scheduled posts publish instead of failing.



## OpenAPI

````yaml https://api.bundle.social/swagger-json post /api/v1/post/reconnect-social-account
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
  /api/v1/post/reconnect-social-account:
    post:
      tags:
        - post
      summary: Reconnect social account to matching posts
      description: >-
        Reattach a newly connected social account to posts that were orphaned
        when the previous account was disconnected, so scheduled posts publish
        instead of failing.
      operationId: post.reconnectSocialAccount
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
                postIds:
                  type: array
                  items:
                    type: string
              required:
                - teamId
                - type
      responses:
        '200':
          description: '200'
          content:
            application/json:
              schema:
                type: object
                properties:
                  total:
                    type: number
                  succeeded:
                    type: number
                  failed:
                    type: number
                  results:
                    type: array
                    items:
                      type: object
                      properties:
                        postId:
                          type: string
                        title:
                          type: string
                          nullable: true
                        success:
                          type: boolean
                        statusBefore:
                          type: string
                          enum:
                            - DRAFT
                            - SCHEDULED
                            - POSTED
                            - ERROR
                            - DELETED
                            - PROCESSING
                            - REVIEW
                            - RETRYING
                        statusAfter:
                          type: string
                          enum:
                            - DRAFT
                            - SCHEDULED
                            - POSTED
                            - ERROR
                            - DELETED
                            - PROCESSING
                            - REVIEW
                            - RETRYING
                        message:
                          type: string
                      required:
                        - postId
                        - success
                required:
                  - total
                  - succeeded
                  - failed
                  - results
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