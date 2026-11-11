> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Connect social account for team

> Generate OAuth URL for social account connection. Redirect user to this URL to connect social account. For Mastodon and Bluesky an unusable `serverUrl` returns 400 with the reason, while a reachable-but-failing instance returns 502.



## OpenAPI

````yaml https://api.bundle.social/swagger-json post /api/v1/social-account/connect
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
  /api/v1/social-account/connect:
    post:
      tags:
        - socialAccount
      summary: Connect social account for team
      description: >-
        Generate OAuth URL for social account connection. Redirect user to this
        URL to connect social account. For Mastodon and Bluesky an unusable
        `serverUrl` returns 400 with the reason, while a reachable-but-failing
        instance returns 502.
      operationId: socialAccount.connect
      parameters: []
      requestBody:
        description: Body
        content:
          application/json:
            schema:
              type: object
              properties:
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
                redirectUrl:
                  description: >-
                    Client-provided return URL. After the OAuth flow completes
                    (success or error), the user will be redirected here with
                    success/error query params appended. Must be a well-formed
                    http/https URL.
                  type: string
                  format: uri
                serverUrl:
                  type: string
                  format: uri
                  description: >-
                    Mastodon or Bluesky only. Required for Mastodon (the user's
                    instance, e.g. https://mastodon.social). Optional for
                    Bluesky - omit it to use the default issuer
                    https://bsky.social, or pass a custom PDS/entryway issuer.
                disableAutoLogin:
                  default: false
                  type: boolean
                  description: >-
                    Optional. When true, adds provider-specific flags to avoid
                    automatic login/auto-approval where supported.
                tiktokForceLogin:
                  default: false
                  type: boolean
                  description: >-
                    Optional and experimental. TikTok only. When true, routes
                    authorization through TikTok logout to request a fresh login
                    session.
                forceBrowserOAuth:
                  default: false
                  type: boolean
                  description: >-
                    Optional. Instagram direct OAuth only. When true, Instagram
                    asks for a fresh login instead of reusing the account logged
                    in on that browser. In the hosted portal it applies only on
                    iPhone/iPad. Staying in the browser on iOS is the default
                    for every connection and needs no flag.
                instagramConnectionMethod:
                  type: string
                  enum:
                    - FACEBOOK
                    - INSTAGRAM
                  description: Instagram only - connection method
                withBusinessScope:
                  default: false
                  type: boolean
                  description: >-
                    Facebook and Instagram: include business_management,
                    ads_management, ads_read scopes. YouTube: include the
                    monetary analytics scope (enables revenue/monetization
                    data).
                withMessagingScope:
                  default: false
                  type: boolean
                  description: >-
                    Facebook and Instagram: include the Meta messaging (DM)
                    scopes. Ignored unless messaging is enabled for your
                    organization.
                reconnect:
                  default: false
                  type: boolean
                  description: >-
                    Re-authorize the account already connected to this team in
                    place: tokens and permissions are refreshed while the
                    account, its posts and scheduled destinations stay. The user
                    must log in with the same account. Currently supported for
                    Instagram connected with instagramConnectionMethod
                    INSTAGRAM.
              required:
                - type
                - teamId
                - redirectUrl
      responses:
        '200':
          description: '200'
          content:
            application/json:
              schema:
                type: object
                properties:
                  url:
                    type: string
                    description: >-
                      OAuth URL - Redirect user to this URL to connect social
                      account
                required:
                  - url
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