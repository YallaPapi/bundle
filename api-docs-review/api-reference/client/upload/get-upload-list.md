> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Get upload list

> List the media files in your team's library, newest first. Each file carries `posts`, the links to the posts using it — pass `includePosts=false` to leave them out. Page with `limit` and `offset`. To check whether specific files already exist, filter by `ids` or `urls` instead of listing everything.



## OpenAPI

````yaml https://api.bundle.social/swagger-json get /api/v1/upload/
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
  /api/v1/upload/:
    get:
      tags:
        - upload
      summary: Get upload list
      description: >-
        List the media files in your team's library, newest first. Each file
        carries `posts`, the links to the posts using it — pass
        `includePosts=false` to leave them out. Page with `limit` and `offset`.
        To check whether specific files already exist, filter by `ids` or `urls`
        instead of listing everything.
      operationId: upload.getList
      parameters:
        - name: teamId
          in: query
          schema:
            type: string
            nullable: true
        - name: type
          in: query
          schema:
            type: string
            enum:
              - image
              - video
              - document
            nullable: true
        - name: types
          in: query
          schema:
            type: array
            items:
              type: string
              enum:
                - image
                - video
                - document
            maxItems: 3
            nullable: true
        - name: status
          in: query
          schema:
            type: string
            enum:
              - USED
              - UNUSED
            nullable: true
        - name: ids
          in: query
          schema:
            type: array
            items:
              type: string
            maxItems: 100
            nullable: true
        - name: urls
          in: query
          schema:
            type: array
            items:
              type: string
            maxItems: 100
            nullable: true
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            nullable: true
        - name: includePosts
          in: query
          schema:
            default: true
            oneOf:
              - type: boolean
              - type: string
                enum:
                  - 'true'
              - type: string
                enum:
                  - 'false'
            nullable: true
        - name: offset
          in: query
          schema:
            default: 0
            type: integer
            minimum: 0
            nullable: true
      responses:
        '200':
          description: '200'
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: string
                    teamId:
                      type: string
                      nullable: true
                    organizationId:
                      type: string
                      nullable: true
                    iconUrl:
                      type: string
                      format: uri
                      nullable: true
                    thumbnailUrl:
                      type: string
                      format: uri
                      nullable: true
                    url:
                      type: string
                      format: uri
                      nullable: true
                    externalLink:
                      type: string
                      format: uri
                      nullable: true
                    iconPath:
                      type: string
                      nullable: true
                    thumbnailPath:
                      type: string
                      nullable: true
                    path:
                      type: string
                      nullable: true
                    type:
                      type: string
                      enum:
                        - image
                        - video
                        - document
                    width:
                      type: number
                      nullable: true
                    height:
                      type: number
                      nullable: true
                    fileSize:
                      type: number
                      nullable: true
                    videoLength:
                      type: number
                      nullable: true
                    mime:
                      type: string
                      nullable: true
                    ext:
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
                    posts:
                      type: array
                      items:
                        type: object
                        properties:
                          postId:
                            type: string
                          uploadId:
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
                          - postId
                          - uploadId
                          - createdAt
                          - updatedAt
                  required:
                    - id
                    - type
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