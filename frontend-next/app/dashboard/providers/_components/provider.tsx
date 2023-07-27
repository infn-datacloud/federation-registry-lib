import {
  Card,
  CardActionArea,
  CardContent,
  CardHeader,
  CardMedia,
  Typography,
} from "@mui/material";
import Link from "next/link";
import { cardMaxWidth, cardMediaHeight } from "../_lib/constants";
import { Provider } from "../[provider]/_lib/types";

const cardMediaImage =
  "https://www.datanami.com/wp-content/uploads/2019/06/cloud_digital_shutterstock_Phonlamai-Photo-300x200.jpg";

export default function ProviderCard({ item }: { item: Provider }) {
  return (
    <Link href={`/dashboard/providers/${item.uid}`}>
      <Card sx={{ maxWidth: cardMaxWidth }}>
        <CardActionArea>
          <CardHeader title={item.name} />
          <CardMedia
            component="img"
            height={cardMediaHeight}
            image={cardMediaImage}
            alt="Cloud provider image"
          />
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
        </CardActionArea>
      </Card>
    </Link>
  );
}
