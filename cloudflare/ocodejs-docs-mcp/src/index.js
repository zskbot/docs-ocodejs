const OWNER = "zskbot";
const REPO = "docs-ocodejs";
const BRANCH = "main";
const API = `https://api.github.com/repos/${OWNER}/${REPO}`;
const RAW = `https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}`;

const TOOLS = [
  {
    name: "search_ocodejs_docs",
    description: "Search the public OCode.js documentation hub for relevant pages and matching excerpts. Read-only; searches docs/, README.md, DESIGN_SYSTEM.md, get-started.md and selected project reference files.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Keywords or question to search for" },
        limit: { type: "integer", minimum: 1, maximum: 10, description: "Maximum matching documents (default 5)" }
      },
      required: ["query"]
    }
  },
  {
    name: "list_ocodejs_docs",
    description: "List available documentation paths in zskbot/docs-ocodejs.",
    inputSchema: {
      type: "object",
      properties: {
        prefix: { type: "string", description: "Optional path prefix, e.g. docs/ or specs/" },
        limit: { type: "integer", minimum: 1, maximum: 100, description: "Maximum paths (default 40)" }
      }
    }
  },
  {
    name: "get_ocodejs_document",
    description: "Read one text document from the public zskbot/docs-ocodejs repository by exact path. Supports Markdown, HTML, JSON, YAML, and text files; no writes.",
    inputSchema: {
      type: "object",
      properties: {
        path: { type: "string", description: "Exact repository-relative path, e.g. docs/ROADMAP.md" }
      },
      required: ["path"]
    }
  },
  {
    name: "get_ocodejs_project_overview",
    description: "Return the canonical OCode.js documentation hub overview, roadmap, design system, and repository URL.",
    inputSchema: { type: "object", properties: {} }
  }
];

function json(data, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "access-control-allow-origin": "*",
      "access-control-allow-methods": "GET, POST, OPTIONS",
      "access-control-allow-headers": "content-type, mcp-session-id, mcp-protocol-version, authorization",
      ...extraHeaders
    }
  });
}
function rpc(id, result) {
  return { jsonrpc: "2.0", id, result };
}
function err(id, code, message) {
  return { jsonrpc: "2.0", id, error: { code, message } };
}
function textResult(value) {
  return { content: [{ type: "text", text: typeof value === "string" ? value : JSON.stringify(value, null, 2) }] };
}
function allowedPath(path) {
  if (typeof path !== "string" || !path.trim() || path.startsWith("/") || path.includes("..") || path.includes("\\") || path.length > 240) return false;
  if (!/^[\w./ -]+$/.test(path)) return false;
  if (!/\.(md|mdx|html?|json|ya?ml|txt)$/i.test(path)) return false;
  return !path.startsWith(".github/") && !path.startsWith("_site/") && !path.startsWith("mdn/content/") && !path.startsWith("files/");
}
async function getTree() {
  const response = await fetch(`${API}/git/trees/${BRANCH}?recursive=1`, {
    headers: { "accept": "application/vnd.github+json", "user-agent": "OCodejs-Docs-MCP" }
  });
  if (!response.ok) throw new Error(`GitHub tree API returned HTTP ${response.status}`);
  const data = await response.json();
  return (data.tree || []).filter(item => item.type === "blob" && allowedPath(item.path)).map(item => item.path)
    .filter(path => path.startsWith("docs/") || path.startsWith("specs/") || path.startsWith("content/") ||
      ["README.md", "DESIGN_SYSTEM.md", "get-started.md", "CONTRIBUTING.md", "RemovedPackages.md", "ecosystem/repositories.json"].includes(path));
}
async function getDocument(path) {
  if (!allowedPath(path)) throw new Error("Invalid or unsupported document path.");
  const response = await fetch(`${RAW}/${path.split("/").map(encodeURIComponent).join("/")}`, {
    headers: { "user-agent": "OCodejs-Docs-MCP" }
  });
  if (!response.ok) throw new Error(`Document not found or unavailable (HTTP ${response.status}): ${path}`);
  const content = await response.text();
  return content.length > 30000 ? content.slice(0, 30000) + "\n\n[Truncated at 30,000 characters]" : content;
}
function scorePath(path, terms) {
  const normalized = path.toLowerCase();
  return terms.reduce((score, term) => score + (normalized.includes(term) ? (normalized.split(term).length - 1) * 3 : 0), 0);
}
async function callTool(name, args = {}) {
  if (name === "get_ocodejs_project_overview") {
    const paths = ["README.md", "docs/ECOSYSTEM.md", "docs/ROADMAP.md", "DESIGN_SYSTEM.md"];
    const docs = await Promise.all(paths.map(async path => {
      try { return { path, content: await getDocument(path) }; }
      catch (e) { return { path, error: e.message }; }
    }));
    return textResult({
      repository: "https://github.com/zskbot/docs-ocodejs",
      branch: BRANCH,
      mode: "read-only documentation MCP",
      docs
    });
  }
  if (name === "get_ocodejs_document") {
    const path = String(args.path || "");
    return textResult({ repository: `${OWNER}/${REPO}`, branch: BRANCH, path, content: await getDocument(path) });
  }
  if (name === "list_ocodejs_docs") {
    const prefix = typeof args.prefix === "string" ? args.prefix.slice(0, 120) : "";
    const limit = Math.max(1, Math.min(100, Number.isInteger(args.limit) ? args.limit : 40));
    const paths = (await getTree()).filter(path => !prefix || path.startsWith(prefix)).sort();
    return textResult({ repository: `${OWNER}/${REPO}`, branch: BRANCH, total: paths.length, paths: paths.slice(0, limit) });
  }
  if (name === "search_ocodejs_docs") {
    const query = String(args.query || "").trim().slice(0, 300);
    if (!query) throw new Error("query must not be empty");
    const terms = [...new Set(query.toLowerCase().split(/[^a-z0-9._-]+/).filter(term => term.length > 1))].slice(0, 12);
    const limit = Math.max(1, Math.min(10, Number.isInteger(args.limit) ? args.limit : 5));
    const paths = await getTree();
    const ranked = paths.map(path => ({ path, score: scorePath(path, terms) })).sort((a, b) => b.score - a.score || a.path.localeCompare(b.path));
    const preferred = ranked.filter(x => x.score > 0).slice(0, 8);
    const baseline = ["README.md", "docs/ROADMAP.md", "docs/ECOSYSTEM.md", "docs/SOURCE-AUDIT.md", "DESIGN_SYSTEM.md"];
    const candidates = [...new Set([...preferred.map(x => x.path), ...baseline.filter(p => paths.includes(p))])].slice(0, 12);
    const docs = await Promise.all(candidates.map(async path => {
      try {
        const content = await getDocument(path);
        const lower = content.toLowerCase();
        const hits = terms.reduce((n, term) => n + (lower.split(term).length - 1), 0);
        const pathScore = scorePath(path, terms);
        if (hits === 0 && pathScore === 0) return null;
        const firstHit = Math.max(0, Math.min(...terms.map(term => {
          const i = lower.indexOf(term);
          return i < 0 ? content.length : i;
        })));
        const start = Math.max(0, firstHit - 180);
        return { path, score: hits + pathScore, excerpt: content.slice(start, Math.min(content.length, start + 900)).replace(/\n{3,}/g, "\n\n") };
      } catch { return null; }
    }));
    const results = docs.filter(Boolean).sort((a, b) => b.score - a.score).slice(0, limit);
    return textResult({ query, repository: `https://github.com/${OWNER}/${REPO}`, results, note: "Results are excerpts from the public repository's main branch; verify the linked source for full context." });
  }
  throw new Error(`Unknown tool: ${name}`);
}

