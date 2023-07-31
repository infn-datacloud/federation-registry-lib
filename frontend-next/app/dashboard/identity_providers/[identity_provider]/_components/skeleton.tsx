import { Grid, Typography } from "@mui/material";
import { IdentityProvider } from "@/app/dashboard/_lib/dbTypes";
import Section from "@/app/dashboard/_components/section";
import IdentityProviderCard from "./locationCard";
import ProvidersTable from "./providersTable";
import UserGroupsTable from "./userGroupsTable";

export default function IdentityProviderSkeleton({
  item,
}: {
  item: IdentityProvider;
}) {
  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Typography variant="h3" align="center">
          {item.endpoint.toString()}
        </Typography>
      </Grid>
      <Grid item xs={12}>
        <IdentityProviderCard item={item} />
      </Grid>
      <Grid item xs={12}>
        <Section
          title="Providers"
          hasItems={item.providers !== undefined && item.providers.length > 0}
        >
          <ProvidersTable items={item.providers} />
        </Section>
      </Grid>
      <Grid item xs={12}>
        <Section
          title="User Groups"
          hasItems={
            item.user_groups !== undefined && item.user_groups.length > 0
          }
        >
          <UserGroupsTable items={item.user_groups} />
        </Section>
      </Grid>
    </Grid>
  );
}
