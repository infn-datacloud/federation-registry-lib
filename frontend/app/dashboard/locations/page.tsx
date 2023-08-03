"use client";

import { Grid } from "@mui/material";
import LocationCardContent from "./_components/locationCardContent";
import Loading from "./loading";
import { useLocations } from "../_lib/crud";
import CardWrapper from "../_components/card/wrapper";
import { Location } from "./_lib/dbTypes";

export default function Page() {
  const { locations } = useLocations();
  const children = locations ? (
    locations.map((location: Location, index: number) => (
      <Grid item key={index}>
        <CardWrapper kind="locations" name={location.name} uid={location.uid}>
          <LocationCardContent item={location} />
        </CardWrapper>
      </Grid>
    ))
  ) : (
    <Loading />
  );
  return (
    <Grid container spacing={2}>
      {children}
    </Grid>
  );
}
