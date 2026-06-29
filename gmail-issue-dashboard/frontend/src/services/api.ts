import axios from 'axios';
import type { AppConfig, FilterState, Email, EmailAnalysis } from '../types';

const api = axios.create({ baseURL: '/api' });

export const gmailApi = {
  getAuthUrl: () => api.get<{ url: string }>('/gmail/auth-url'),
  getStatus: (email: string) =>
    api.get<{ connected: boolean; email: string }>('/gmail/status', { params: { email } }),
  disconnect: (email: string) => api.post('/gmail/disconnect', { email }),
};

export const emailsApi = {
  fetch: (config: AppConfig & Partial<FilterState> & { maxResults?: number }) =>
    api.post<{ emails: Omit<Email, 'analysis' | 'analyzed'>[]; count: number }>('/emails/fetch', {
      receiverEmail: config.receiverEmail,
      senderFilter: config.sender,
      dateFrom: config.dateFrom,
      dateTo: config.dateTo,
      keyword: config.keyword,
      maxResults: config.maxResults || 50,
    }),
  send: (payload: {
    receiverEmail: string;
    to: string;
    subject: string;
    body: string;
    threadId?: string;
  }) => api.post<{ success: boolean; messageId: string }>('/emails/send', payload),
};

export const analyzeApi = {
  analyzeEmails: (emails: object[]) =>
    api.post<{ emails: Email[]; stats: { total: number; newTicket: number; inProgress: number; resolved: number; escalation: number } }>(
      '/analyze/emails',
      { emails }
    ),
  generateReply: (payload: {
    email: Email;
    analysis: EmailAnalysis;
    companyName: string;
    assignerEmail: string;
    category: string;
  }) => api.post<{ reply: string }>('/analyze/generate-reply', payload),
  generateEscalation: (payload: {
    email: Email;
    analysis: EmailAnalysis;
    companyName: string;
    escalationEmail: string;
    assignerEmail: string;
  }) => api.post<{ escalationDraft: string }>('/analyze/generate-escalation', payload),
};
