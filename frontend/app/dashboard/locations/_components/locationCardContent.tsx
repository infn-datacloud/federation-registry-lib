import { CardContent, Typography } from "@mui/material";
import { LocationBase } from "../../_lib/dbTypes";

export default function LocationCardContent({ item }: { item: LocationBase }) {
  return (
    <CardContent>
      <Typography variant="body2" color="text.secondary">
        {item.country}
      </Typography>
    </CardContent>
  );
}
