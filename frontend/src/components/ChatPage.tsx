import { Paper, Box, Alert } from "@mui/material";
import { useChatStore } from "../store/chatStore";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";

export default function ChatPage() {
  const { messages, isSending, error } = useChatStore();

  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Box sx={{ height: 520, overflow: "auto", p: 1, mb: 2 }}>
        {error && <Alert severity="error" sx={{ mb: 1 }}>{error}</Alert>}
        <MessageList messages={messages} isSending={isSending} />
      </Box>
      <MessageInput disabled={isSending} />
    </Paper>
  );
}