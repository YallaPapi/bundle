> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Search for Instagram Business/Creator user by username

> Checks if an Instagram user exists and returns their public profile data. Only works for Business and Creator accounts and only when Instagram is connected via Facebook Login. Returns followers_count, media_count, and profile picture if available.



## OpenAPI

````yaml https://api.bundle.social/swagger-json get /api/v1/misc/instagram/tags
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
  /api/v1/misc/instagram/tags:
    get:
      tags:
        - misc
      summary: Search for Instagram Business/Creator user by username
      description: >-
        Checks if an Instagram user exists and returns their public profile
        data. Only works for Business and Creator accounts and only when
        Instagram is connected via Facebook Login. Returns followers_count,
        media_count, and profile picture if available.
      operationId: misc.instagram.businessDiscovery
      parameters:
        - name: teamId
          in: query
          required: true
          schema:
            type: string
        - name: username
          in: query
          description: Instagram username to search for
          required: true
          schema:
            type: string
            minLength: 1
      responses:
        '200':
          description: '200'
          content:
            application/json:
              schema:
                type: object
                properties:
                  exists:
                    type: boolean
                    description: >-
                      Whether the user is discoverable via Instagram
                      business_discovery (typically Business/Creator).
                      Personal/private accounts can return false even if
                      taggable in media payload.
                  data:
                    type: object
                    properties:
                      id:
                        type: string
                        description: Instagram User ID
                      username:
                        type: string
                        description: Instagram username
                      followers_count:
                        type: number
                        description: Number of followers
                      media_count:
                        type: number
                        description: Number of media posts
                      profile_picture_url:
                        type: string
                        format: uri
                        description: Profile picture URL if available
                      biography:
                        type: string
                        description: User biography if available
                      name:
                        type: string
                        description: Full name if available
                      media:
                        type: object
                        properties:
                          data:
                            type: array
                            items:
                              type: object
                              properties:
                                id:
                                  type: string
                                  description: Instagram Media ID
                                media_type:
                                  type: string
                                  description: Instagram media type
                                like_count:
                                  type: number
                                  description: Number of likes if available
                                comments_count:
                                  type: number
                                  description: Number of comments if available
                                timestamp:
                                  type: string
                                  description: Media publication timestamp
                                caption:
                                  type: string
                                  description: Media caption if available
                              required:
                                - id
                                - media_type
                        required:
                          - data
                        description: Up to 12 recent public media items
                    required:
                      - id
                      - username
                      - followers_count
                      - media_count
                    description: User data if exists, null otherwise
                    nullable: true
                required:
                  - exists
                  - data
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