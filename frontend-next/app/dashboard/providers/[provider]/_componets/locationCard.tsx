import { Location } from "@/app/dashboard/_lib/dbTypes";
import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Box,
  Card,
  CardContent,
  CardHeader,
  Typography,
} from "@mui/material";
import Link from "next/link";
import { ExpandMore } from "@mui/icons-material";

export default function LocationCard({ item }: { item?: Location }) {
  return (
    <Card>
      <CardHeader title="Location" />
      <CardContent>
        {item ? (
          <Accordion elevation={0} sx={{ border: "1px solid" }}>
            <AccordionSummary expandIcon={<ExpandMore />}>
              <Typography>{item.name}</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography>{item.country}</Typography>
              {item.latitude ? <Typography>{item.latitude}</Typography> : null}
              {item.longitude ? (
                <Typography>{item.longitude}</Typography>
              ) : null}
            </AccordionDetails>
            {/* <Link href={`/dashboard/location/${item.uid}`}></Link> */}
          </Accordion>
        ) : (
          "Location not defined"
        )}
      </CardContent>
    </Card>
  );
}
