import { Provider } from "@/app/dashboard/_lib/dbTypes";
import { Card, CardContent, CardHeader, Typography } from "@mui/material";

export default function ProviderCard({ item }: { item: Provider }) {
  return (
    <Card>
      <CardHeader title="Details" />
      <CardContent>
        <Typography>{item.is_public ? "Public" : "Private"}</Typography>
        <Typography>Contacts: {item.support_emails.join(", ")}</Typography>
      </CardContent>
    </Card>
  );
}
