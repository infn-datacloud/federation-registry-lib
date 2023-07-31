import { Grid, Typography } from "@mui/material";
import { Provider } from "@/app/dashboard/_lib/dbTypes";
import LocationCard from "./locationCard";
import IdentityProvidersTable from "./identityProvidersTable";
import ServicesTable from "./servicesTable";
import ProjectsTable from "./projectsTable";
import FlavorsTable from "./flavorsTable";
import ImagesTable from "./imagesTable";
import ProviderSection from "./providerSection";
import ProviderCard from "./providerCard";

export default function ProviderSkeleton({ provider }: { provider: Provider }) {
  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Typography variant="h3" align="center">
          {provider.name}
        </Typography>
      </Grid>
      <Grid item xs={12} lg={6}>
        <ProviderCard item={provider} />
      </Grid>
      <Grid item xs={12} lg={6}>
        <LocationCard item={provider.location} />
      </Grid>
      <Grid item xs={12}>
        <ProviderSection
          title="Identity Providers"
          hasItems={
            provider.identity_providers !== undefined &&
            provider.identity_providers.length > 0
          }
        >
          <IdentityProvidersTable items={provider.identity_providers} />
        </ProviderSection>
      </Grid>
      <Grid item xs={12}>
        <ProviderSection
          title="Services"
          hasItems={
            provider.services !== undefined && provider.services.length > 0
          }
        >
          <ServicesTable items={provider.services} />
        </ProviderSection>
      </Grid>
      <Grid item xs={12}>
        <ProviderSection
          title="Projects"
          hasItems={
            provider.projects !== undefined && provider.projects.length > 0
          }
        >
          <ProjectsTable items={provider.projects} />
        </ProviderSection>
      </Grid>
      <Grid item xs={12}>
        <ProviderSection
          title="Flavors"
          hasItems={
            provider.flavors !== undefined && provider.flavors.length > 0
          }
        >
          <FlavorsTable items={provider.flavors} />
        </ProviderSection>
      </Grid>
      <Grid item xs={12}>
        <ProviderSection
          title="Images"
          hasItems={provider.images !== undefined && provider.images.length > 0}
        >
          <ImagesTable items={provider.images} />
        </ProviderSection>
      </Grid>
    </Grid>
  );
}
