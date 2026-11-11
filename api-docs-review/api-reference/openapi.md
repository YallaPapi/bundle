> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# OpenAPI

> The full OpenAPI 3.0 spec for the bundle.social API. Try endpoints live, browse them in Swagger UI, or generate a typed client in your own language.

Our API is fully described by an OpenAPI 3.0 spec. You can use it to explore endpoints interactively, generate client libraries, or import into your favorite API tool.

## Try It Live

<Card title="Docs client" icon="webhook" href="/api-reference/client">
  Interactive API explorer embedded right here in the docs. Pass your API key and start making requests.
</Card>

## Swagger UI

<Card title="Swagger" icon="code" href="https://api.bundle.social/swagger">
  The classic Swagger UI. Browse all endpoints, see request/response schemas, and try things out.
</Card>

## Raw Specs

<CardGroup>
  <Card title="JSON spec" icon="code" href="https://api.bundle.social/swagger-json">
    OpenAPI 3.0 spec in JSON format.
  </Card>

  <Card title="YAML spec" icon="code" href="https://api.bundle.social/swagger-yaml">
    OpenAPI 3.0 spec in YAML format.
  </Card>
</CardGroup>

***

## Code Generation

You can use the OpenAPI spec to auto-generate client libraries in pretty much any language. Some popular tools:

| Tool | Command |
| :- | :- |
| [openapi-generator](https://openapi-generator.tech/) | `openapi-generator generate -i https://api.bundle.social/swagger-json -g typescript-fetch -o ./client` |
| [openapi-typescript](https://github.com/openapi-ts/openapi-typescript) | `npx openapi-typescript https://api.bundle.social/swagger-json -o ./types.ts` |
| [Postman](https://www.postman.com/) | Import the JSON URL directly into a collection |
| [Insomnia](https://insomnia.rest/) | File > Import > From URL |

<Tip>
  If you're using TypeScript, we recommend our official [SDK](/api-reference/sdk) instead of generating a client - it has better types, built-in webhook verification, and we actually maintain it.
</Tip>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.