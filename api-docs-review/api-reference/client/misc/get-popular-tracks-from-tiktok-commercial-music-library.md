> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Get popular tracks from TikTok Commercial Music Library

> Retrieve up to 100 popular tracks pre-cleared for organic content and ad creation from TikTok CML.



## OpenAPI

````yaml https://api.bundle.social/swagger-json get /api/v1/misc/tiktok/cml/trending-list
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
  /api/v1/misc/tiktok/cml/trending-list:
    get:
      tags:
        - misc
      summary: Get popular tracks from TikTok Commercial Music Library
      description: >-
        Retrieve up to 100 popular tracks pre-cleared for organic content and ad
        creation from TikTok CML.
      operationId: misc.tiktok.getCommercialMusicTrendingList
      parameters:
        - name: teamId
          in: query
          required: true
          schema:
            type: string
        - name: genre
          in: query
          description: Genre filter for commercial music results.
          schema:
            default: POP
            type: string
            enum:
              - ROCK
              - POP
              - LATIN
              - METAL
              - ELECTRONIC
              - HIP_HOP/RAP
              - ALTERNATIVE/INDIE
              - R&B/SOUL
              - COUNTRY
              - CLASSICAL
              - JAZZ
              - CHILDHOOD
              - ALTERNATIVE_HIP_HOP
              - AMBIENT
              - BOSSA_NOVA
              - BRAZILIAN_FUNK_STYLE
              - CHILL_BEATS
              - CHILLOUT
              - CHINESE_POP
              - CHRISTIAN_MUSIC
              - COUNTRY_POP
              - DANCE_POP
              - DISCO
              - DJ
              - DRUM&BASS
              - DUBSTEP
              - EDM
              - FUNK
              - HOUSE
              - INDIE_POP
              - J-POP
              - K-POP
              - LATIN_POP
              - LO-FI
              - OLD_SCHOOL
              - PUNK
              - RUSSIAN_POP
              - SOUL
              - SOUNDTRACK
              - SYNTH_POP
              - TECHNO
              - TEEN_POP
        - name: dateRange
          in: query
          description: Timeframe for popular tracks ranking.
          schema:
            default: 7DAY
            type: string
            enum:
              - 1DAY
              - 7DAY
              - 30DAY
      responses:
        '200':
          description: List of trending tracks.
          content:
            application/json:
              schema:
                default: []
                type: array
                items:
                  type: object
                  properties:
                    commercial_music_name:
                      type: string
                      nullable: true
                      description: The name of the commercial music track.
                    duration:
                      type: integer
                      nullable: true
                      description: Track duration in seconds.
                    thumbnail_url:
                      type: string
                      format: uri
                      description: Thumbnail image URL for the track.
                    artist:
                      type: string
                      description: Artist name.
                    preview_url:
                      type: string
                      format: uri
                      nullable: true
                      description: Track preview URL (valid for six hours).
                    genres:
                      default: []
                      type: array
                      items:
                        type: string
                      description: List of genres associated with the track.
                    rank_position:
                      type: string
                      description: Current rank position in the selected region.
                    trending_history:
                      default: []
                      type: array
                      items:
                        type: object
                        properties:
                          date:
                            type: string
                            description: Date in YYYY-MM-DD format.
                          rank_position_daily:
                            type: string
                            nullable: true
                            description: >-
                              Rank position on a specific date. Can be null if
                              not ranked.
                        required:
                          - date
                      description: Historical ranking data (up to 30 days).
                    full_duration_song_clip:
                      type: object
                      properties:
                        preview_url:
                          type: string
                          format: uri
                          nullable: true
                          description: Track preview URL (valid for six hours).
                        duration:
                          type: integer
                          nullable: true
                          description: Track duration in seconds.
                        song_clip_id:
                          type: string
                          description: >-
                            Track clip ID that can be used as music_sound_id in
                            publish endpoint.
                      required:
                        - song_clip_id
                      nullable: true
                    trending_song_clip:
                      type: object
                      properties:
                        preview_url:
                          type: string
                          format: uri
                          nullable: true
                          description: Track preview URL (valid for six hours).
                        duration:
                          type: integer
                          nullable: true
                          description: Track duration in seconds.
                        song_clip_id:
                          type: string
                          description: >-
                            Track clip ID that can be used as music_sound_id in
                            publish endpoint.
                      required:
                        - song_clip_id
                      nullable: true
                  required:
                    - thumbnail_url
                    - artist
                    - rank_position
                description: List of trending tracks.
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