import { Card, CardContent, CardHeader, Typography } from "@mui/material";
import { IdentityProviderBase } from "@/app/dashboard/_lib/dbTypes";

export default function IdentityProviderCard({
  item,
}: {
  item: IdentityProviderBase;
}) {
  return (
    <Card>
      <CardHeader title="Details" />
      <CardContent>
        <Typography>Group claim: {item.group_claim}</Typography>
      </CardContent>
    </Card>
  );
}
