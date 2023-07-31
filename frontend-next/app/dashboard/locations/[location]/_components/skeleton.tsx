import { Grid, Typography } from "@mui/material";
import Section from "@/app/dashboard/_components/section";
import LocationCard from "./locationCard";
import ProvidersTable from "./providersTable";
import { Location } from "../_lib/dbTypes";

export default function LocationSkeleton({ item }: { item: Location }) {
  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Typography variant="h3" align="center">
          {item.name}
        </Typography>
      </Grid>
      <Grid item xs={12}>
        <LocationCard item={item} />
      </Grid>
      <Grid item xs={12}>
        <Section
          title="Providers"
          hasItems={item.providers !== undefined && item.providers.length > 0}
        >
          <ProvidersTable items={item.providers} />
        </Section>
      </Grid>
    </Grid>
  );
}
