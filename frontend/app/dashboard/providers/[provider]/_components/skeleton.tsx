"use client";

import { Grid, Typography } from "@mui/material";
import LocationCard from "./locationCard";
import IdentityProvidersTable from "./identityProvidersTable";
import ProjectsTable from "./projectsTable";
import FlavorsTable from "./flavorsTable";
import ImagesTable from "./imagesTable";
import ProviderCard from "./providerCard";
import { Provider } from "../../_lib/dbTypes";
import ServicesTable from "./servicesTable";
import PaginatedTable from "@/app/dashboard/_components/paginatedTable";

export default function Skeleton({ item }: { item: Provider }) {
  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Typography variant="h3" align="center">
          {item.name}
        </Typography>
      </Grid>
      <Grid item xs={12} lg={6}>
        <ProviderCard item={item} />
      </Grid>
      <Grid item xs={12} lg={6}>
        <LocationCard item={item.location} />
      </Grid>
      <Grid item xs={12}>
        <PaginatedTable
          title="Identity Providers"
          items={item.identity_providers}
          renderItem={(items, page, rowsPerPage) => (
            <IdentityProvidersTable
              items={items}
              page={page}
              rowsPerPage={rowsPerPage}
            />
          )}
        />
      </Grid>
      <Grid item xs={12}>
        <PaginatedTable
          title="Services"
          items={item.services}
          renderItem={(items, page, rowsPerPage) => (
            <ServicesTable
              items={items}
              page={page}
              rowsPerPage={rowsPerPage}
            />
          )}
        />
      </Grid>
      <Grid item xs={12}>
        <PaginatedTable
          title="Projects"
          items={item.projects}
          renderItem={(items, page, rowsPerPage) => (
            <ProjectsTable
              items={items}
              page={page}
              rowsPerPage={rowsPerPage}
            />
          )}
        />
      </Grid>
      <Grid item xs={12}>
        <PaginatedTable
          title="Flavors"
          items={item.flavors}
          renderItem={(items, page, rowsPerPage) => (
            <FlavorsTable
              items={items}
              page={page}
              rowsPerPage={rowsPerPage}
            />
          )}
        />
      </Grid>
      <Grid item xs={12}>
      <PaginatedTable
          title="Images"
          items={item.images}
          renderItem={(items, page, rowsPerPage) => (
            <ImagesTable
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
