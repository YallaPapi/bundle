> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Delete comment

> Permanently delete a comment from bundle.social. Deleting a scheduled comment cancels it before it publishes.



## OpenAPI

````yaml https://api.bundle.social/swagger-json delete /api/v1/comment/{id}
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
  /api/v1/comment/{id}:
    delete:
      tags:
        - comment
      summary: Delete comment
      description: >-
        Permanently delete a comment from bundle.social. Deleting a scheduled
        comment cancels it before it publishes.
      operationId: comment.delete
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
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
                  internalPostId:
                    type: string
                    nullable: true
                  importedPostId:
                    type: string
                    nullable: true
                  internalParentCommentId:
                    type: string
                    nullable: true
                  fetchedParentCommentId:
                    type: string
                    nullable: true
                  title:
                    type: string
                    nullable: true
                  postDate:
                    type: string
                    format: date-time
                    nullable: true
                  postedDate:
                    type: string
                    format: date-time
                    nullable: true
                  status:
                    type: string
                    enum:
                      - DRAFT
                      - SCHEDULED
                      - POSTED
                      - ERROR
                      - DELETED
                      - PROCESSING
                      - RETRYING
                  data:
                    type: object
                    properties:
                      TWITTER:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                        nullable: true
                      FACEBOOK:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                        nullable: true
                      INSTAGRAM:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                        nullable: true
                      THREADS:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                        nullable: true
                      TIKTOK:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                        nullable: true
                      LINKEDIN:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                        nullable: true
                      YOUTUBE:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                        nullable: true
                      REDDIT:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                        nullable: true
                      MASTODON:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                        nullable: true
                      DISCORD:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                        nullable: true
                      SLACK:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                        nullable: true
                      BLUESKY:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                        nullable: true
                  error:
                    type: string
                    nullable: true
                  errors:
                    type: object
                    properties:
                      TIKTOK:
                        type: string
                        nullable: true
                      YOUTUBE:
                        type: string
                        nullable: true
                      INSTAGRAM:
                        type: string
                        nullable: true
                      FACEBOOK:
                        type: string
                        nullable: true
                      TWITTER:
                        type: string
                        nullable: true
                      THREADS:
                        type: string
                        nullable: true
                      LINKEDIN:
                        type: string
                        nullable: true
                      REDDIT:
                        type: string
                        nullable: true
                      MASTODON:
                        type: string
                        nullable: true
                      DISCORD:
                        type: string
                        nullable: true
                      SLACK:
                        type: string
                        nullable: true
                      BLUESKY:
                        type: string
                        nullable: true
                    nullable: true
                  errorsVerbose:
                    type: object
                    properties:
                      TWITTER:
                        type: object
                        properties:
                          code:
                            type: string
                            nullable: true
                          errorMessage:
                            type: string
                            nullable: true
                          isTransient:
                            type: boolean
                            nullable: true
                          retryability:
                            type: string
                            enum:
                              - retryable
                              - non_retryable
                              - unknown
                            nullable: true
                          httpStatus:
                            type: number
                            nullable: true
                          meta:
                            nullable: true
                          userFacingMessage:
                            type: string
                            nullable: true
                        nullable: true
                      FACEBOOK:
                        type: object
                        properties:
                          code:
                            type: string
                            nullable: true
                          errorMessage:
                            type: string
                            nullable: true
                          isTransient:
                            type: boolean
                            nullable: true
                          retryability:
                            type: string
                            enum:
                              - retryable
                              - non_retryable
                              - unknown
                            nullable: true
                          httpStatus:
                            type: number
                            nullable: true
                          meta:
                            nullable: true
                          userFacingMessage:
                            type: string
                            nullable: true
                        nullable: true
                      INSTAGRAM:
                        type: object
                        properties:
                          code:
                            type: string
                            nullable: true
                          errorMessage:
                            type: string
                            nullable: true
                          isTransient:
                            type: boolean
                            nullable: true
                          retryability:
                            type: string
                            enum:
                              - retryable
                              - non_retryable
                              - unknown
                            nullable: true
                          httpStatus:
                            type: number
                            nullable: true
                          meta:
                            nullable: true
                          userFacingMessage:
                            type: string
                            nullable: true
                        nullable: true
                      TIKTOK:
                        type: object
                        properties:
                          code:
                            type: string
                            nullable: true
                          errorMessage:
                            type: string
                            nullable: true
                          isTransient:
                            type: boolean
                            nullable: true
                          retryability:
                            type: string
                            enum:
                              - retryable
                              - non_retryable
                              - unknown
                            nullable: true
                          httpStatus:
                            type: number
                            nullable: true
                          meta:
                            nullable: true
                          userFacingMessage:
                            type: string
                            nullable: true
                        nullable: true
                      LINKEDIN:
                        type: object
                        properties:
                          code:
                            type: string
                            nullable: true
                          errorMessage:
                            type: string
                            nullable: true
                          isTransient:
                            type: boolean
                            nullable: true
                          retryability:
                            type: string
                            enum:
                              - retryable
                              - non_retryable
                              - unknown
                            nullable: true
                          httpStatus:
                            type: number
                            nullable: true
                          meta:
                            nullable: true
                          userFacingMessage:
                            type: string
                            nullable: true
                        nullable: true
                      REDDIT:
                        type: object
                        properties:
                          code:
                            type: string
                            nullable: true
                          errorMessage:
                            type: string
                            nullable: true
                          isTransient:
                            type: boolean
                            nullable: true
                          retryability:
                            type: string
                            enum:
                              - retryable
                              - non_retryable
                              - unknown
                            nullable: true
                          httpStatus:
                            type: number
                            nullable: true
                          meta:
                            nullable: true
                          userFacingMessage:
                            type: string
                            nullable: true
                        nullable: true
                      YOUTUBE:
                        type: object
                        properties:
                          code:
                            type: string
                            nullable: true
                          errorMessage:
                            type: string
                            nullable: true
                          isTransient:
                            type: boolean
                            nullable: true
                          retryability:
                            type: string
                            enum:
                              - retryable
                              - non_retryable
                              - unknown
                            nullable: true
                          httpStatus:
                            type: number
                            nullable: true
                          meta:
                            nullable: true
                          userFacingMessage:
                            type: string
                            nullable: true
                        nullable: true
                      MASTODON:
                        type: object
                        properties:
                          code:
                            type: string
                            nullable: true
                          errorMessage:
                            type: string
                            nullable: true
                          isTransient:
                            type: boolean
                            nullable: true
                          retryability:
                            type: string
                            enum:
                              - retryable
                              - non_retryable
                              - unknown
                            nullable: true
                          httpStatus:
                            type: number
                            nullable: true
                          meta:
                            nullable: true
                          userFacingMessage:
                            type: string
                            nullable: true
                        nullable: true
                      THREADS:
                        type: object
                        properties:
                          code:
                            type: string
                            nullable: true
                          errorMessage:
                            type: string
                            nullable: true
                          isTransient:
                            type: boolean
                            nullable: true
                          retryability:
                            type: string
                            enum:
                              - retryable
                              - non_retryable
                              - unknown
                            nullable: true
                          httpStatus:
                            type: number
                            nullable: true
                          meta:
                            nullable: true
                          userFacingMessage:
                            type: string
                            nullable: true
                        nullable: true
                      DISCORD:
                        type: object
                        properties:
                          code:
                            type: string
                            nullable: true
                          errorMessage:
                            type: string
                            nullable: true
                          isTransient:
                            type: boolean
                            nullable: true
                          retryability:
                            type: string
                            enum:
                              - retryable
                              - non_retryable
                              - unknown
                            nullable: true
                          httpStatus:
                            type: number
                            nullable: true
                          meta:
                            nullable: true
                          userFacingMessage:
                            type: string
                            nullable: true
                        nullable: true
                      SLACK:
                        type: object
                        properties:
                          code:
                            type: string
                            nullable: true
                          errorMessage:
                            type: string
                            nullable: true
                          isTransient:
                            type: boolean
                            nullable: true
                          retryability:
                            type: string
                            enum:
                              - retryable
                              - non_retryable
                              - unknown
                            nullable: true
                          httpStatus:
                            type: number
                            nullable: true
                          meta:
                            nullable: true
                          userFacingMessage:
                            type: string
                            nullable: true
                        nullable: true
                      BLUESKY:
                        type: object
                        properties:
                          code:
                            type: string
                            nullable: true
                          errorMessage:
                            type: string
                            nullable: true
                          isTransient:
                            type: boolean
                            nullable: true
                          retryability:
                            type: string
                            enum:
                              - retryable
                              - non_retryable
                              - unknown
                            nullable: true
                          httpStatus:
                            type: number
                            nullable: true
                          meta:
                            nullable: true
                          userFacingMessage:
                            type: string
                            nullable: true
                        nullable: true
                    nullable: true
                  externalData:
                    type: object
                    properties:
                      TWITTER:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          permalink:
                            type: string
                            nullable: true
                        nullable: true
                      FACEBOOK:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          permalink:
                            type: string
                            nullable: true
                        nullable: true
                      INSTAGRAM:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          permalink:
                            type: string
                            nullable: true
                        nullable: true
                      TIKTOK:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          permalink:
                            type: string
                            nullable: true
                        nullable: true
                      LINKEDIN:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          commentUrn:
                            type: string
                            nullable: true
                          permalink:
                            type: string
                            nullable: true
                        nullable: true
                      REDDIT:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          permalink:
                            type: string
                            nullable: true
                        nullable: true
                      YOUTUBE:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          permalink:
                            type: string
                            nullable: true
                        nullable: true
                      MASTODON:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          permalink:
                            type: string
                            nullable: true
                        nullable: true
                      THREADS:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          permalink:
                            type: string
                            nullable: true
                        nullable: true
                      DISCORD:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          permalink:
                            type: string
                            nullable: true
                        nullable: true
                      SLACK:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          permalink:
                            type: string
                            nullable: true
                        nullable: true
                      BLUESKY:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          uri:
                            type: string
                            nullable: true
                          cid:
                            type: string
                            nullable: true
                            description: 'Content ID of the created record '
                          permalink:
                            type: string
                            nullable: true
                          did:
                            type: string
                            nullable: true
                            description: Author DID (owner of the record)
                        nullable: true
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
                  - status
                  - data
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