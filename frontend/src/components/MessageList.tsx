import { Box, Typography, Chip, Divider } from "@mui/material";
import type { ChatMessage } from "../store/chatStore";
import SourcesPanel from "./SourcesPanel";
import FeedbackButtons from "./FeedbackButtons";

export default function MessageList({ messages, isSending }: { messages: ChatMessage[]; isSending: boolean }) {
  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 1.5 }}>
      {messages.length === 0 && (
        <Typography variant="body2" color="text.secondary">
          Try: “How long does the password reset link last?”
        </Typography>
      )}

      {messages.map((m) => (
        <Box key={m.id}>
          <Box sx={{ display: "flex", justifyContent: m.role === "user" ? "flex-end" : "flex-start" }}>
            <Box
              sx={{
                maxWidth: "85%",
                p: 1.25,
                borderRadius: 2,
                bgcolor: m.role === "user" ? "primary.main" : "grey.100",
                color: m.role === "user" ? "primary.contrastText" : "text.primary",
              }}
            >
              <Typography variant="body2" sx={{ whiteSpace: "pre-wrap" }}>
                {m.text}
              </Typography>

              {m.role === "assistant" && (
                <Box sx={{ mt: 1, display: "flex", gap: 1, flexWrap: "wrap", alignItems: "center" }}>
                  {typeof m.latencyMs === "number" && <Chip size="small" label={`${m.latencyMs} ms`} />}
                  {m.notInKb && <Chip size="small" color="warning" label="Not in KB" />}
                </Box>
              )}
            </Box>
          </Box>

          {m.role === "assistant" && (
            <Box sx={{ mt: 1, ml: 0 }}>
              <SourcesPanel sources={m.sources || []} />
              {m.turnId && <FeedbackButtons turnId={m.turnId} />}
              <Divider sx={{ mt: 1 }} />
            </Box>
          )}
        </Box>
      ))}

      {isSending && (
        <Typography variant="body2" color="text.secondary">
          Assistant is typing…
        </Typography>
      )}
    </Box>
  );
}