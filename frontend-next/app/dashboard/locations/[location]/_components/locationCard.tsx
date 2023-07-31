import { Card, CardContent, CardHeader, Typography } from "@mui/material";
import { LocationBase } from "@/app/dashboard/_lib/dbTypes";

export default function LocationCard({ item }: { item: LocationBase }) {
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
