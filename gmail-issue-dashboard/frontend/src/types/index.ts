export type Category = 'New Ticket' | 'In-Progress' | 'Resolved' | 'Escalation';
export type Priority = 'Critical' | 'High' | 'Medium' | 'Low';
export type Sentiment = 'Positive' | 'Neutral' | 'Negative' | 'Urgent';

export interface EmailAnalysis {
  isIssueRelated: boolean;
  category: Category;
  priority: Priority;
  summary: string;
  keyPoints: string[];
  suggestedAction: string;
  sentiment: Sentiment;
  topic: string;
}

export interface Email {
  id: string;
  threadId: string;
  messageId: string;
  subject: string;
  from: string;
  senderName: string;
  senderEmail: string;
  to: string;
  date: string;
  snippet: string;
  body: string;
  labelIds: string[];
  analysis: EmailAnalysis;
  analyzed: boolean;
  assignedTo?: string;
}

export interface DashboardStats {
  total: number;
  newTicket: number;
  inProgress: number;
  resolved: number;
  escalation: number;
}

export interface AppConfig {
  receiverEmail: string;
  assignerEmail: string;
  escalationEmail: string;
  companyName: string;
}

export interface FilterState {
  category: string;
  priority: string;
  sender: string;
  keyword: string;
  dateFrom: string;
  dateTo: string;
}
