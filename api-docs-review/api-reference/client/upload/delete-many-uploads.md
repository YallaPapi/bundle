> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Delete many uploads

> Permanently delete several media files in one request. Use it to clean up your library in bulk instead of calling delete per file.



## OpenAPI

````yaml https://api.bundle.social/swagger-json delete /api/v1/upload/
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
    delete:
      tags:
        - upload
      summary: Delete many uploads
      description: >-
        Permanently delete several media files in one request. Use it to clean
        up your library in bulk instead of calling delete per file.
      operationId: upload.deleteMany
      parameters: []
      requestBody:
        description: Body
        content:
          application/json:
            schema:
              type: object
              properties:
                ids:
                  type: array
                  items:
                    type: string
                  minItems: 1
              required:
                - ids
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