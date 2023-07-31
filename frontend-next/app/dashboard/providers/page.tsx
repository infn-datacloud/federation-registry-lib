import { Grid } from "@mui/material";
import { Suspense } from "react";
import ProviderCardContent from "./_components/providerCardContent";
import Loading from "./loading";
import { getProviders } from "../_lib/crud";
import CardWrapper from "../_components/card/wrapper";
import { Provider } from "./_lib/dbTypes";

export default async function Page() {
  const providers: Provider[] = await getProviders();
  let children = providers.map((provider, index) => (
    <Grid item key={index}>
      <CardWrapper kind="providers" name={provider.name} uid={provider.uid}>
        <ProviderCardContent item={provider} />
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
