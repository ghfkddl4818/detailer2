import type { VercelRequest, VercelResponse } from '@vercel/node';

const transparentPixel = Buffer.from(
  'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO8FlEsAAAAASUVORK5CYII=',
  'base64'
);

const extractId = (value: string | string[] | undefined): string => {
  if (!value) {
    return 'missing-id';
  }

  if (Array.isArray(value)) {
    return value[0] ?? 'missing-id';
  }

  return value;
};

const getClientIp = (req: VercelRequest): string => {
  const headerValue = req.headers['x-forwarded-for'];

  if (typeof headerValue === 'string' && headerValue.length > 0) {
    return headerValue.split(',')[0].trim();
  }

  if (Array.isArray(headerValue) && headerValue.length > 0) {
    return headerValue[0].split(',')[0].trim();
  }

  return req.socket?.remoteAddress ?? 'unknown';
};

const sendPixel = (res: VercelResponse): void => {
  res.setHeader('Content-Type', 'image/png');
  res.setHeader('Content-Length', transparentPixel.length.toString());
  res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
  res.setHeader('Expires', '0');
  res.setHeader('Content-Disposition', 'inline; filename="pixel.png"');
  res.statusCode = 200;
  res.end(transparentPixel);
};

const handler = (req: VercelRequest, res: VercelResponse): void => {
  const id = extractId(req.query.id);
  const now = new Date().toISOString();
  const clientIp = getClientIp(req);
  const userAgent = req.headers['user-agent'] ?? 'unknown';

  console.log(
    JSON.stringify({
      event: 'email-open',
      id,
      requestedAt: now,
      ip: clientIp,
      userAgent,
      method: req.method
    })
  );

  sendPixel(res);
};

export default handler;
