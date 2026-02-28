import { useState } from "react";
import { Box, IconButton, Tooltip, TextField, Button } from "@mui/material";
import ThumbUpAltOutlinedIcon from "@mui/icons-material/ThumbUpAltOutlined";
import ThumbDownAltOutlinedIcon from "@mui/icons-material/ThumbDownAltOutlined";
import { useChatStore } from "../store/chatStore";

export default function FeedbackButtons({ turnId }: { turnId: number }) {
  const rate = useChatStore((s) => s.rate);
  const [open, setOpen] = useState(false);
  const [comment, setComment] = useState("");

  return (
    <Box sx={{ mt: 0.5, display: "flex", alignItems: "center", gap: 1, flexWrap: "wrap" }}>
      <Tooltip title="Helpful">
        <IconButton size="small" onClick={() => rate(turnId, "up")}>
          <ThumbUpAltOutlinedIcon fontSize="small" />
        </IconButton>
      </Tooltip>
      <Tooltip title="Not helpful (optional comment)">
        <IconButton size="small" onClick={() => setOpen((v) => !v)}>
          <ThumbDownAltOutlinedIcon fontSize="small" />
        </IconButton>
      </Tooltip>

      {open && (
        <>
          <TextField
            size="small"
            placeholder="Optional: what was missing?"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
          />
          <Button
            size="small"
            variant="outlined"
            onClick={async () => {
              await rate(turnId, "down", comment);
              setOpen(false);
              setComment("");
            }}
          >
            Submit
          </Button>
        </>
      )}
    </Box>
  );
}