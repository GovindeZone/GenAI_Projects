import { createServerFn } from "@tanstack/react-start";
import { getRequest } from "@tanstack/react-start/server";
import { z } from "zod";

const contactSchema = z.object({
  name: z.string().trim().min(1, "Name is required").max(100),
  company: z.string().trim().max(150).optional().default(""),
  email: z.string().trim().email("Invalid email").max(255),
  phone: z.string().trim().max(50).optional().default(""),
  message: z.string().trim().min(1, "Message is required").max(2000),
  // anti-bot fields (client-supplied, validated server-side)
  website: z.string().max(0).optional().default(""), // honeypot — must be empty
  ts: z.number().int().nonnegative().optional(),
});

function escapeHtml(s: string) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

const ALLOWED_HOSTS = new Set([
  "aibro.sbs",
  "www.aibro.sbs",
  "ai-bro-web-spark.lovable.app",
]);
const ALLOWED_HOST_SUFFIXES = [".lovable.app", ".lovable.dev"];

function hostAllowed(urlStr: string | null): boolean {
  if (!urlStr) return false;
  try {
    const host = new URL(urlStr).host.toLowerCase();
    if (ALLOWED_HOSTS.has(host)) return true;
    if (host === "localhost" || host.startsWith("localhost:") || host.startsWith("127.0.0.1")) return true;
    return ALLOWED_HOST_SUFFIXES.some((s) => host.endsWith(s));
  } catch {
    return false;
  }
}

// Simple in-memory per-IP rate limiter (best-effort; per worker instance).
const RATE_WINDOW_MS = 60_000;
const RATE_MAX = 3;
const ipHits = new Map<string, number[]>();

function rateLimited(ip: string): boolean {
  const now = Date.now();
  const arr = (ipHits.get(ip) || []).filter((t) => now - t < RATE_WINDOW_MS);
  arr.push(now);
  ipHits.set(ip, arr);
  if (ipHits.size > 2000) {
    // prune
    for (const [k, v] of ipHits) {
      if (!v.some((t) => now - t < RATE_WINDOW_MS)) ipHits.delete(k);
    }
  }
  return arr.length > RATE_MAX;
}

