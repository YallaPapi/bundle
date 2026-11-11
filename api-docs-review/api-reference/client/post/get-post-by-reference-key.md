> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Get post by reference key

> Retrieve a single post using your own reference key instead of the bundle.social post ID. Useful when you store your own identifier on create and want to look the post up later without keeping a mapping table.



## OpenAPI

````yaml https://api.bundle.social/swagger-json get /api/v1/post/reference-key/{referenceKey}
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
  /api/v1/post/reference-key/{referenceKey}:
    get:
      tags:
        - post
      summary: Get post by reference key
      description: >-
        Retrieve a single post using your own reference key instead of the
        bundle.social post ID. Useful when you store your own identifier on
        create and want to look the post up later without keeping a mapping
        table.
      operationId: post.getByReferenceKey
      parameters:
        - name: referenceKey
          in: path
          required: true
          schema:
            type: string
            minLength: 1
            maxLength: 128
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
                  title:
                    type: string
                  referenceKey:
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
                      - REVIEW
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
                          uploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          mediaItems:
                            type: array
                            items:
                              type: object
                              properties:
                                uploadId:
                                  type: string
                                altText:
                                  type: string
                                  maxLength: 1000
                                  nullable: true
                                  description: >-
                                    Alternative text for the image, used by
                                    screen readers. Applies to images/GIFs only.
                              required:
                                - uploadId
                            nullable: true
                          replySettings:
                            type: string
                            enum:
                              - EVERYONE
                              - FOLLOWING
                              - MENTIONED_USERS
                              - SUBSCRIBERS
                              - VERIFIED
                            nullable: true
                          poll:
                            type: object
                            properties:
                              options:
                                type: array
                                items:
                                  type: string
                                  minLength: 1
                                  maxLength: 25
                                minItems: 2
                                maxItems: 4
                              durationMinutes:
                                type: integer
                                minimum: 5
                                maximum: 10080
                            required:
                              - options
                              - durationMinutes
                            nullable: true
                          quoteTweetId:
                            type: string
                            nullable: true
                          replyToTweetId:
                            type: string
                            nullable: true
                          subscribersOnly:
                            type: boolean
                            nullable: true
                          thread:
                            type: array
                            items:
                              type: object
                              properties:
                                text:
                                  type: string
                                  maxLength: 25000
                                  nullable: true
                                uploadIds:
                                  type: array
                                  items:
                                    type: string
                                  nullable: true
                            maxItems: 25
                            nullable: true
                          tweetStorm:
                            type: boolean
                            nullable: true
                          tweetStormNumbering:
                            type: boolean
                            nullable: true
                          isAiGenerated:
                            default: false
                            type: boolean
                            nullable: true
                            description: >-
                              Set to true if the post contains AI-generated
                              media. Adds X's 'made with AI' label.
                        nullable: true
                      PINTEREST:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                          description:
                            type: string
                            nullable: true
                          boardName:
                            type: string
                          uploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          thumbnail:
                            type: string
                            nullable: true
                            description: The URL to image uploaded on bundle.social.
                          link:
                            type: string
                            nullable: true
                            description: The URL to which the Pin will link to.
                          altText:
                            type: string
                            nullable: true
                            description: >-
                              The alt text for the image. This is used by screen
                              readers and when the image can't be loaded.
                          note:
                            type: string
                            nullable: true
                            description: >-
                              A note about the Pin. This is not visible to the
                              public.
                          dominantColor:
                            type: string
                            nullable: true
                            description: >-
                              The dominant color of the image. This is used to
                              display the image before it's loaded.
                          isAiGenerated:
                            default: false
                            type: boolean
                            nullable: true
                            description: >-
                              Set to true if the Pin content was generated or
                              modified by AI. Adds Pinterest's AI disclosure
                              label.
                        required:
                          - boardName
                        nullable: true
                      FACEBOOK:
                        type: object
                        properties:
                          type:
                            default: POST
                            type: string
                            enum:
                              - POST
                              - REEL
                              - STORY
                          text:
                            type: string
                            nullable: true
                          uploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          mediaItems:
                            type: array
                            items:
                              type: object
                              properties:
                                uploadId:
                                  type: string
                                altText:
                                  type: string
                                  nullable: true
                              required:
                                - uploadId
                            nullable: true
                          link:
                            type: string
                            nullable: true
                            description: >-
                              The URL to which the post will link to. Only
                              available for type POST.
                          thumbnail:
                            type: string
                            nullable: true
                            description: The URL to image uploaded on bundle.social.
                          mediaTitle:
                            type: string
                            nullable: true
                            description: >-
                              Title for video posts (type POST with video only,
                              not REEL or STORY). This is displayed as the video
                              title on Facebook.
                          nativeScheduleTime:
                            type: string
                            format: date-time
                            nullable: true
                            description: >-
                              If passed, instead of publishing immediately, the
                              post will be scheduled for the given date/time
                              directly in Meta scheduler. Local date/time as ISO
                              8601 string max 30 days in the future.
                          textFormatPresetId:
                            type: string
                            nullable: true
                            description: >-
                              Facebook text background preset ID (colored
                              status), e.g. 1679248482160767 for blue. Only
                              available for type POST without video.
                        nullable: true
                      INSTAGRAM:
                        type: object
                        properties:
                          type:
                            default: POST
                            type: string
                            enum:
                              - POST
                              - REEL
                              - STORY
                          text:
                            type: string
                            nullable: true
                          uploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          altText:
                            type: string
                            nullable: true
                            description: Alternative text for a single image post.
                          thumbnailOffset:
                            default: 0
                            type: number
                            nullable: true
                            description: >-
                              Choose a frame of the published video as the cover
                              photo in ms
                          thumbnail:
                            type: string
                            nullable: true
                            description: The URL to image uploaded on bundle.social.
                          shareToFeed:
                            default: true
                            type: boolean
                            nullable: true
                            description: >-
                              For Reels only.When true, indicates that the reel
                              can appear in both the Feed and Reels tabs.When
                              false, indicates the reel can only appear in the
                              Reels tab.
                          collaborators:
                            type: array
                            items:
                              type: string
                            nullable: true
                          autoFitImage:
                            default: false
                            type: boolean
                            nullable: true
                          autoCropImage:
                            default: false
                            type: boolean
                            nullable: true
                          tagged:
                            type: array
                            items:
                              type: object
                              properties:
                                username:
                                  type: string
                                x:
                                  type: number
                                  minimum: 0
                                  maximum: 1
                                'y':
                                  type: number
                                  minimum: 0
                                  maximum: 1
                              required:
                                - username
                            nullable: true
                          carouselItems:
                            type: array
                            items:
                              type: object
                              properties:
                                uploadId:
                                  type: string
                                altText:
                                  type: string
                                  nullable: true
                                tagged:
                                  type: array
                                  items:
                                    type: object
                                    properties:
                                      username:
                                        type: string
                                      x:
                                        type: number
                                        minimum: 0
                                        maximum: 1
                                      'y':
                                        type: number
                                        minimum: 0
                                        maximum: 1
                                    required:
                                      - username
                                      - x
                                      - 'y'
                                  nullable: true
                              required:
                                - uploadId
                            nullable: true
                          locationId:
                            type: string
                            nullable: true
                          trialParams:
                            type: object
                            properties:
                              graduationStrategy:
                                type: string
                                enum:
                                  - MANUAL
                                  - SS_PERFORMANCE
                            required:
                              - graduationStrategy
                            nullable: true
                            description: >-
                              For Reels only. Trial reels are only shared to
                              non-followers.
                          isPaidPartnership:
                            default: false
                            type: boolean
                            nullable: true
                            description: >-
                              Enables the native "Paid partnership" disclosure
                              label.
                          brandedContentSponsors:
                            type: array
                            items:
                              type: string
                              minLength: 1
                              maxLength: 30
                            maxItems: 2
                            nullable: true
                            description: >-
                              Up to 2 Instagram usernames of the brands tagged
                              as paid-partnership sponsors.
                          musicSoundInfo:
                            type: object
                            properties:
                              musicSoundId:
                                type: string
                                minLength: 1
                                description: >-
                                  Use audio_id from Instagram Audio API search
                                  endpoint.
                              musicSoundVolume:
                                type: integer
                                minimum: 0
                                maximum: 100
                                nullable: true
                                description: Audio volume (0-100).
                              videoOriginalSoundVolume:
                                type: integer
                                minimum: 0
                                maximum: 100
                                nullable: true
                                description: >-
                                  Background volume of the original video sound
                                  (0-100).
                            required:
                              - musicSoundId
                            nullable: true
                            description: >-
                              Information about the Instagram audio asset used
                              for Reels publishing.
                          isAiGenerated:
                            default: false
                            type: boolean
                            nullable: true
                            description: >-
                              Set to true if the content was generated or
                              modified by AI. Adds Instagram's AI content label.
                        nullable: true
                      THREADS:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                          uploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          mediaItems:
                            type: array
                            items:
                              type: object
                              properties:
                                uploadId:
                                  type: string
                                altText:
                                  type: string
                                  nullable: true
                              required:
                                - uploadId
                            nullable: true
                          topicTag:
                            type: string
                            nullable: true
                          replyControl:
                            type: string
                            enum:
                              - everyone
                              - accounts_you_follow
                              - mentioned_only
                              - parent_post_author_only
                              - followers_only
                            nullable: true
                          linkAttachment:
                            type: string
                            nullable: true
                          poll:
                            type: object
                            properties:
                              optionA:
                                type: string
                              optionB:
                                type: string
                              optionC:
                                type: string
                                nullable: true
                              optionD:
                                type: string
                                nullable: true
                            required:
                              - optionA
                              - optionB
                            nullable: true
                          gif:
                            type: object
                            properties:
                              gifId:
                                type: string
                              provider:
                                default: GIPHY
                                type: string
                                enum:
                                  - GIPHY
                            required:
                              - gifId
                            nullable: true
                          allowlistedCountryCodes:
                            type: array
                            items:
                              type: string
                            nullable: true
                          crosspostToInstagramStory:
                            type: boolean
                            nullable: true
                          crosspostToInstagramStoryDarkMode:
                            type: boolean
                            nullable: true
                        nullable: true
                      TIKTOK:
                        type: object
                        properties:
                          type:
                            default: VIDEO
                            type: string
                            enum:
                              - VIDEO
                              - IMAGE
                          text:
                            type: string
                            nullable: true
                          uploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          thumbnail:
                            type: string
                            nullable: true
                            description: The URL to image uploaded on bundle.social.
                          privacy:
                            type: string
                            enum:
                              - SELF_ONLY
                              - PUBLIC_TO_EVERYONE
                              - MUTUAL_FOLLOW_FRIENDS
                              - FOLLOWER_OF_CREATOR
                            nullable: true
                          photoCoverIndex:
                            default: 0
                            type: integer
                            minimum: 0
                            nullable: true
                          isBrandContent:
                            default: false
                            type: boolean
                            nullable: true
                            description: >-
                              Set to true if the video is a paid partnership to
                              promote a third-party business.
                          isOrganicBrandContent:
                            default: false
                            type: boolean
                            nullable: true
                            description: >-
                              Set to true if this video is promoting the
                              creator's own business.
                          disableComments:
                            default: false
                            type: boolean
                            nullable: true
                            description: >-
                              If set to true, other TikTok users will not be
                              allowed to make comments on this post.
                          disableDuet:
                            default: false
                            type: boolean
                            nullable: true
                            description: >-
                              If set to true, other TikTok users will not be
                              allowed to make Stitches using this post.
                          disableStitch:
                            default: false
                            type: boolean
                            nullable: true
                            description: >-
                              If set to true, other TikTok users will not be
                              allowed to make Duets using this post.
                          thumbnailOffset:
                            default: 0
                            type: number
                            nullable: true
                            description: >-
                              Choose a frame of the published video as the cover
                              photo in ms
                          isAiGenerated:
                            default: false
                            type: boolean
                            nullable: true
                            description: Set to true if this video is AI generated.
                          autoAddMusic:
                            default: false
                            type: boolean
                            nullable: true
                            description: >-
                              If set to true, TikTok will automatically add
                              music to the photos.
                          autoScale:
                            default: false
                            type: boolean
                            nullable: true
                          uploadToDraft:
                            default: false
                            type: boolean
                            nullable: true
                            description: If set to true, upload post as draft.
                          musicSoundInfo:
                            type: object
                            properties:
                              musicSoundId:
                                type: string
                                minLength: 1
                                description: >-
                                  Use song_clip_id from CML trending list
                                  (full_duration_song_clip or
                                  trending_song_clip).
                              musicSoundVolume:
                                type: integer
                                minimum: 0
                                maximum: 100
                                nullable: true
                                description: Commercial sound volume (0-100).
                              musicSoundStart:
                                type: integer
                                minimum: 0
                                nullable: true
                                description: >-
                                  Starting point of the commercial sound in
                                  milliseconds.
                              musicSoundEnd:
                                type: integer
                                minimum: 0
                                nullable: true
                                description: >-
                                  Ending point of the commercial sound in
                                  milliseconds.
                              videoOriginalSoundVolume:
                                type: integer
                                minimum: 0
                                maximum: 100
                                nullable: true
                                description: >-
                                  Background volume of the original video sound
                                  (0-100).
                            required:
                              - musicSoundId
                            nullable: true
                            description: >-
                              Information about the commercial sound (track)
                              used for TikTok publishing.
                        nullable: true
                      LINKEDIN:
                        type: object
                        properties:
                          text:
                            type: string
                          uploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          link:
                            type: string
                            nullable: true
                            description: Optional URL for LinkedIn article preview post.
                          thumbnail:
                            type: string
                            nullable: true
                            description: The URL to image uploaded on bundle.social.
                          mediaTitle:
                            type: string
                            nullable: true
                            description: >-
                              Title for video or document posts. If not provided
                              for videos, LinkedIn displays the posting date
                              under the video.
                          privacy:
                            type: string
                            enum:
                              - CONNECTIONS
                              - PUBLIC
                              - LOGGED_IN
                              - CONTAINER
                            nullable: true
                          hideFromFeed:
                            default: false
                            type: boolean
                            nullable: true
                            description: >-
                              Set to true if the post shouldn't be displayed in
                              the main feed.
                          disableReshare:
                            default: false
                            type: boolean
                            nullable: true
                            description: >-
                              Set to true if the post is not allowed to be
                              reshared.
                        required:
                          - text
                        nullable: true
                      YOUTUBE:
                        type: object
                        properties:
                          type:
                            default: SHORT
                            type: string
                            enum:
                              - VIDEO
                              - SHORT
                          uploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          text:
                            type: string
                            nullable: true
                          description:
                            type: string
                            nullable: true
                          thumbnail:
                            type: string
                            nullable: true
                            description: The URL to image uploaded on bundle.social.
                          privacy:
                            type: string
                            enum:
                              - PRIVATE
                              - PUBLIC
                              - UNLISTED
                            nullable: true
                          defaultLanguage:
                            type: string
                            maxLength: 35
                            nullable: true
                            description: >-
                              BCP-47 language code for the video's title and
                              description, e.g. "en" or "pl".
                          defaultAudioLanguage:
                            type: string
                            maxLength: 35
                            nullable: true
                            description: >-
                              BCP-47 language code for the video's default audio
                              track, e.g. "en" or "pl".
                          madeForKids:
                            default: false
                            type: boolean
                            nullable: true
                            description: Set to true if the video is made for kids.
                          containsSyntheticMedia:
                            default: false
                            type: boolean
                            nullable: true
                            description: Set to true if video contains AI generated content
                          hasPaidProductPlacement:
                            default: false
                            type: boolean
                            nullable: true
                            description: Set to true if video has paid product placement
                        nullable: true
                      REDDIT:
                        type: object
                        properties:
                          sr:
                            type: string
                            description: >-
                              Subreddit name. Example: r/subredditName or
                              u/username
                          text:
                            type: string
                          description:
                            type: string
                            nullable: true
                          uploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          link:
                            type: string
                            nullable: true
                            description: The URL to which the post will link to.
                          nsfw:
                            default: false
                            type: boolean
                            nullable: true
                            description: Set to true if the post is NSFW.
                          flairId:
                            type: string
                            nullable: true
                            description: >-
                              Flair ID for the post. Required if the subreddit
                              requires flair selection.
                        required:
                          - sr
                          - text
                        nullable: true
                      DISCORD:
                        type: object
                        properties:
                          channelId:
                            type: string
                          text:
                            type: string
                            nullable: true
                          uploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          username:
                            type: string
                            nullable: true
                            description: >-
                              The username to display as the author of the
                              message.
                          avatarUrl:
                            type: string
                            nullable: true
                            description: >-
                              Avatar url to display as the author of the
                              message.
                        required:
                          - channelId
                        nullable: true
                      SLACK:
                        type: object
                        properties:
                          channelId:
                            type: string
                          text:
                            type: string
                            nullable: true
                          uploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          username:
                            type: string
                            nullable: true
                            description: >-
                              The username to display as the author of the
                              message.
                          avatarUrl:
                            type: string
                            nullable: true
                            description: >-
                              Avatar url to display as the author of the
                              message.
                        required:
                          - channelId
                        nullable: true
                      MASTODON:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                          uploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          thumbnail:
                            type: string
                            nullable: true
                            description: The URL to image uploaded on bundle.social.
                          privacy:
                            type: string
                            enum:
                              - PUBLIC
                              - UNLISTED
                              - PRIVATE
                              - DIRECT
                            nullable: true
                          spoiler:
                            type: string
                            nullable: true
                        nullable: true
                      BLUESKY:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                          uploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          tags:
                            type: array
                            items:
                              type: string
                            maxItems: 8
                            nullable: true
                            description: 'Extra hashtags (without #), up to 8.'
                          labels:
                            type: array
                            items:
                              type: string
                              enum:
                                - '!no-unauthenticated'
                                - porn
                                - sexual
                                - nudity
                                - graphic-media
                            nullable: true
                            description: >-
                              Self-labels (content warnings) applied to the
                              post.
                          quoteUri:
                            description: >-
                              AT-URI of the post to quote (e.g.
                              at://did.../app.bsky.feed.post/<rkey>).
                            type: string
                            maxLength: 512
                            pattern: ^at:\/\/\S+$
                          externalUrl:
                            type: string
                            format: uri
                            nullable: true
                            description: Target URL for the external link card
                          externalTitle:
                            type: string
                            nullable: true
                            description: Card title for the external link card
                          externalDescription:
                            type: string
                            nullable: true
                            description: Card description for the external link card
                          thumbnail:
                            type: string
                            format: uri
                            maxLength: 2048
                            nullable: true
                            description: >-
                              This should be URL to publicly available image
                              uploaded to bundle.social account.
                          videoAlt:
                            type: string
                            maxLength: 10000
                            nullable: true
                            description: Alt text for the video embed.
                        nullable: true
                      GOOGLE_BUSINESS:
                        type: object
                        properties:
                          text:
                            type: string
                            nullable: true
                          uploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                            description: IDs of images/videos uploaded to bundle.social.
                          topicType:
                            default: STANDARD
                            type: string
                            enum:
                              - STANDARD
                              - EVENT
                              - OFFER
                              - ALERT
                            nullable: true
                          languageCode:
                            type: string
                            nullable: true
                            description: Language tag like 'en' or 'en-US'.
                          callToActionType:
                            type: string
                            enum:
                              - BOOK
                              - ORDER
                              - SHOP
                              - LEARN_MORE
                              - SIGN_UP
                              - CALL
                            nullable: true
                          callToActionUrl:
                            type: string
                            nullable: true
                          eventTitle:
                            type: string
                            nullable: true
                          eventStartDate:
                            type: string
                            format: date-time
                            nullable: true
                          eventEndDate:
                            type: string
                            format: date-time
                            nullable: true
                          offerCouponCode:
                            type: string
                            nullable: true
                          offerRedeemOnlineUrl:
                            type: string
                            nullable: true
                          offerTermsConditions:
                            type: string
                            nullable: true
                          alertType:
                            default: COVID_19
                            type: string
                            enum:
                              - COVID_19
                            nullable: true
                            description: Alert type for ALERT posts.
                        nullable: true
                      SNAPCHAT:
                        type: object
                        properties:
                          type:
                            default: STORY
                            type: string
                            enum:
                              - STORY
                              - SPOTLIGHT
                              - SAVED_STORY
                          uploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          text:
                            type: string
                            nullable: true
                          title:
                            type: string
                            nullable: true
                          description:
                            type: string
                            nullable: true
                          locale:
                            type: string
                            nullable: true
                          skipSaveToProfile:
                            default: false
                            type: boolean
                            nullable: true
                          storyDuration:
                            type: string
                            enum:
                              - ONE_DAY
                              - TWO_DAYS
                              - THREE_DAYS
                              - ONE_WEEK
                            nullable: true
                        nullable: true
                  error:
                    type: string
                    nullable: true
                  errors:
                    type: object
                    properties:
                      TWITTER:
                        type: string
                        nullable: true
                      PINTEREST:
                        type: string
                        nullable: true
                      FACEBOOK:
                        type: string
                        nullable: true
                      INSTAGRAM:
                        type: string
                        nullable: true
                      TIKTOK:
                        type: string
                        nullable: true
                      LINKEDIN:
                        type: string
                        nullable: true
                      REDDIT:
                        type: string
                        nullable: true
                      DISCORD:
                        type: string
                        nullable: true
                      SLACK:
                        type: string
                        nullable: true
                      YOUTUBE:
                        type: string
                        nullable: true
                      MASTODON:
                        type: string
                        nullable: true
                      THREADS:
                        type: string
                        nullable: true
                      BLUESKY:
                        type: string
                        nullable: true
                      GOOGLE_BUSINESS:
                        type: string
                        nullable: true
                      SNAPCHAT:
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
                      PINTEREST:
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
                      GOOGLE_BUSINESS:
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
                      SNAPCHAT:
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
                      PINTEREST:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          permalink:
                            type: string
                            nullable: true
                          thumbnail:
                            type: string
                            nullable: true
                        nullable: true
                      FACEBOOK:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          postId:
                            type: string
                            nullable: true
                          videoId:
                            type: string
                            nullable: true
                          permalink:
                            type: string
                            nullable: true
                          thumbnail:
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
                          thumbnail:
                            type: string
                            nullable: true
                          creationId:
                            type: string
                            nullable: true
                            description: >-
                              Media container id; lets a retry detect a
                              container Meta already published.
                        nullable: true
                      TIKTOK:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          shareId:
                            type: string
                            nullable: true
                          requestId:
                            type: string
                            nullable: true
                          permalink:
                            type: string
                            nullable: true
                          status:
                            type: string
                            nullable: true
                        nullable: true
                      LINKEDIN:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          activity:
                            type: string
                            nullable: true
                          permalink:
                            type: string
                            nullable: true
                          thumbnail:
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
                          subreddit_name:
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
                          channelId:
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
                          channelId:
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
                          thumbnail:
                            type: string
                            nullable: true
                          sessionUri:
                            type: string
                            nullable: true
                            description: >-
                              YouTube resumable upload session URI for retry
                              handling
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
                          thumbnail:
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
                          creationId:
                            type: string
                            nullable: true
                            description: >-
                              Media container id; lets a retry detect a
                              container Meta already published.
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
                      GOOGLE_BUSINESS:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                            description: >-
                              Resource name of the Local Post, e.g.
                              'accounts/{accountId}/locations/{locationId}/localPosts/{postId}'.
                          permalink:
                            type: string
                            nullable: true
                            description: >-
                              Public link to the post (searchUrl) when
                              available.
                        nullable: true
                      SNAPCHAT:
                        type: object
                        properties:
                          id:
                            type: string
                            nullable: true
                          mediaId:
                            type: string
                            nullable: true
                          mediaIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          type:
                            type: string
                            enum:
                              - STORY
                              - SPOTLIGHT
                              - SAVED_STORY
                            nullable: true
                          profileId:
                            type: string
                            nullable: true
                          sourceUploadId:
                            type: string
                            nullable: true
                          sourceUploadIds:
                            type: array
                            items:
                              type: string
                            nullable: true
                          mediaUploadedAt:
                            type: string
                            nullable: true
                            description: >-
                              When the media ids were uploaded; Snap expires
                              them after 24h.
                          permalink:
                            type: string
                            nullable: true
                          status:
                            type: string
                            enum:
                              - MEDIA_UPLOADED
                              - MEDIA_PROCESSING
                              - PUBLISHED
                            nullable: true
                        nullable: true
                    nullable: true
                  retryCount:
                    type: number
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
                  firstComment:
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
                  uploads:
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
                        upload:
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
                      required:
                        - postId
                        - uploadId
                        - createdAt
                        - updatedAt
                        - upload
                  socialAccounts:
                    type: array
                    items:
                      type: object
                      properties:
                        postId:
                          type: string
                        socialAccountId:
                          type: string
                        externalPostId:
                          type: string
                          nullable: true
                        externalAlternatePostId:
                          type: string
                          nullable: true
                        externalVideoId:
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
                        deletedAt:
                          type: string
                          format: date-time
                          nullable: true
                        socialAccount:
                          type: object
                          properties:
                            id:
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
                            teamId:
                              type: string
                            username:
                              type: string
                              nullable: true
                            displayName:
                              type: string
                              nullable: true
                            bio:
                              type: string
                              nullable: true
                            avatarUrl:
                              type: string
                              nullable: true
                            externalId:
                              type: string
                              nullable: true
                            providerPageId:
                              type: string
                              nullable: true
                            userUsername:
                              type: string
                              nullable: true
                            userDisplayName:
                              type: string
                              nullable: true
                            userEmail:
                              type: string
                              nullable: true
                            userId:
                              type: string
                              nullable: true
                            channels:
                              type: array
                              items:
                                type: object
                                properties:
                                  id:
                                    type: string
                                  name:
                                    type: string
                                    nullable: true
                                  username:
                                    type: string
                                    nullable: true
                                  address:
                                    type: string
                                    nullable: true
                                  avatarUrl:
                                    type: string
                                    nullable: true
                                  webhook:
                                    type: object
                                    properties:
                                      id:
                                        type: string
                                        nullable: true
                                      name:
                                        type: string
                                        nullable: true
                                      avatar:
                                        type: string
                                        nullable: true
                                      url:
                                        type: string
                                        nullable: true
                                    nullable: true
                                  metadata:
                                    type: object
                                    properties:
                                      allowImages:
                                        type: boolean
                                        nullable: true
                                      allowVideos:
                                        type: boolean
                                        nullable: true
                                      allowGalleries:
                                        type: boolean
                                        nullable: true
                                      linkFlairEnabled:
                                        type: boolean
                                        nullable: true
                                      facebookPageId:
                                        type: string
                                        nullable: true
                                    nullable: true
                                required:
                                  - id
                              nullable: true
                            mastodonServerId:
                              type: string
                              nullable: true
                            instagramConnectionMethod:
                              type: string
                              enum:
                                - FACEBOOK
                                - INSTAGRAM
                              nullable: true
                            twitterSubType:
                              type: string
                              enum:
                                - none
                                - basic
                                - premium
                                - premium_plus
                              nullable: true
                            isTiktokBusinessAccount:
                              type: boolean
                              nullable: true
                            disconnectedCheckTryAt:
                              type: string
                              format: date-time
                              nullable: true
                            deleteOn:
                              type: string
                              format: date-time
                              nullable: true
                            messagingStatus:
                              default: DISABLED
                              type: string
                              enum:
                                - DISABLED
                                - ENABLED
                                - DISABLE_PENDING
                            messagingStatusUpdatedAt:
                              type: string
                              format: date-time
                              nullable: true
                            messagingLastError:
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
                            deletedAt:
                              type: string
                              format: date-time
                              nullable: true
                          required:
                            - id
                            - type
                            - teamId
                            - createdAt
                            - updatedAt
                      required:
                        - postId
                        - socialAccountId
                        - createdAt
                        - updatedAt
                        - socialAccount
                required:
                  - id
                  - teamId
                  - title
                  - postDate
                  - status
                  - data
                  - retryCount
                  - createdAt
                  - updatedAt
                  - uploads
                  - socialAccounts
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