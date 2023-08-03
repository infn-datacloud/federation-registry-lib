"use client";

import { Grid, Typography } from "@mui/material";
import IdentityProviderCard from "./identityProviderCard";
import ProvidersTable from "./providersTable";
import UserGroupsTable from "./userGroupsTable";
import { IdentityProvider } from "../../_lib/dbTypes";
import PaginatedTable from "@/app/dashboard/_components/paginatedTable";

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
        <PaginatedTable
          title="Providers"
          items={item.providers}
          renderItem={(items, page, rowsPerPage) => (
            <ProvidersTable
              items={items}
              page={page}
              rowsPerPage={rowsPerPage}
            />
          )}
        />
      </Grid>
      <Grid item xs={12}>
        <PaginatedTable
          title="User Groups"
          items={item.user_groups}
          renderItem={(items, page, rowsPerPage) => (
            <UserGroupsTable
              items={items}
              page={page}
              rowsPerPage={rowsPerPage}
            />
          )}
        />
      </Grid>
    </Grid>
  );
}
