# Goose

Nothing to submit.

- **Extensions directory:** closed to new entries. aaif-goose/goose Discussion #10830 (2026-07-30): "Effective
  immediately, we are no longer accepting new server contributions… Publish your server to the official MCP
  registry using the server.json format. Once our support lands, it will show up in the goose doc pages
  automatically." PR #13399 (merged 2026-11-10) closes requests to add a server automatically.
- **Official MCP Registry:** Palanor is already listed as `com.palanor/mcp` (`mcp/server.json` in Palanor's main
  repository), with the Streamable HTTP remote and its `Authorization` header. Goose will pick it up when its
  registry support lands. As of 2026-11-18 that support had not landed (PR #11934 closed unmerged).
- **Skills:** Goose reads the Agent Skills standard from `~/.agents/skills/`, so the `agentskills` or `goose` copy
  works as is. There is no Goose skill directory to list in.

For documentation, a Goose Desktop install link for the extension. It opens the extension form so the user types
the key; the key is never in the link.

```
goose://extension?url=https%3A%2F%2Fmcp.palanor.com&type=streamable_http&id=palanor&name=Palanor&description=Palanor%20MCP%20server%20(read-only%20public%20data%20lattice)&timeout=300&header=Authorization%3DBearer%2520%3CYOUR_PALANOR_KEY%3E
```
