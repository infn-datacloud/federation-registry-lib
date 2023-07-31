import { Box, Typography } from "@mui/material";
import { ReactNode } from "react";

export default function Section({
  title,
  hasItems,
  children,
}: {
  title: string;
  hasItems: boolean;
  children: ReactNode;
}) {
  return (
    <Box>
      <Typography variant="h6">{title}</Typography>
      {hasItems ? children : "No " + title}
    </Box>
  );
}