export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: {
      "access-control-allow-origin": "*",
      "access-control-allow-methods": "GET, POST, OPTIONS",
      "access-control-allow-headers": "content-type, mcp-session-id, mcp-protocol-version, authorization"
    }});
    if (url.pathname === "/health" || url.pathname === "/") {
      return json({ name: "ocodejs-docs-mcp", status: "ok", transport: "MCP Streamable HTTP", endpoint: "/mcp", repository: `https://github.com/${OWNER}/${REPO}`, tools: TOOLS.map(t => t.name) });
    }
    if (url.pathname !== "/mcp") return json({ error: "Not found", endpoint: "/mcp" }, 404);
    if (request.method !== "POST") return json({ error: "MCP endpoint requires POST JSON-RPC requests." }, 405, { allow: "POST, OPTIONS" });
    let body;
    try { body = await request.json(); } catch { return json(err(null, -32700, "Parse error"), 400); }
    if (Array.isArray(body)) {
      const responses = [];
      for (const item of body) {
        const response = await handleRpc(item);
        if (response) responses.push(response);
      }
      return responses.length ? json(responses) : new Response(null, { status: 202 });
    }
    const response = await handleRpc(body);
    return response ? json(response) : new Response(null, { status: 202 });
  }
};

async function handleRpc(message) {
  const id = Object.prototype.hasOwnProperty.call(message || {}, "id") ? message.id : undefined;
  if (!message || message.jsonrpc !== "2.0" || typeof message.method !== "string") return err(id ?? null, -32600, "Invalid Request");
  if (message.method === "notifications/initialized" || message.method === "notifications/cancelled" || message.method === "notifications/progress") return null;
  if (message.method === "initialize") {
    return rpc(id, {
      protocolVersion: "2025-03-26",
      capabilities: { tools: {} },
      serverInfo: { name: "ocodejs-docs-mcp", version: "1.0.0" },
      instructions: "Read-only MCP server for the public zskbot/docs-ocodejs documentation hub. Use search_ocodejs_docs to find material, get_ocodejs_document to read a file, list_ocodejs_docs to discover paths, and get_ocodejs_project_overview for the project summary."
    });
  }
  if (message.method === "ping") return rpc(id, {});
  if (message.method === "tools/list") return rpc(id, { tools: TOOLS });
  if (message.method === "tools/call") {
    const name = message.params?.name;
    const args = message.params?.arguments || {};
    try { return rpc(id, await callTool(name, args)); }
    catch (e) { return rpc(id, { ...textResult(`Tool error: ${e?.message || "unknown error"}`), isError: true }); }
  }
  return err(id ?? null, -32601, `Method not found: ${message.method}`);
}
