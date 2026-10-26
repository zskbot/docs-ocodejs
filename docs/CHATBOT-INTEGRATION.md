# OCode.js chatbot integration

## Architecture

- The documentation hub remains a static GitHub Pages site.
- The floating assistant launcher in `index.html` opens the standalone `chatbot.html` page.
- The standalone page embeds the separately hosted Next.js application in an iframe once the public URL is configured.
- The source application is [OCodejs/chatbot](https://github.com/OCodejs/chatbot). It is not copied into this repository because its API routes, authentication, streaming responses, database, and storage require a server runtime.

## Connect the Vercel deployment

1. In Vercel, import the Git repository `OCodejs/chatbot` as its own project.
2. Use the repository root as the project root and let Vercel detect Next.js. The repository's build script runs database migrations before `next build`, so required database configuration must exist before a successful build.
3. Configure required environment variables in Vercel, not in Git. The checked-in `.env.example` identifies `AUTH_SECRET`, `POSTGRES_URL`, `REDIS_URL`, and related AI Gateway/Blob configuration. Add credentials only for services that are actually connected and enabled.
4. Confirm a successful deployment and copy its public HTTPS URL.
5. Set `window.OCODEJS_CHATBOT_URL` in `chatbot-config.js` to that verified URL.
6. Redeploy/publish the documentation site and test the floating launcher, standalone page, sign-in flow, and a streamed chat response.

## Security and limitations

- Never commit populated `.env` files or secrets.
- Keep server-only values out of any `NEXT_PUBLIC_*` variable.
- A public URL alone does not make the chatbot functional; authentication, database, Redis, and any required storage/provider integration must be configured.
- The Vercel connector returned HTTP 403 when asked to create the `ocodejs-chatbot` project for the currently connected team. Consequently, there is no verified deployment URL yet and `chatbot-config.js` deliberately remains unset.
- Existing documentation content is preserved; this integration only adds launcher/page/configuration documentation.
