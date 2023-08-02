"use client";

import { Grid } from "@mui/material";
import ProviderCardContent from "./_components/providerCardContent";
import Loading from "./loading";
import { useProviders } from "../_lib/crud";
import CardWrapper from "../_components/card/wrapper";
import { Provider } from "./_lib/dbTypes";

export default function Page() {
  const { providers } = useProviders();
  const children = providers ? (
    providers.map((provider: Provider, index: number) => (
      <Grid item key={index}>
        <CardWrapper kind="providers" name={provider.name} uid={provider.uid}>
          <ProviderCardContent item={provider} />
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
