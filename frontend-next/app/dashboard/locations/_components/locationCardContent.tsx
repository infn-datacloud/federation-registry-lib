import { CardContent, Typography } from "@mui/material";
import { Location } from "../../_lib/dbTypes";

export default function LocationCardContent({ item }: { item: Location }) {
  return (
    <CardContent>
      <Typography variant="body2" color="text.secondary">
        {item.country}
      </Typography>
    </CardContent>
  );
}
