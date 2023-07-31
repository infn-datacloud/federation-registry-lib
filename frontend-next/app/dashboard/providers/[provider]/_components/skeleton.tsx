import { Grid, Typography } from "@mui/material";
import Section from "@/app/dashboard/_components/section";
import LocationCard from "./locationCard";
import IdentityProvidersTable from "./identityProvidersTable";
import ServicesTable from "./servicesTable";
import ProjectsTable from "./projectsTable";
import FlavorsTable from "./flavorsTable";
import ImagesTable from "./imagesTable";
import ProviderCard from "./providerCard";
import { Provider } from "../../_lib/dbTypes";

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
        <Section
          title="Identity Providers"
          hasItems={item.identity_providers.length > 0}
        >
          <IdentityProvidersTable items={item.identity_providers} />
        </Section>
      </Grid>
      <Grid item xs={12}>
        <Section title="Services" hasItems={item.services.length > 0}>
          <ServicesTable items={item.services} />
        </Section>
      </Grid>
      <Grid item xs={12}>
        <Section title="Projects" hasItems={item.projects.length > 0}>
          <ProjectsTable items={item.projects} />
        </Section>
      </Grid>
      <Grid item xs={12}>
        <Section title="Flavors" hasItems={item.flavors.length > 0}>
          <FlavorsTable items={item.flavors} />
        </Section>
      </Grid>
      <Grid item xs={12}>
        <Section title="Images" hasItems={item.images.length > 0}>
          <ImagesTable items={item.images} />
        </Section>
      </Grid>
    </Grid>
  );
}
