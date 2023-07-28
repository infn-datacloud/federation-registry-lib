import { CardContent, Typography } from "@mui/material";
import { SLA } from "../../_lib/dbTypes";

export default function SLACardContent({ item }: { item: SLA }) {
  return (
    <CardContent>
      <Typography variant="body2" color="text.secondary">
        Involved User Group: {item.user_group?.name}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Involved Project: {item.project?.name}
      </Typography>
    </CardContent>
  );
}
