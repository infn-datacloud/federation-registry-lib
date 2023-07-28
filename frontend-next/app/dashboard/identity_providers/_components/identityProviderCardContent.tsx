import { CardContent, Typography } from "@mui/material";
import { IdentityProvider } from "../../_lib/dbTypes";

export default function IdentityProviderCardContent({
  item,
}: {
  item: IdentityProvider;
}) {
  return (
    <CardContent>
      <Typography variant="body2" color="text.secondary">
        Group claim: {item.group_claim}
      </Typography>
    </CardContent>
  );
}
