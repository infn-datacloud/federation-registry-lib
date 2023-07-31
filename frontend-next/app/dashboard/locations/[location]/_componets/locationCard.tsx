import { Location } from "@/app/dashboard/_lib/dbTypes";
import { Card, CardContent, CardHeader, Typography } from "@mui/material";

export default function LocationCard({ item }: { item: Location }) {
  return (
    <Card>
      <CardHeader title="Details" />
      <CardContent>
        <Typography>{item.country}</Typography>
        <Typography>{item.latitude}</Typography>
        <Typography>{item.longitude}</Typography>
      </CardContent>
    </Card>
  );
}
