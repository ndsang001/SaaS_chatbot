import { Container, Typography, Box } from "@mui/material";
import ChatPage from "./components/ChatPage";

export default function App() {
  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Box sx={{ mb: 2 }}>
        <Typography variant="h5" fontWeight={700}>
          SaaS Support Chatbot (RAG Demo)
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Answers are grounded in provided FAQ/help articles and include sources + latency.
        </Typography>
      </Box>
      <ChatPage />
    </Container>
  );
}