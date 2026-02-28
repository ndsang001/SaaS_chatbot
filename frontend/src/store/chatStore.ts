import { create } from "zustand";
import { sendChat, sendFeedback } from "../api/chat";
import type { SourceItem } from "../api/chat";

type Role = "user" | "assistant";

export type ChatMessage = {
  id: string;
  role: Role;
  text: string;
  turnId?: number;          // only for assistant message
  sources?: SourceItem[];   // only for assistant message
  latencyMs?: number;
  notInKb?: boolean;
};

type State = {
  sessionId: string;
  messages: ChatMessage[];
  isSending: boolean;
  error?: string;

  ask: (question: string) => Promise<void>;
  rate: (turnId: number, rating: "up" | "down", comment?: string) => Promise<void>;
};

function genId() {
  return Math.random().toString(36).slice(2);
}

function getOrCreateSessionId(): string {
  const key = "thesis_chat_session_id";
  const existing = localStorage.getItem(key);
  if (existing) return existing;
  const created = `s_${crypto.randomUUID()}`;
  localStorage.setItem(key, created);
  return created;
}

export const useChatStore = create<State>((set, get) => ({
  sessionId: getOrCreateSessionId(),
  messages: [],
  isSending: false,

  ask: async (question: string) => {
    const q = question.trim();
    if (!q) return;

    const userMsg: ChatMessage = { id: genId(), role: "user", text: q };
    set((s) => ({ messages: [...s.messages, userMsg], isSending: true, error: undefined }));

    try {
      const { sessionId } = get();
      const resp = await sendChat(sessionId, q);

      const asstMsg: ChatMessage = {
        id: genId(),
        role: "assistant",
        text: resp.answer,
        turnId: resp.turn_id,
        sources: resp.sources,
        latencyMs: resp.latency_ms,
        notInKb: resp.not_in_kb,
      };

      set((s) => ({ messages: [...s.messages, asstMsg], isSending: false }));
    } catch (e: any) {
      set({ isSending: false, error: e?.message || "Request failed" });
    }
  },

  rate: async (turnId: number, rating: "up" | "down", comment?: string) => {
    await sendFeedback(turnId, rating, comment);
  },
}));