"use client";

import { CircularProgress, Grid } from "@mui/material";
import { Suspense } from "react";
import IdentityProviderCardContent from "./_components/identityProviderCardContent";
import Loading from "../identity_providers/loading";
import { useIdentityProviders } from "../_lib/crud";
import CardWrapper from "../_components/card/wrapper";
import { IdentityProvider } from "./_lib/dbTypes";

export default function Page() {
  const { identityProviders } = useIdentityProviders();
  const children = identityProviders ? (
    identityProviders.map(
      (identityProvider: IdentityProvider, index: number) => (
        <Grid item key={index}>
          <CardWrapper
            kind="identity_providers"
            name={identityProvider.endpoint.toString()}
            uid={identityProvider.uid}
          >
            <IdentityProviderCardContent item={identityProvider} />
          </CardWrapper>
        </Grid>
      )
    )
  ) : (
    <Loading />
  );
  return (
    <Grid container spacing={2}>
      {children}
    </Grid>
  );
}
