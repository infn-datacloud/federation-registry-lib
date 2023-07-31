import { Grid } from "@mui/material";
import { Suspense } from "react";
import LocationCardContent from "./_components/locationCardContent";
import Loading from "../locations/loading";
import { getLocations } from "../_lib/crud";
import CardWrapper from "../_components/card/wrapper";
import { Location } from "./_lib/dbTypes";

export default async function Page() {
  const locations: Location[] = await getLocations();
  let children = locations.map((location, index) => (
    <Grid item key={index}>
      <CardWrapper kind="locations" name={location.name} uid={location.uid}>
        <LocationCardContent item={location} />
      </CardWrapper>
    </Grid>
  ));
  return (
    <Suspense fallback={<Loading />}>
      <Grid container spacing={2}>
        {children}
      </Grid>
    </Suspense>
  );
}
