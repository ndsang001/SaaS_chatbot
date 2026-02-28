import { api } from "./client";

export type SourceItem = {
  chunk_id: string;
  title: string;
  section?: string | null;
  source?: string | null;
};

export type ChatResponse = {
  turn_id: number;
  answer: string;
  sources: SourceItem[];
  latency_ms: number;
  not_in_kb: boolean;
};

export async function sendChat(sessionId: string, question: string): Promise<ChatResponse> {
  const res = await api.post<ChatResponse>("/chat", {
    session_id: sessionId,
    question,
  });
  return res.data;
}

export async function sendFeedback(turnId: number, rating: "up" | "down", comment?: string) {
  await api.post("/feedback", { turn_id: turnId, rating, comment: comment || null });
}