"use client";

import { Grid, Typography } from "@mui/material";
import LocationCard from "./locationCard";
import ProvidersTable from "./providersTable";
import { Location } from "../../_lib/dbTypes";
import PaginatedTable from "@/app/dashboard/_components/paginatedTable";

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
    </Grid>
  );
}
