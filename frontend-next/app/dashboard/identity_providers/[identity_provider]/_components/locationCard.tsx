import { IdentityProvider } from "@/app/dashboard/_lib/dbTypes";
import { Card, CardContent, CardHeader, Typography } from "@mui/material";

export default function IdentityProviderCard({ item }: { item: IdentityProvider }) {
  return (
    <Card>
      <CardHeader title="Details" />
      <CardContent>
        <Typography>Group claim: {item.group_claim}</Typography>
      </CardContent>
    </Card>
  );
}
