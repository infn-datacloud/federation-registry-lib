import { IdentityProvider } from "@/app/dashboard/_lib/dbTypes";
import { ExpandMore } from "@mui/icons-material";
import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Card,
  CardContent,
  CardHeader,
  List,
  ListItem,
  Typography,
} from "@mui/material";
import Link from "next/link";

export default function IdentityProvidersCard({
  items,
}: {
  items?: IdentityProvider[];
}) {
  return (
    <Card>
      <CardHeader title="Identity Providers" />
      <CardContent>
        {items
          ? items.map((item, index) => (
              <Accordion
                key={index}
                disableGutters
                elevation={0}
                sx={{ border: "1px solid" }}
              >
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Typography>{item.endpoint.toString()}</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography>
                    Recorded name: {item.relationship?.idp_name}
                  </Typography>
                  <Typography>
                    Communication protocol: {item.relationship?.protocol}
                  </Typography>
                </AccordionDetails>
              </Accordion>
              // <Link href={`/dashboard/identity_providers/${item.uid}`}>
              // </Link>
            ))
          : "No identity providers allowed"}
      </CardContent>
    </Card>
  );
}
