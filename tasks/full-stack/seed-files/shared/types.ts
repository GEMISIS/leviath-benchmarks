/**
 * Shared type definitions for notification system
 * IMPORTANT: Both frontend and backend must use these exact types
 */

export enum NotificationType {
  COMMENT = 'comment',
  MENTION = 'mention',
  SYSTEM = 'system',
  SECURITY = 'security',
}

export enum NotificationPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent',
}

export interface Notification {
  id: string;
  user_id: number;
  type: NotificationType;
  priority: NotificationPriority;
  title: string;
  message: string;
  link?: string;
  read: boolean;
  created_at: string; // ISO 8601
  metadata?: Record<string, any>;
}

export interface NotificationPreferences {
  user_id: number;
  email_enabled: boolean;
  push_enabled: boolean;
  enabled_types: NotificationType[];
  quiet_hours: {
    start: string; // HH:MM format
    end: string;   // HH:MM format
    timezone: string;
  } | null;
}

export interface WebSocketMessage {
  type: 'notification' | 'notification_read' | 'ping' | 'pong';
  payload: any;
  timestamp: string; // ISO 8601
}
