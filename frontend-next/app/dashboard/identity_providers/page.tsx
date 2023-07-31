import { Grid } from "@mui/material";
import { Suspense } from "react";
import IdentityProviderCardContent from "./_components/identityProviderCardContent";
import Loading from "../identity_providers/loading";
import { getIdentityProviders } from "../_lib/crud";
import CardWrapper from "../_components/card/wrapper";
import { IdentityProvider } from "./_lib/dbTypes";

export default async function Page() {
  const identity_providers: IdentityProvider[] = await getIdentityProviders();
  let children = identity_providers.map((identity_provider, index) => (
    <Grid item key={index}>
      <CardWrapper
        kind="identity_providers"
        name={identity_provider.endpoint.toString()}
        uid={identity_provider.uid}
      >
        <IdentityProviderCardContent item={identity_provider} />
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
