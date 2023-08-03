import { SLABase } from "@/app/dashboard/_lib/dbTypes";
import { Card, CardContent, CardHeader, Typography } from "@mui/material";

export default function SLACard({ item }: { item: SLABase }) {
  return (
    <Card>
      <CardHeader title="Details" />
      <CardContent>
        <Typography>Start date: {item.start_date.toISOString()}</Typography>
        <Typography>End date: {item.start_date.toISOString()}</Typography>
        <Typography>Document: {item.document_uuid}</Typography>
      </CardContent>
    </Card>
  );
}
