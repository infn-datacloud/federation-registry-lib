import { Grid, Stack } from "@mui/material";
import LocationCard from "./locationCard";
import IdentityProvidersCard from "./identityProvidersCard";
import ServicesCard from "./servicesCard";
import ProjectsCard from "./projectsCard";
import FlavorsCard from "./flavorsCard";
import ImagesCard from "./imagesCard";
import { Provider } from "@/app/dashboard/_lib/dbTypes";

export default function ProviderSkeleton({ provider }: { provider: Provider }) {
  return (
    <Grid container spacing={4}>
      <Grid item xs={4}>
        <Stack spacing={2}>
          <LocationCard item={provider.location} />
          <ProjectsCard items={provider.projects} />
        </Stack>
      </Grid>
      <Grid item xs={4}>
        <Stack spacing={2}>
          <IdentityProvidersCard items={provider.identity_providers} />
          <FlavorsCard items={provider.flavors} />
        </Stack>
      </Grid>
      <Grid item xs={4}>
        <Stack spacing={2}>
          <ServicesCard items={provider.services} />
          <ImagesCard items={provider.images} />
        </Stack>
      </Grid>
    </Grid>
  );
}
