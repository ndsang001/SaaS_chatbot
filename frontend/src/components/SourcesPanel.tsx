import { Box, Typography, List, ListItem, ListItemText } from "@mui/material";
import type { SourceItem } from "../api/chat";

export default function SourcesPanel({ sources }: { sources: SourceItem[] }) {
  if (!sources.length) return null;

  return (
    <Box sx={{ mt: 1 }}>
      <Typography variant="caption" color="text.secondary">
        Sources
      </Typography>
      <List dense sx={{ py: 0 }}>
        {sources.map((s) => (
          <ListItem key={s.chunk_id} sx={{ py: 0 }}>
            <ListItemText
              primaryTypographyProps={{ variant: "body2" }}
              secondaryTypographyProps={{ variant: "caption" }}
              primary={`${s.title} [${s.chunk_id}]`}
              secondary={s.source || ""}
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );
}