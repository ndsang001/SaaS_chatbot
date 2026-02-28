import { useState } from "react";
import { Box, TextField, Button } from "@mui/material";
import { useChatStore } from "../store/chatStore";

export default function MessageInput({ disabled }: { disabled: boolean }) {
  const [value, setValue] = useState("");
  const ask = useChatStore((s) => s.ask);

  return (
    <Box sx={{ display: "flex", gap: 1 }}>
      <TextField
        fullWidth
        size="small"
        placeholder="Ask a support question…"
        value={value}
        disabled={disabled}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            ask(value);
            setValue("");
          }
        }}
      />
      <Button
        variant="contained"
        disabled={disabled || !value.trim()}
        onClick={() => {
          ask(value);
          setValue("");
        }}
      >
        Send
      </Button>
    </Box>
  );
}