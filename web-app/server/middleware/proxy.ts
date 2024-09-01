import { createProxyMiddleware } from 'http-proxy-middleware';
import { defineEventHandler, H3Event } from 'h3';

// Get the target URL from the environment variable
const target = process.env.API_URL || 'http://localhost:8000';

export default defineEventHandler((event: H3Event) => {
  // On vérifie si l'URL commence par /api
  if (event.node.req.url?.startsWith('/api')) {
    const proxy = createProxyMiddleware({
      target: target,
      pathRewrite: { '^/api': '' },
      changeOrigin: true,
      cookieDomainRewrite: {"*": ""},
    });

    return new Promise<void>((resolve, reject) => {
      proxy(event.node.req, event.node.res, (err) => {
        if (err) {
          reject(err);
        } else {
          resolve();
        }
      });
    });
  }

  // Si l'URL ne correspond pas à /api, on ne fait rien et on retourne directement
  return;
});
