import { CardContent, Typography } from "@mui/material";
import { Provider } from "../../_lib/dbTypes";

export default function ProviderCardContent({ item }: { item: Provider }) {
  return (
    <CardContent>
      <Typography variant="body2" color="text.secondary">
        {item.is_public ? "Public" : "Private"} provider
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Country: {item.location.country}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Contacts: {item.support_emails.join(", ")}
      </Typography>
    </CardContent>
  );
}
