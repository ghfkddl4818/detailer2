# email-open-tracker

Simple Node/TypeScript tracker designed for Vercel. Drop this folder into your repository and push it; Vercel will automatically detect the serverless function in api/open.ts.

## Files
- api/open.ts – the GET /api/open endpoint. It logs the id, timestamp, client IP, and user-agent before returning a 1×1 transparent PNG.
- tsconfig.json – TypeScript configuration for the API sources.
- vercel.json – tells Vercel to deploy api/open.ts using nodejs20.x.
- package.json – basic scripts for tsc and dependency versions.

## Deploying
1. Run npm install to populate node_modules (Vercel does this automatically).
2. Commit and push this folder to your email-open-tracker repository.
3. Import that repo into Vercel; the GET /api/open route is immediately available.

## Notes
- The function always responds with a cached-transparent PNG so it can be embedded in emails.
- All logging is written to the console, which Vercel exposes via the deployment logs.