export const submitContact = createServerFn({ method: "POST" })
  .inputValidator((data: unknown) => contactSchema.parse(data))
  .handler(async ({ data }) => {
    const req = getRequest();

    // 1) Origin/Referer allowlist — block cross-origin and direct curl abuse
    const origin = req.headers.get("origin");
    const referer = req.headers.get("referer");
    if (!hostAllowed(origin) && !hostAllowed(referer)) {
      throw new Error("Forbidden");
    }

    // 2) Honeypot — bots usually fill hidden fields
    if (data.website && data.website.length > 0) {
      // Pretend success to avoid signaling detection
      return { ok: true as const };
    }

    // 3) Minimum form fill time (>= 2s) — bots submit instantly
    if (typeof data.ts === "number") {
      const elapsed = Date.now() - data.ts;
      if (elapsed >= 0 && elapsed < 2000) {
        return { ok: true as const };
      }
    }

    // 4) Per-IP rate limit
    const ip =
      req.headers.get("cf-connecting-ip") ||
      req.headers.get("x-forwarded-for")?.split(",")[0].trim() ||
      "unknown";
    if (rateLimited(ip)) {
      throw new Error("Too many requests. Please try again in a minute.");
    }

    const nodemailer = (await import("nodemailer")).default;

    const host = process.env.SMTP_HOST!;
    const port = Number(process.env.SMTP_PORT || "465");
    const user = process.env.SMTP_USER!;
    const pass = process.env.SMTP_PASSWORD!;
    const from = process.env.SMTP_FROM || `AI Bro <${user}>`;
    const to = process.env.INQUIRIES_TO || user;

    const transporter = nodemailer.createTransport({
      host,
      port,
      secure: port === 465,
      auth: { user, pass },
    });

    const safe = {
      name: escapeHtml(data.name),
      company: escapeHtml(data.company || "—"),
      email: escapeHtml(data.email),
      phone: escapeHtml(data.phone || "—"),
      message: escapeHtml(data.message).replace(/\n/g, "<br/>"),
    };

    const adminHtml = `
      <div style="font-family:Arial,sans-serif;background:#0b0b0f;padding:24px;color:#f5f5f5">
        <div style="max-width:600px;margin:0 auto;background:#14141b;border:1px solid #2a2a36;border-radius:12px;overflow:hidden">
          <div style="background:linear-gradient(135deg,#facc15,#f59e0b);padding:20px 24px;color:#111">
            <h2 style="margin:0;font-size:20px">New Enquiry — AI Bro</h2>
            <p style="margin:4px 0 0;font-size:13px;opacity:.8">A new lead just submitted the contact form</p>
          </div>
          <div style="padding:24px;font-size:14px;line-height:1.6">
            <p><strong>Name:</strong> ${safe.name}</p>
            <p><strong>Company:</strong> ${safe.company}</p>
            <p><strong>Email:</strong> <a href="mailto:${safe.email}" style="color:#facc15">${safe.email}</a></p>
            <p><strong>Phone:</strong> ${safe.phone}</p>
            <p style="margin-top:16px"><strong>Message / Pain Point:</strong></p>
            <div style="background:#0b0b0f;border:1px solid #2a2a36;border-radius:8px;padding:14px;margin-top:6px">${safe.message}</div>
          </div>
          <div style="padding:14px 24px;background:#0b0b0f;font-size:12px;color:#888;border-top:1px solid #2a2a36">
            Sent automatically from aibro.sbs
          </div>
        </div>
      </div>`;

    const customerHtml = `
      <div style="font-family:Arial,sans-serif;background:#0b0b0f;padding:24px;color:#f5f5f5">
        <div style="max-width:600px;margin:0 auto;background:#14141b;border:1px solid #2a2a36;border-radius:12px;overflow:hidden">
          <div style="background:linear-gradient(135deg,#facc15,#f59e0b);padding:24px;color:#111;text-align:center">
            <h1 style="margin:0;font-size:24px">Thanks for reaching out, ${safe.name}! 🤖</h1>
            <p style="margin:6px 0 0;font-size:14px">Your AI Bro has received your enquiry</p>
          </div>
          <div style="padding:24px;font-size:14px;line-height:1.7">
            <p>Hi ${safe.name},</p>
            <p>Thanks for connecting with <strong>AI Bro Solutions</strong>. We've received your message and our team will get back to you within <strong>1 business day</strong> with the next steps.</p>
            <p style="margin-top:18px"><strong>Here's a copy of what you sent us:</strong></p>
            <div style="background:#0b0b0f;border-left:3px solid #facc15;padding:12px 16px;margin-top:6px;border-radius:6px">${safe.message}</div>
            <p style="margin-top:22px">In the meantime, feel free to reply to this email if you'd like to add anything.</p>
            <p style="margin-top:22px">Warm regards,<br/><strong>Team AI Bro</strong><br/><span style="color:#888;font-size:12px">A Generative AI Architecture &amp; Automation Company</span></p>
          </div>
          <div style="padding:14px 24px;background:#0b0b0f;font-size:12px;color:#888;border-top:1px solid #2a2a36;text-align:center">
            AI Bro Solutions · Chennai, India · <a href="https://aibro.sbs" style="color:#facc15">aibro.sbs</a>
          </div>
        </div>
      </div>`;

    await transporter.sendMail({
      from,
      to,
      replyTo: data.email,
      subject: `New AI Bro enquiry from ${data.name}${data.company ? ` (${data.company})` : ""}`,
      html: adminHtml,
    });

    await transporter.sendMail({
      from,
      to: data.email,
      subject: "We've received your enquiry — AI Bro",
      html: customerHtml,
    }).catch((err) => {
      console.error("Customer ack email failed:", err);
    });

    return { ok: true as const };
  });
