> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Create portal link

> Simplify connect flow. Create a portal link which can be used to manage connected social accounts directly on bundle.social platform without implementing the logic on your side.



## OpenAPI

````yaml https://api.bundle.social/swagger-json post /api/v1/social-account/create-portal-link
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
  /api/v1/social-account/create-portal-link:
    post:
      tags:
        - socialAccount
      summary: Create portal link
      description: >-
        Simplify connect flow. Create a portal link which can be used to manage
        connected social accounts directly on bundle.social platform without
        implementing the logic on your side.
      operationId: socialAccount.createPortalLink
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
                redirectUrl:
                  type: string
                  format: uri
                socialAccountTypes:
                  type: array
                  items:
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
                    Optional. If true, portal will request provider-specific
                    anti-auto-login behavior where supported.
                tiktokForceLogin:
                  default: false
                  type: boolean
                  description: >-
                    Optional and experimental. TikTok only. When true, portal
                    routes TikTok authorization through logout to request a
                    fresh login session.
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
                  type: boolean
                  description: >-
                    Optional. Facebook and Instagram only - when provided,
                    portal skips business scope selection modal for Facebook
                    login paths.
                withMessagingScope:
                  type: boolean
                  description: >-
                    Optional. Facebook and Instagram only - request the Meta
                    messaging (DM) scopes. Ignored unless messaging is enabled
                    for your organization.
                expiresIn:
                  type: integer
                  minimum: 5
                  maximum: 2880
                  description: >-
                    Time in minutes, after which the link will expire. Minimum 5
                    minutes, maximum 48 hours.
                logoUrl:
                  type: string
                  format: uri
                userLogoUrl:
                  type: string
                  format: uri
                userName:
                  type: string
                goBackButtonText:
                  type: string
                hidePoweredBy:
                  type: boolean
                hideGoBackButton:
                  type: boolean
                hideUserLogo:
                  type: boolean
                hideUserName:
                  type: boolean
                hideLanguageSwitcher:
                  type: boolean
                showModalOnConnectSuccess:
                  type: boolean
                language:
                  default: en
                  type: string
                  enum:
                    - en
                    - pl
                    - fr
                    - hi
                    - sv
                    - de
                    - es
                    - it
                    - nl
                    - pt
                    - ru
                    - tr
                    - zh
                    - da
                    - th
                    - ko
                    - he
                    - ar
                maxSocialAccountsConnected:
                  type: number
              required:
                - teamId
                - socialAccountTypes
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